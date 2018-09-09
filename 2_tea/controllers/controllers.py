# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from openerp.addons.survey.controllers import main
from openerp import SUPERUSER_ID
import json
import logging


class Tea(http.Controller):
    @http.route('/2_tea/2_tea/menu', auth='public', cors='*')
    def menu(self, **kw):
        cr, uid, context = request.cr, request.uid, request.context
        tea_food = request.registry['tea.food']
        tea_food_type = request.registry['tea.food.type']

        foods = tea_food.search_read(cr, SUPERUSER_ID, [])
        food_types = tea_food_type.search_read(cr, SUPERUSER_ID, [])
        return json.dumps({"food_types": food_types, "foods": foods})

    @http.route('/2_tea/2_tea/order', auth='public', cors='*', csrf=False, methods=['POST'])
    def order(self, **kw):
      cr, uid, context = request.cr, request.uid, request.context
      tea_order = request.registry['tea.order']
      tea_order_mon = request.registry['tea.order.mon']
      post_data = json.load(request.httprequest.stream)
      vals = {}
      vals['price'] = post_data.get('sum', 0)
      vals['is_thanh_toan'] = True
      mon_an = []
      for item in post_data.get('foods', False):
        mon_them = False
        if item.get('topping', False):
          mon_them = []
          for topping in item.get('topping'):
            mon_them.append((4, topping.get('id', False)))
        size = False
        if item.get('size', False) and item.get('size') == 'L':
          size = 2
        else:
          size = 1
        mon_an.append((0, 0, {'is_thanh_toan': True,
                              'size': size,
                              'status': 3,
                              'mon_an': item.get('food', False).get('id', False),
                              'mon_them': mon_them,
                              'price': item.get('price', False),
                              'sl': item.get('sl', False)
                              }))
      vals['mon_an'] = mon_an
      rs = tea_order.create(cr, SUPERUSER_ID, vals)
      return json.dumps({'id': rs})
