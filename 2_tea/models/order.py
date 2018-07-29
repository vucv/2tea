# coding=utf-8
from openerp import _,models,fields,api


class Order(models.Model):
    _name = 'tea.order'
    _description = 'Order Food'

    ban = fields.Many2one("tea.ban", "Bàn", required=True)
    mon_an = fields.One2many("tea.order.mon", "order_id", "Món")
    description = fields.Text("Ghi Chú")
    color = fields.Integer("Color")


class OrderDetail(models.Model):
    _name = 'tea.order.mon'
    _description = 'Order Food'

    order_id = fields.Many2one("tea.order", "Đặt hàng", required=True)
    # ban = fields.Many2one("tea.ban", "Bàn", required=True)
    mon_an = fields.Many2one("tea.food", "Món", required=True)
    mon_them = fields.Many2many("tea.food", "tea_order_mon_them", "order_mon_id", "food_id", "Thêm")
    description = fields.Text("Description")
    color = fields.Integer("Color")