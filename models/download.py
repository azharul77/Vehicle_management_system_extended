from odoo import models, fields, _, api
from odoo.exceptions import UserError
import PyPDF2
import tempfile
import os
import base64
import io

class download(models.Model):
    _inherit = ['sale.order', 'stock.picking']
    transaction_ids = fields.Many2many('payment.transaction', 'sale_order_transaction_rel', 'sale_order_id',
                                       'transaction_ids',
                                       string='Transactions', copy=False, readonly=True)

    tag_ids = fields.Many2many('crm.tag', 'sale_order_tag_rel', 'order_id', 'tag_ids', string='Tags')

    def generate_awb_pdf(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        pickings = self.env['stock.picking'].search([('origin', 'in', [o.name for o in sale_orders])])
        attachment_ids = self.env['ir.attachment'].search(
            [('res_model', '=', 'stock.picking'), ('res_id', 'in', [p.id for p in pickings])])
        result = b''

        for rec in attachment_ids:
            result += rec.datas
            attachment_obj = self.env['ir.attachment']
            attachment_id = attachment_obj.sudo().create(
                {'name': "name", 'store_fname': 'awb.pdf', 'datas': rec.datas})
            download_url = '/web/content/' + str(attachment_id.id) + '?download=true'
            self.get_report(download_url)

    def get_report(self, download_url):
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        return {
            'name': 'Report',
            'type': 'ir.actions.act_url',
            'url': str(base_url) + str(download_url),
            'target': 'new',
        }