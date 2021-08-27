# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_notes = fields.Boolean(string='Is Notes', default=False)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        self.ensure_one()

        value = super(SaleOrder, self)._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)
        SaleOrderLineSudo = self.env['sale.order.line'].sudo()
        line = SaleOrderLineSudo.browse(value.get('line_id'))

        if kwargs.get('notes') and line:
            line.write({'notes': kwargs.get('notes')})
        return value

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    notes = fields.Text(string="Product Notes")