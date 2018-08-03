# coding=utf-8
from openerp import _,models,fields,api


class Order(models.Model):
    _name = 'tea.order'
    _description = 'Order Food'
    _rec_name = 'ban'

    ban = fields.Many2one("tea.ban", "Bàn", domain="[('status', '=', '0')]", required=True)
    mon_an = fields.One2many("tea.order.mon", "order_id", "Món")
    description = fields.Text("Ghi Chú")
    color = fields.Integer("Color")


class OrderDetail(models.Model):
    _name = 'tea.order.mon'
    _description = 'Order Food'
    _rec_name = 'ban'

    order_id = fields.Many2one("tea.order", "Đặt hàng", required=True)
    ban = fields.Many2one("tea.ban", "Bàn", related="order_id.ban")
    status = fields.Selection([('0', 'Chưa làm'), ('1', 'Đang làm'), ('2', 'Xong')], "Trạng Thái", default="0")
    mon_an = fields.Many2one("tea.food", "Món", domain="[('is_required', '=', True)]", required=True)
    mon_them = fields.Many2many("tea.food", "tea_order_mon_them", "order_mon_id", "food_id", "Thêm",
                                domain="[('is_required', '=', False)]")
    description = fields.Text("Ghi chú")
    color = fields.Integer("Color")