# -*- coding: utf-8 -*-
# Copyright 2015 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from cStringIO import StringIO

from openerp.report.report_sxw import report_sxw
from openerp import pooler
import logging
_logger = logging.getLogger(__name__)

try:
    import xlsxwriter
except ImportError:
    _logger.debug('Can not import xlsxwriter`.')


class ReportXlsx(report_sxw):

    def create(self, cr, uid, ids, data, context=None):
        self.pool = pooler.get_pool(cr.dbname)
        self.cr = cr
        self.uid = uid
        report_obj = self.pool.get('ir.actions.report.xml')
        report_ids = report_obj.search(
            cr, uid, [('report_name', '=', self.name[7:])], context=context)
        if report_ids:
            report_xml = report_obj.browse(
                cr, uid, report_ids[0], context=context)
            self.title = report_xml.name
            if report_xml.report_type == 'xlsx':
                return self.create_xlsx_report(cr, uid, ids, data, report_xml, context)
        return super(ReportXlsx, self).create(cr, uid, ids, data, context)

    def create_xlsx_report(self, cr, uid, ids, data, report, context):
        self.parser_instance = self.parser(
            cr, uid, self.name2, context)
        objs = self.getObjects(
            cr, uid, ids, context)
        self.parser_instance.set_context(objs, data, ids, 'xlsx')
        file_data = StringIO()
        workbook = xlsxwriter.Workbook(file_data)
        self.generate_xlsx_report(workbook, data, objs)
        workbook.close()
        file_data.seek(0)
        return (file_data.read(), 'xlsx')

    def generate_xlsx_report(self, workbook, data, objs):
        raise NotImplementedError()
