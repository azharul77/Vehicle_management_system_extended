from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class CrmInherit(models.Model):
    _inherit = ['res.partner']

    aadhar_number = fields.Char(string='Aadhar Card No.')
    esi_number = fields.Char(string='ESI No.')
    vehicle_registration_number = fields.One2many('vehicle.info', 'vehicle_owner', string="Vehicle Number")


class CustomerInfo(models.Model):
    _name = 'customer.info'
    _description = 'Customer record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one('res.partner', string='Customer Name', required=True)
    code = fields.Char(string="Code", readonly=True)
    customer_address_number = fields.Char(string='Address')
    customer_phone_number = fields.Char(string='Customer Phone Number')
    notes = fields.Text(string='Maintain Customer Detail')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Name already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!'),
    ]

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('customer.info')
        res = super(CustomerInfo, self).create(vals)
        return res

    @api.onchange('name')
    def onchange_vehicle_owner(self):
        for rec in self:
            if rec.name:
                rec.customer_phone_number = rec.name.phone

    @api.onchange('name')
    def onchange_customer_address(self):
        for rec in self:
            if rec.name:
                rec.customer_address_number = rec.name.street