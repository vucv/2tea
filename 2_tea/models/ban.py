# coding=utf-8
from openerp import _,models,fields,api
import random


class Ban(models.Model):
    _name = 'tea.ban'
    _description = 'Vi tri phuc vu'
    _rec_name = 'name'

    name = fields.Char("Name", required=True)
    status = fields.Many2one("tea.ban.status", "Trạng Thái", default=1)
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
        self.write({"status": self.env.ref('2_tea.3').id, "is_thanh_toan": True})
        self.order_id.write({"is_thanh_toan": True})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'tea.ban',
            'view_type': 'form',
            'view_mode': 'kanban',
            'target': 'new',
        }

    @api.one
    def action_reset_so(self):
        # Change status to 0
        self.order_id.write({"is_thanh_toan": True})
        return self.write({"status": self.env.ref('2_tea.0').id, "order_id": False, "is_thanh_toan": False})
        # return {
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'tea.ban',
        #     'view_type': 'form',
        #     'view_mode': 'kanban',
        #     'target': 'new',
        # }

    @api.onchange('mon_an')
    def onchange_monan(self):
        if not self.mon_an:
            self.status = "0"
        else:
            self.status = "1"


class BanStatus(models.Model):
    _name = 'tea.ban.status'
    _description = 'Trang thai bàn'

    name = fields.Char("Name", required=True)
