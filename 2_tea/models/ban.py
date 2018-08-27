# coding=utf-8
from openerp import _, models, fields, api
import random
import win32ui
import datetime


class Ban(models.Model):
    _name = 'tea.ban'
    _description = 'Vi tri phuc vu'
    _rec_name = 'name'

    name = fields.Char("Name", required=True)
    status = fields.Many2one("tea.ban.status", "Trạng Thái")
    km = fields.Many2one("tea.km", "Chương Trình KM", related="order_id.km")
    percent = fields.Integer("Giảm giá", related="km.percent")
    # status = fields.Selection([('0', 'Số có sẵn'), ('1', 'Chờ pha chế'), ('2', 'Đã phục vụ'), ('3', 'Đã thanh toán')], "Trạng Thái", default="0")
    description = fields.Text("Mô tả")
    color = fields.Integer("Color")
    order_id = fields.Many2one("tea.order", "Đặt hàng")
    mon_an = fields.One2many("tea.order.mon", "ban", "Món", domain=[("is_thanh_toan", "=", False)])
    position = fields.Many2one("tea.order.position", "Khu vực", related="order_id.position")
    is_thanh_toan = fields.Boolean("Đã thanh toán")
    price = fields.Float("Thành tiền", related="order_id.price")

    def _read_group_stage_ids(self, cr, uid, ids, domain, read_group_order=None, access_rights_uid=None, context=None):
        stage_obj = self.pool.get('tea.ban.status')
        stage_ids = stage_obj.search(cr, uid, [], context=context)
        result = stage_obj.name_get(cr, uid, stage_ids, context=context)
        return result, {}

    _group_by_full = {
        'status': _read_group_stage_ids,
    }
    _defaults = {
        'status': lambda self, cr, uid, c: self.pool['ir.model.data'].xmlid_to_object(cr, uid, '2_tea.0', False),
    }

    @api.model
    def create(self, vals):
        vals['color'] = random.randint(0, 9)
        rec = super(Ban, self).create(vals)
        return rec

    @api.multi
    def action_order(self):
        return {
            'name': self.name,
            'res_model': 'tea.order',
            'type': 'ir.actions.act_window',
            'context': {'default_ban': self.id},
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.order_id.id,
            'view_id': self.env.ref('2_tea.tea_order_form_view').id,
            'target': 'current'
        }

    @api.one
    def action_checkout(self):
        # Check tien thối

        # In bill
        # test_print("Hello Would!!!")
        print_bill(self.order_id)
        # L0gic
        self.write({"is_thanh_toan": True})

    @api.one
    def action_in_tem(self):
        n = 0
        for i, mon_an in enumerate(self.order_id.mon_an):
            if mon_an.mon_an.is_print_temp and mon_an.status == 1:
                for j in range(0, mon_an.sl):
                    n += 1
                    print_mon_an(mon_an, "(%s/%s)" % (n, self.order_id.sl))

    @api.one
    def action_reset_so(self):
        # Change status to 0
        self.order_id.write({"is_thanh_toan": True})
        self.write({"status": self.env.ref('2_tea.0').id, "order_id": False, "is_thanh_toan": False})
        return {'type': 'ir.actions.act_close_wizard_and_reload_view'}

    @api.multi
    def write(self, vals):
        if "status" in vals:
            for item in self:
                if not item.is_thanh_toan and vals.get("status", 0) == 4:
                    warning = {'title': 'Cảnh báo!', 'message': 'Tính tiền trước khi chuyển qua trạng thái này'}
                    return {'warning': warning}
                if not item.mon_an and vals.get("status", 0) != 1:
                    warning = {'title': 'Cảnh báo!', 'message': 'Chưa gọi món'}
                    return {'warning': warning}
        rec = super(Ban, self).write(vals)
        for item in self:
            if vals.get("status", 0) == 3:
                item.mon_an.write({"status": 3})
        return rec


class BanStatus(models.Model):
    _name = 'tea.ban.status'
    _description = 'Trang thai bàn'

    name = fields.Char("Name", required=True)


def test_print(input_string):
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC("XP-80")
    hDC.StartDoc("XXX")
    hDC.StartPage()
    hDC.TextOut(0, 0, input_string)
    for x in range(0, 200):
        hDC.TextOut(50, x, str(x))
    hDC.EndPage()
    hDC.EndDoc()


fonts = {}


def createFonts():
    global fonts
    normal = {
        'name': 'Courier New',
        'size': 12,
        'weight': 400
    }
    bold = {
        'name': 'Courier New',
        'size': 12,
        'weight': 700
    }
    italic = {
        'name': 'Courier New',
        'size': 12,
        'weight': 400,
        'italic': 1
    }
    for i in ['normal', 'bold', 'italic']:
        d = locals().get(i)
        f = win32ui.CreateFont(d)
        fonts[i] = f


def print_bill(order):
    Y = 0
    hDC = win32ui.CreateDC()
    font_h1 = win32ui.CreateFont({
        "name": "Courier New",
        "height": 70,
        "weight": 800,
        "charset": 0x000000A3
    })
    font_h2 = win32ui.CreateFont({
        "name": "Courier New",
        "height": 30,
        "weight": 700,
        "charset": 0x000000A3
    })
    font_normal = win32ui.CreateFont({
        "name": "Courier New",
        "height": 25,
        "weight": 600
    })
    hDC.CreatePrinterDC("XP-80")
    hDC.StartDoc("XXX")
    hDC.StartPage()
    hDC.SelectObject(font_h1)
    hDC.TextOut(60, 0, "Tra Sua 2Tea")
    Y += 60
    hDC.SelectObject(font_normal)
    hDC.TextOut(0, Y, "HD:" + str(order.id))
    hDC.TextOut(200, Y, "Ngay:" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    Y += 30
    hDC.SelectObject(font_h2)
    hDC.TextOut(0, Y, "Mon")
    hDC.TextOut(330, Y, str("Size"))
    hDC.TextOut(410, Y, str("SL"))
    hDC.TextOut(490, Y, str("Gia"))
    Y += 40
    hDC.SelectObject(font_normal)
    for item in order.mon_an:
        p = 0
        if len(item.mon_an.name_print) > 20:
            chars = item.mon_an.name_print.split(" ")
            lines = []
            line = []
            n = 0
            for char in chars:
                n += len(char)
                if n > 15:
                    hDC.TextOut(0, Y + p * 20, " ".join(line))
                    p += 1
                    line = []
                    n = 0
                else:
                    line.append(char)
            if n > 0:
                hDC.TextOut(0, Y + p * 20, " ".join(line))

        else:
            hDC.TextOut(0, Y, item.mon_an.name_print)

        hDC.TextOut(415, Y, str(item.sl))
        if item.size == 2:
            hDC.TextOut(360, Y, "L")
            hDC.TextOut(450, Y, str(item.mon_an.price_xl))
        else:
            hDC.TextOut(360, Y, "M")
            hDC.TextOut(450, Y, str(item.mon_an.price))
        Y += 40
    hDC.TextOut(0, Y, "                      --------------")
    Y += 20
    hDC.SelectObject(font_h2)
    hDC.TextOut(0, Y, "Tong cong:")
    hDC.TextOut(450, Y, str(order.price))
    Y += 30
    hDC.TextOut(0, Y, "Tien mat:")
    hDC.TextOut(450, Y, str(order.price))
    Y += 30
    hDC.TextOut(0, Y, "Thoi lai:")
    hDC.TextOut(450, Y, str(0))
    Y += 30
    hDC.TextOut(0, Y, "====================================")
    Y += 30
    if order.km:
        hDC.TextOut(0, Y, "Ap dung KM:")
        hDC.TextOut(150, Y, order.km.name_print)
    Y += 30
    hDC.SelectObject(font_h2)
    hDC.TextOut(0, Y, "*******CHUC QUY KHACH VUI VE*****")

    hDC.EndPage()
    hDC.EndDoc()


def print_mon_an(mon_an, note):
    Y = 10
    hDC = win32ui.CreateDC()
    font_h1 = win32ui.CreateFont({
        "name": "Courier New",
        "height": 70,
        "weight": 800,
        "charset": 0x000000A3
    })
    font_h2 = win32ui.CreateFont({
        "name": "Courier New",
        "height": 30,
        "weight": 700,
        "charset": 0x000000A3
    })
    font_normal = win32ui.CreateFont({
        "name": "Courier New",
        "height": 25,
        "weight": 600
    })
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC("Gprinter 2120TU(Label)")
    hDC.StartDoc("XXX")
    hDC.StartPage()
    hDC.SelectObject(font_h2)
    p = 0
    if len(mon_an.mon_an.name_print) > 20:
        chars = mon_an.mon_an.name_print.split(" ")
        lines = []
        line = []
        n = 0
        for char in chars:
            n += len(char)
            if n > 20:
                hDC.TextOut(30, Y + p * 30, " ".join(line))
                p += 1
                line = []
                n = 0
            else:
                line.append(char)
        if n > 0:
            hDC.TextOut(30, Y + p * 30, " ".join(line))

    else:
        hDC.TextOut(30, Y, mon_an.mon_an.name_print)
    Y += 30 + p * 20

    hDC.TextOut(50, Y + 20, "Size:")
    hDC.SelectObject(font_h1)
    if mon_an.size == 2:
        hDC.TextOut(150, Y, "L")
    else:
        hDC.TextOut(150, Y, "M")
    hDC.SelectObject(font_h2)
    hDC.TextOut(200, Y + 20, note)
    Y += 50
    hDC.SelectObject(font_normal)
    hDC.TextOut(0, Y, "======================")
    Y += 20
    text = []
    for item in mon_an.mon_them:
        text = text + item.name_print.split(" ")
        text.append(",")
    if len(text) > 1:
        del text[-1]
    p = 0
    if len(text) > 20:
        lines = []
        line = []
        n = 0
        for char in text:
            n += len(char)
            if n > 20:
                hDC.TextOut(30, Y + p * 20, " ".join(line))
                p += 1
                line = []
                n = 0
            else:
                line.append(char)
        if n > 0:
            hDC.TextOut(30, Y + p * 20, " ".join(line))
    else:
        hDC.TextOut(30, Y, " ".join(text))
    Y += 30 + p * 20
    hDC.SelectObject(font_normal)
    p = 0
    if mon_an.description != False and len(mon_an.description) > 20:
        chars = mon_an.description.split(" ")
        lines = []
        line = []
        n = 0
        for char in chars:
            line.append(char)
            n += len(char)
            if n > 20:
                hDC.TextOut(30, Y + p * 20, " ".join(line))
                p += 1
                line = []
                n = 0
        if n > 0:
            hDC.TextOut(30, Y + p * 20, " ".join(line))

    elif mon_an.description != False:
        hDC.TextOut(20, Y, mon_an.description)
    hDC.EndPage()
    hDC.EndDoc()
