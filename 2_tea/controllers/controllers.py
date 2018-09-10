# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from openerp.addons.survey.controllers import main
from openerp import SUPERUSER_ID
import json
import logging
import random
import win32ui
import datetime


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


    @http.route('/2_tea/2_tea/print_bill', auth='public', cors='*', csrf=False, methods=['POST'])
    def print_bill(self, **kw):
      post_data = json.load(request.httprequest.stream)
      try:
        print_bill(post_data)
      except:
        print "This is an error message!"
      return json.dumps({'id': 'OK'})


    @http.route('/2_tea/2_tea/print_tem', auth='public', cors='*', csrf=False, methods=['POST'])
    def print_tem(self, **kw):
      post_data = json.load(request.httprequest.stream)
      n = 0
      sum_sl = 0
      for i, item in post_data.get('foods', False):
        sum_sl += item.get('sl',1)
      for i, item in post_data.get('foods', False):
        for j in range(0, item.get('sl',1)):
          n += 1
          try:
            print_mon_an(item, "(%s/%s)" % (n, sum_sl), post_data.get('uuid', 0))
          except:
            print "This is an error message!"
      return json.dumps({'id': 'OK'})


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
  hDC.TextOut(60, 0, "Tra Sua HiTea")
  Y += 60
  hDC.SelectObject(font_normal)
  hDC.TextOut(0, Y, "HD:" + str(order.get("uuid", 0)))
  hDC.TextOut(200, Y, "Ngay:" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
  Y += 30
  hDC.SelectObject(font_h2)
  hDC.TextOut(0, Y, "Mon")
  hDC.TextOut(330, Y, str("Size"))
  hDC.TextOut(410, Y, str("SL"))
  hDC.TextOut(490, Y, str("Gia"))
  Y += 40
  hDC.SelectObject(font_normal)
  for item in order.get('foods', False):
    p = 0
    if len(item.get('food', False).name_print) > 20:
      chars = item.get('food', False).get('name_print', "").split(" ")
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
      hDC.TextOut(0, Y, item.get('food', False).get('name_print', ""))

    hDC.TextOut(360, Y, item.get('size', False))
    hDC.TextOut(415, Y, str(item.get('sl', False)))
    hDC.TextOut(450, Y, item.get('price', False))
    Y += 40
    for topping in item.get('topping'):
      p = 0
      if len(topping.get('name_print')) > 20:
        chars = topping.get('name_print').split(" ")
        lines = []
        line = []
        n = 0
        for char in chars:
          n += len(char)
          if n > 15:
            hDC.TextOut(20, Y + p * 20, " ".join(line))
            p += 1
            line = []
            n = 0
          else:
            line.append(char)
        if n > 0:
          hDC.TextOut(20, Y + p * 20, " ".join(line))

      else:
        hDC.TextOut(0, Y, topping.get('name_print'))
      hDC.TextOut(415, Y, str(item.get('sl', False)))
      hDC.TextOut(450, Y, topping.get('price', False))
      Y += 40

  hDC.TextOut(0, Y, "                      --------------")
  Y += 20
  hDC.SelectObject(font_h2)
  hDC.TextOut(0, Y, "Tong cong:")
  hDC.TextOut(450, Y, str(order.get('sum')))
  Y += 30
  hDC.TextOut(0, Y, "Tien mat:")
  hDC.TextOut(450, Y, str(order.get('khach_dua')))
  Y += 30
  hDC.TextOut(0, Y, "Thoi lai:")
  hDC.TextOut(450, Y, str(order.get('thoi')))
  Y += 30
  hDC.TextOut(0, Y, "====================================")
  Y += 30
  hDC.SelectObject(font_h2)
  hDC.TextOut(0, Y, "*******CHUC QUY KHACH VUI VE*****")

  hDC.EndPage()
  hDC.EndDoc()


def print_mon_an(mon_an, note, order_id):
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
  hDC.SelectObject(font_normal)
  hDC.TextOut(50, Y, "Ma: " + str(order_id))
  Y += 20
  hDC.SelectObject(font_h2)
  p = 0
  if len(mon_an.get('food').get('name_print')) > 20:
    chars = mon_an.get('food').get('name_print').split(" ")
    lines = []
    line = []
    n = 0
    for char in chars:
      n += len(char)
      if n > 40:
        hDC.TextOut(30, Y + p * 30, " ".join(line))
        p += 1
        line = []
        n = 0
      else:
        line.append(char)
    if n > 0:
      hDC.TextOut(30, Y + p * 30, " ".join(line))

  else:
    hDC.TextOut(30, Y, mon_an.get('food').get('name_print'))
  Y += 30 + p * 20

  hDC.TextOut(50, Y + 20, "Size:")
  hDC.SelectObject(font_h1)
  hDC.TextOut(150, Y, mon_an.get('size'))
  hDC.SelectObject(font_h2)
  hDC.TextOut(200, Y + 20, note)
  Y += 50
  hDC.SelectObject(font_normal)
  hDC.TextOut(0, Y, "======================")
  Y += 20
  for topping in mon_an.get('topping'):
    hDC.TextOut(30, Y, topping.get('name_print'))
    Y += 10
  hDC.SelectObject(font_normal)
  hDC.EndPage()
  hDC.EndDoc()
