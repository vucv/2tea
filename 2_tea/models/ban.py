# coding=utf-8
from openerp import _,models,fields,api
import random
import win32ui
import win32con


class Ban(models.Model):
    _name = 'tea.ban'
    _description = 'Vi tri phuc vu'
    _rec_name = 'name'

    name = fields.Char("Name", required=True)
    status = fields.Many2one("tea.ban.status", "Trạng Thái")
    # status = fields.Selection([('0', 'Số có sẵn'), ('1', 'Chờ pha chế'), ('2', 'Đã phục vụ'), ('3', 'Đã thanh toán')], "Trạng Thái", default="0")
    description = fields.Text("Mô tả")
    color = fields.Integer("Color")
    order_id = fields.Many2one("tea.order", "Đặt hàng")
    mon_an = fields.One2many("tea.order.mon", "ban", "Món", domain=[("is_thanh_toan", "=", False)])
    position = fields.Many2one("tea.order.position", "Khu vực", related="order_id.position")
    is_thanh_toan = fields.Boolean("Đã thanh toán")

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
        print_bill(self.order_id.mon_an)
        # L0gic
        self.write({"is_thanh_toan": True})

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
                    item.action_checkout()
        rec = super(Ban, self).write(vals)
        return rec


class BanStatus(models.Model):
    _name = 'tea.ban.status'
    _description = 'Trang thai bàn'

    name = fields.Char("Name", required=True)


def test_print(input_string):
    hDC = win32ui.CreateDC ()
    hDC.CreatePrinterDC ("XP-80")
    hDC.StartDoc ("XXX")
    hDC.StartPage ()
    hDC.TextOut(0,0,input_string)
    for x in range(0, 200):
        hDC.TextOut(50,x,str(x))
    hDC.EndPage ()
    hDC.EndDoc ()


def print_bill(order):
    X = 0
    Y = 0
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC("XP-80")
    hDC.StartDoc("XXX")
    hDC.StartPage()
    hDC.TextOut(0, 0, "Trà Sữa 2Tea")
    Y += 50
    for item in order:
        hDC.TextOut(0, Y, item.mon_an.name)
        hDC.TextOut(300, Y, str(item.sl))
        hDC.TextOut(450, Y, str(item.mon_an.price))
        Y += 40
    hDC.EndPage()
    hDC.EndDoc()
#
#
# def print_mon_an(self):
#     p = Usb(0x04b8, 0x0202, 0, profile="TM-T88III")
#     p.text("Hello World\n")
#     p.image("logo.gif")
#     p.barcode('1324354657687', 'EAN13', 64, 2, '', '')
#     p.cut()