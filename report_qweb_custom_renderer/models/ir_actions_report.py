# Copyright 2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)
from datetime import datetime


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    qweb_pdf_engine = fields.Selection(
        [('wkhtmltopdf', 'wkhtmltopdf')], default='wkhtmltopdf',
        string='PDF Engine',
    )

    def _render_qweb_pdf(self, res_ids=None, data=None):
        start = datetime.now()
        if self.qweb_pdf_engine == 'wkhtmltopdf':
            res = super()._render_qweb_pdf(
                res_ids=res_ids, data=data,
            )
        else:
            res = getattr(self, '_render_qweb_pdf_%s' % self.qweb_pdf_engine)(
                res_ids=res_ids, data=data,
            )
        print("===============")
        print("Process", self.qweb_pdf_engine, datetime.now() - start)
        print("===============")
        return res
