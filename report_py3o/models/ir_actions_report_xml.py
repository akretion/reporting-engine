# -*- coding: utf-8 -*-
# Copyright 2013 XCG Consulting (http://odoo.consulting)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import os
import logging
from openerp import api, fields, models, SUPERUSER_ID, _
from openerp.report.interface import report_int
from openerp.exceptions import ValidationError
from openerp import addons
from ..py3o_parser import Py3oParser

logger = logging.getLogger(__name__)

try:
    from py3o.formats import Formats
except ImportError:
    logger.debug('Cannot import py3o.formats')


class IrActionsReportXml(models.Model):
    """ Inherit from ir.actions.report.xml to allow customizing the template
    file. The user cam chose a template from a list.
    The list is configurable in the configuration tab, see py3o_template.py
    """

    _inherit = 'ir.actions.report.xml'

    @api.one
    @api.constrains("py3o_filetype", "report_type")
    def _check_py3o_filetype(self):
        if self.report_type == "py3o" and not self.py3o_filetype:
            raise ValidationError(_(
                "Field 'Output Format' is required for Py3O report"))

    @api.one
    @api.constrains("py3o_is_local_fusion", "py3o_server_id",
                    "py3o_filetype")
    def _check_py3o_server_id(self):
        is_native = Formats().get_format(self.py3o_filetype)
        if ((not is_native or not self.py3o_is_local_fusion) and
                not self.py3o_server_id):
            raise ValidationError(_(
                "Can not use not native format in local fusion. "
                "Please specify a Fusion Server"))

    @api.model
    def _get_py3o_filetypes(self):
        formats = Formats()
        names = formats.get_known_format_names()
        selections = []
        for name in names:
            description = name
            if formats.get_format(name).native:
                description = description + " " + _("(Native)")
            selections.append((name, description))
        return selections

    py3o_filetype = fields.Selection(
        selection="_get_py3o_filetypes",
        string="Output Format")
    py3o_template_id = fields.Many2one(
        'py3o.template',
        "Template")
    py3o_is_local_fusion = fields.Boolean(
        "Local Fusion",
        help="Native formats will be processed without a server. "
             "You must use this mode if you call methods on your model into "
             "the template.",
        default=True)
    py3o_server_id = fields.Many2one(
        "py3o.server",
        "Fusion Server")
    module = fields.Char(
        "Module",
        help="The implementer module that provides this report")
    py3o_template_fallback = fields.Char(
        "Fallback",
        size=128,
        help=(
            "If the user does not provide a template this will be used "
            "it should be a relative path to root of YOUR module "
            "or an absolute path on your server."
        ))
    report_type = fields.Selection(selection_add=[('py3o', "Py3o")])

    @api.cr
    def _lookup_report(self, cr, name):
        """Look up a report definition.
        """

        # First lookup in the deprecated place, because if the report
        # definition has not been updated, it is more likely the correct
        # definition is there. Only reports with custom parser
        # specified in Python are still there.
        if 'report.' + name in report_int._reports:
            new_report = report_int._reports['report.' + name]
            if not isinstance(new_report, Py3oParser):
                new_report = None
        else:
            report_data = self.search_read(
                cr, SUPERUSER_ID,
                [("report_name", "=", name),
                 ("report_type", "=", "py3o")],
                ['parser', 'model', 'report_name', 'report_rml', 'header'],
                limit=1)
            if report_data:
                report_data = report_data[0]
                kwargs = {}
                if report_data['parser']:
                    kwargs['parser'] = getattr(addons, report_data['parser'])

                new_report = Py3oParser(
                    'report.' + report_data['report_name'],
                    report_data['model'],
                    os.path.join('addons', report_data['report_rml'] or '/'),
                    header=report_data['header'],
                    register=False,
                    **kwargs
                )
            else:
                new_report = None

        if new_report:
            return new_report
        else:
            return super(IrActionsReportXml, self)._lookup_report(cr, name)