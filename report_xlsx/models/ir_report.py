# -*- coding: utf-8 -*-
# Copyright 2015 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import orm, fields


class IrActionsReportXml(orm.Model):
    _inherit = 'ir.actions.report.xml'

    report_type = fields.selection(selection_add=[("xlsx", "xlsx")])
