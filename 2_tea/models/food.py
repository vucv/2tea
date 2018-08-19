# coding=utf-8
from openerp import _,models,fields,api
import random


class Food(models.Model):
    _name = 'tea.food'
    _description = 'Menu and Food'
    _rec_name = 'name'

    name = fields.Char("Name", required=True)
    description = fields.Text("Công thức")
    is_required = fields.Boolean("Món chính")
    is_print_temp = fields.Boolean("In tem lên ly")
    image = fields.Binary(string="Image")
    price = fields.Float("Giá")
    color = fields.Integer("Color")

    @api.model
    def create(self, vals):
        vals['color'] = random.randint(0, 9)
        rec = super(Food, self).create(vals)
        return rec

