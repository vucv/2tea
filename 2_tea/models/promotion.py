# coding=utf-8
from openerp import _,models,fields,api
import random


class KM(models.Model):
    _name = 'tea.km'
    _description = 'KM'
    _rec_name = 'name'

    name = fields.Char("Tên", required=True)
    name_print = fields.Char("Tên In tem", required=True)
    description = fields.Text("Chi tiết chương trình")
    percent = fields.Integer("Giảm giá")
    active = fields.Boolean("Kích Hoạt", default=True)


