# coding=utf-8
from openerp import _,models,fields,api


class Ban(models.Model):
    _name = 'tea.ban'
    _description = 'Vi tri phuc vu'

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    color = fields.Integer("Color")
