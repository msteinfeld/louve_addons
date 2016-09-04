# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today: Smile (<http://www.smile.fr>)
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from openerp.addons import decimal_precision as dp


class ProductCoefficient(models.Model):
    _name = 'product.coefficient'
    _order = 'name'

    _SELECT_OPERATION_TYPE = [
        ('multiplier', 'Multiplier'),
        ('fixed', 'Fixed Amount'),
    ]

    _SELECT_COEFFICIENT_TYPE = [
        ('supplier', 'Supplier Coefficient'),
        ('shipping', 'Shipping Coefficient'),
        ('loss', 'Loss Coefficient'),
        ('custom', 'Custom Coefficient'),
        ('margin', 'Margin Coefficient'),
    ]

    # Column Section
    name = fields.Char(string='Name', required=True)

    value = fields.Float(
        string='Value', digits=dp.get_precision('Product Price'))

    operation_type = fields.Selection(
        string='Operation Type', selection=_SELECT_OPERATION_TYPE,
        required=True, default='multiplier')

    coefficient_type = fields.Selection(
        string='Coefficient Type', selection=_SELECT_COEFFICIENT_TYPE,
        required=True, default='custom')

    # Compute Section
    @api.model
    def compute_price(self, coefficient, reference_price):
        if not coefficient:
            return reference_price
        elif coefficient.operation_type == 'multiplier':
            return reference_price * (1 + coefficient.value)
        else:
            return reference_price + coefficient.value
