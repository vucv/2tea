# coding=utf-8
from openerp import _,models,fields,api


class Food(models.Model):
    _name = 'tea.food'
    _description = 'Menu and Food'

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
