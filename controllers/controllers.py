from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleProductNotes(WebsiteSale):
    @http.route()
    def product(self, product, category='', search='', **kwargs):
        res = super(WebsiteSaleProductNotes, self).product(product, category=category, search=search, **kwargs)
        res.qcontext.update({'sale_order': request.website.sale_get_order()})
        return res

    @http.route()
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        redirect = super(WebsiteSaleProductNotes, self).cart_update(product_id, add_qty=add_qty, set_qty=set_qty, **kw)
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.state != 'draft':
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)
        sale_order._cart_update(
            product_id=int(product_id),
#            add_qty=add_qty,
            set_qty=set_qty,
            attributes=self._filter_attributes(**kw),
            **kw
        )
        return redirect