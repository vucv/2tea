# coding=utf-8
from openerp import _,models,fields,api


class Food(models.Model):
    _name = 'tea.food'
    _description = 'Menu and Food'
    _rec_name = 'name'

    name = fields.Char("Name", required=True)
    description = fields.Text("Công thức")
    is_required = fields.Boolean("Món chính")
    image = fields.Binary(string="Image")
    price = fields.Float("Giá")
    color = fields.Integer("Color")

