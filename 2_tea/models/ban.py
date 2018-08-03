# coding=utf-8
from openerp import _,models,fields,api


class Ban(models.Model):
    _name = 'tea.ban'
    _description = 'Vi tri phuc vu'
    _rec_name = 'name'

    name = fields.Char("Name", required=True)
    status = fields.Selection([('0', 'Trống'), ('1', 'Đang Phục Vụ')], "Trạng Thái", default="0")
    description = fields.Text("Mô tả")
    color = fields.Integer("Color")

    # _group_by_full = {'status': [0,1]}


class Ban(models.Model):
    _name = 'tea.ban.status'
    _description = 'Vi tri phuc vu'

    name = fields.Char("Name", required=True)
