import logging

from odoo import models, fields, api, _
from odoo.exceptions import Warning
from odoo.tools import exception_to_unicode
import xlsxwriter
import base64
import datetime
from odoo.tools import misc
from operator import itemgetter, attrgetter
import math
import os
import calendar
import logging

_logger = logging.getLogger(__name__)
import io

try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')

try:
    import pandas
except ImportError:
    _logger.debug('Cannot `import pandas`.')

try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class csv_import(models.TransientModel):
    _name = "csv.import"

    file_to_upload = fields.Binary('File')
    import_option = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select', default='csv')

    # Upload CSV File In Content

    @api.multi
    def import_csv_content(self):
        # You need to Set Configurations In Settings
        setting = self.env['setting.file'].search([('active', '=', True)], limit=1)
        delimiter = setting.delimiter
        header = ['id', 'name', 'description', 'device/id', 'expire_date', 'state']
        # Add Your CSV File Here You Can Set Any Local Path Here
        csv_file_path = os.path.join(setting.local_path, 'content_import.csv')
        report_data = open(csv_file_path, 'rb+')
        file = report_data.read()
        data_file = io.TextIOWrapper(io.BytesIO(file), encoding="utf-8-sig")
        if not data_file:
            _logger.warning("File is Missing!!!")
        reader = csv.DictReader(data_file, delimiter=delimiter)
        if len(header) != len(reader.fieldnames):
            _logger.warning("Invalid Header Found!!!")
        data = [row for row in reader]
        if not data:
            _logger.warning("This File Is Empty!!!")
        imp_obj = self.env['content.sync']
        try:
            for list_val in data:
                if not list_val['id']:
                    _logger.warning("Id is Missing!!!")
                if not list_val['name']:
                    _logger.warning("Name is Missing!!!")
                if not list_val['description']:
                    _logger.warning("Description is Missing!!!")
                if not list_val['device/id']:
                    _logger.warning("Device is Missing!!!")
                if not list_val['expire_date']:
                    _logger.warning("Expire Date is Missing!!!")
                if not list_val['state']:
                    _logger.warning("State is Missing!!!")
                self.create_content(list_val['id'], list_val['name'], list_val['description'], list_val['device/id'],
                                    list_val['expire_date'], list_val['state'],
                                    imp_obj)
        except Exception as e:
            _logger.info("Content Sync Process Failed!!!")
            _logger.info(exception_to_unicode(e))
        return False

    # Create Content
    def create_content(self, id, name, description, device, expire_date, state, obj):
        obj.create(
            {'id': id, 'name': name, 'description': description, 'device': device,
             'expire_date': expire_date, 'state': state})
        return True


class csv_download_content(models.TransientModel):
    _name = "csv.download.content"
    _description = "Download content"

    excel_file = fields.Binary('excel file')
    file_name = fields.Char('Excel File', size=64)
    is_printed = fields.Boolean('Printed', default=False)

    @api.multi
    def action_download(self, context=None):
        # this is the function related to the report creation
        active_ids = context.get('active_ids', []) or []
        self.report_data(active_ids)
        # file name of the report to be created
        filename = os.path.join('ContentReport.csv')
        # converts the report to binary
        my_report_data = open(filename, 'rb+')
        file = my_report_data.read()
        record_id = self.env['csv.download.content'].create({'excel_file': base64.encodestring(file),
                                                             'file_name': filename, 'is_printed': True})

        cr, uid, context = record_id.env.args
        ctx = dict(context)
        ctx.update({'report_file': base64.encodestring(file)})
        ctx.update({'file': filename})
        record_id.env.args = cr, uid, misc.frozendict(context)
        return {'view_mode': 'form',
                'res_id': record_id.id,
                'res_model': 'csv.download.content',
                'view_type': 'form',
                'context': ctx,
                'type': 'ir.actions.act_window',
                'target': 'new',
                }

    @api.multi
    def report_data(self, active_ids):
        # creating the file
        filename = os.path.join('Content Report' + '.csv')
        # create the workbook and worksheet
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        worksheet.set_landscape()

        # formatting properties and options needed to the report

        format_3 = workbook.add_format(
            {'align': 'center', 'font_size': 10, 'font_name': "Trebuchet MS", 'border': 1, 'valign': 'vcenter',
             'bold': True})
        data = workbook.add_format(
            {'align': 'center', 'font_size': 10, 'font_name': "Trebuchet MS", 'border': 1, 'valign': 'vcenter'})

        # setting width and height to column groups
        # worksheet.set_column('H:XFD', None, None, {'hidden': True})
        worksheet.set_column(0, 0, 15)
        worksheet.set_column(1, 1, 35)
        worksheet.set_column(2, 2, 30)

        row = 2
        col = 0

        # header

        worksheet.write(row + 1, col, "Name", format_3)
        worksheet.write(row + 1, col + 1, "Description", format_3)
        worksheet.write(row + 1, col + 2, "Device", format_3)
        worksheet.write(row + 1, col + 3, "Expire Date", format_3)
        worksheet.write(row + 1, col + 4, "State", format_3)

        domain = self.env['content.sync'].browse(active_ids)
        row = 4
        for record in domain:
            worksheet.write(row, col, record.name, data)
            worksheet.write(row, col + 1, record.description, data)
            worksheet.write(row, col + 2, record.device.name, data)
            worksheet.write(row, col + 3, str(record.expire_date), data)
            worksheet.write(row, col + 4, record.state, data)
            row += 1

        # close the workbook
        workbook.close()
        return filename
