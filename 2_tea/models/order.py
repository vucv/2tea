# coding=utf-8
from openerp import _,models,fields,api


class Order(models.Model):
    _name = 'tea.order'
    _description = 'Order Food'
    _rec_name = 'position'

    ban = fields.Many2one("tea.ban", "Bàn", domain="[('status', '=', '0')]", required=True)
    create_date = fields.datetime("Ngày", related='create_date')
    position = fields.Many2one("tea.order.position", "Khu vực")
    # position = fields.Selection([('0', 'Trong nhà'), ('1', 'Gác'), ('2', 'Vườn')], "Khu vực", default="0")
    mon_an = fields.One2many("tea.order.mon", "order_id", "Món")
    description = fields.Text("Ghi Chú")
    color = fields.Integer("Color")
    price = fields.Float("Thành tiền")
    currency_id = fields.Many2one('res.currency', string='Currency')
    is_thanh_toan = fields.Boolean("Đã thanh toán")
    sl = fields.Integer("Số Lượng", default=0)

    _defaults = {
        'position': lambda self, cr, uid, c: self.pool['ir.model.data'].xmlid_to_object(cr, uid, '2_tea.trong_nha', False),
        'currency_id': lambda self, cr, uid, c: self.pool['ir.model.data'].xmlid_to_object(cr, uid, 'base.VND', False),
    }

    @api.one
    def action_checkout(self):
        return self.ban.action_checkout()

    @api.one
    def action_in_tem(self):
        # In bill

        # Change status to
        return self.ban.action_in_tem()

    @api.onchange('mon_an')
    def onchange_monan(self):
        price = 0
        sl = 0
        for mon_an in self.mon_an:
            price += mon_an.price
            sl += mon_an.sl
        self.price = price
        self.sl = sl

    @api.model
    def create(self, vals):
        rec = super(Order, self).create(vals)
        rec.ban.write({"order_id": rec.id, "status": self.env.ref('2_tea.1').id})
        return rec

    @api.multi
    def write(self, vals):
        if "is_thanh_toan" in vals:
            for item in self:
                item.mon_an.write({"is_thanh_toan": True, "status": 3})
        rec = super(Order, self).write(vals)
        return rec


class OrderDetail(models.Model):
    _name = 'tea.order.mon'
    _description = 'Order Food'
    _rec_name = 'mon_an'

    order_id = fields.Many2one("tea.order", "Đặt hàng", required=True)
    ban = fields.Many2one("tea.ban", "Bàn", related="order_id.ban", store=True)
    is_thanh_toan = fields.Boolean("Đã thanh toán")
    size = fields.Selection([(1, 'M'), (2, 'L')], default=1)
    status = fields.Selection([(1, 'Chưa làm'), (2, 'Đang làm'), (3, 'Xong')], "Trạng Thái", default=1)
    mon_an = fields.Many2one("tea.food", "Món", domain="[('is_required', '=', True)]", required=True)
    mon_them = fields.Many2many("tea.food", "tea_order_mon_them", "order_mon_id", "food_id", "Thêm",
                                domain="[('is_required', '=', False)]")
    description = fields.Text("Ghi chú")
    price = fields.Float("Thành tiền")
    price_xl = fields.Float("Size L", related="mon_an.price_xl")
    currency_id = fields.Many2one('res.currency', string='Currency')
    sl = fields.Integer("Số Lượng", default=1)
    color = fields.Integer("Color")

    _defaults = {
        'currency_id': lambda self, cr, uid, c: self.pool['ir.model.data'].xmlid_to_object(cr, uid, 'base.VND', False),
    }

    @api.onchange('mon_an', 'mon_them', 'sl', 'size')
    @api.multi
    def onchange_monan(self):
        price = 0
        for item in self:
            if item.size == 2:
                price += item.mon_an.price_xl
            else:
                price += item.mon_an.price
            for mon_them in item.mon_them:
                price += mon_them.price
            if isinstance(item.mon_an.price_xl, float) and item.mon_an.price_xl == 0:
                item.size = False
            item.price = price*item.sl


class Position(models.Model):
    _name = 'tea.order.position'
    _description = 'Vị trí bàn'

    name = fields.Char("Name", required=True)
