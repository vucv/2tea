# coding=utf-8
from openerp import _,models,fields,api


class Order(models.Model):
    _name = 'tea.order'
    _description = 'Order Food'
    _rec_name = 'position'

    ban = fields.Many2one("tea.ban", "Bàn", domain="[('status', '=', '0')]", required=True)
    position = fields.Many2one("tea.order.position", "Khu vực")
    # position = fields.Selection([('0', 'Trong nhà'), ('1', 'Gác'), ('2', 'Vườn')], "Khu vực", default="0")
    mon_an = fields.One2many("tea.order.mon", "order_id", "Món")
    description = fields.Text("Ghi Chú")
    color = fields.Integer("Color")
    price = fields.Float("Thành tiền")
    is_thanh_toan = fields.Boolean("Đã thanh toán")

    _defaults = {
        'position': lambda self, cr, uid, c: self.pool['ir.model.data'].xmlid_to_object(cr, uid, '2_tea.trong_nha', False),
    }

    @api.one
    def action_checkout(self):
        return self.ban.action_checkout()

    @api.one
    def action_in_tem(self):
        # In bill

        # Change status to
        return self.ban.action_checkout()

    @api.onchange('mon_an')
    def onchange_monan(self):
        price = 0
        for mon_an in self.mon_an:
            price += mon_an.price

        self.price = price

    @api.model
    def create(self, vals):
        rec = super(Order, self).create(vals)
        rec.ban.write({"order_id": rec.id, "status": self.env.ref('2_tea.1').id})
        return rec

    @api.multi
    def write(self, vals):
        if "is_thanh_toan" in vals:
            for item in self:
                item.mon_an.write({"is_thanh_toan": True})
        rec = super(Order, self).write(vals)
        return rec


class OrderDetail(models.Model):
    _name = 'tea.order.mon'
    _description = 'Order Food'
    _rec_name = 'ban'

    order_id = fields.Many2one("tea.order", "Đặt hàng", required=True)
    ban = fields.Many2one("tea.ban", "Bàn", related="order_id.ban", store=True)
    is_thanh_toan = fields.Boolean("Đã thanh toán")
    status = fields.Selection([('0', 'Chưa làm'), ('1', 'Đang làm'), ('2', 'Xong')], "Trạng Thái", default="0")
    mon_an = fields.Many2one("tea.food", "Món", domain="[('is_required', '=', True)]", required=True)
    mon_them = fields.Many2many("tea.food", "tea_order_mon_them", "order_mon_id", "food_id", "Thêm",
                                domain="[('is_required', '=', False)]")
    description = fields.Text("Ghi chú")
    price = fields.Float("Thành tiền")
    sl = fields.Integer("Số Lượng", default=1)
    color = fields.Integer("Color")

    @api.onchange('mon_an', 'mon_them', 'sl')
    def onchange_monan(self):
        price = 0
        price += self.mon_an.price
        for mon_them in self.mon_them:
            price += mon_them.price

        self.price = price*self.sl


class Position(models.Model):
    _name = 'tea.order.position'
    _description = 'Vị trí bàn'

    name = fields.Char("Name", required=True)
