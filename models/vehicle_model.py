from odoo import models, fields, _, api


class VehicleBrand(models.Model):
    _name = 'vehicle.brand'
    _description = 'Vehicle Brand record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Brand Name', required=True)
    code = fields.Char(string="Code", readonly=True)
    company_id = fields.Many2one('res.company', string='Company Name')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Name already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!'),
    ]

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('vehicle.brand')
        res = super(VehicleBrand, self).create(vals)
        return res
