from odoo import models, fields, _, api
import logging

_logger = logging.getLogger(__name__)

# Enabling download attachment option in sale order action button


class download(models.Model):
    _inherit = ['sale.order']
    transaction_ids = fields.Many2many('payment.transaction', 'order_ids', string="Transactions")
    tag_ids = fields.Many2many('crm.tag', 'tag_ids', string='Tags')

    def generate_awb_pdf(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        attachment_ids = self.env['ir.attachment'].search(
            [('res_model', '=', 'sale.order'), ('res_id', 'in', [o.id for o in sale_orders])])

        for rec in attachment_ids:
            attachment_obj = self.env['ir.attachment']
            attachment_id = attachment_obj.sudo().create(
                {'name': "name", 'store_fname': 'awb.pdf', 'datas': rec.datas})
            download_url = '/web/content/' + str(attachment_id.id) + '?download=true'

        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        return {
            'name': 'Report',
            'type': 'ir.actions.act_url',
            'url': str(base_url) + str(download_url),
            'target': 'new',
        }

# adding user signature in purchase order


class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']

    signature = fields.Binary(string="Signature", attachment=True, store=True)




