#!/usr/bin/env python
# -*- coding: utf-8 -*-
### Python build-in library
import jinja2
import collections
import datetime
import logging
import webapp2

### 我們自己寫的 library
from lib.gcm import *
from lib.tmlapn import *
from lib import redhare

from model import temperature

### GAE自己的 或其他3nd party的library
from pytz.gae import pytz
from google.appengine.ext import ndb


jinja2_env = jinja2.Environment()
jinja2_env.globals.update(zip=zip)
        

class AddCaseUserMessageHistory(webapp2.RequestHandler):
  def post(self):
    current_temperature = self.request.get('current_temperature')
    redhare_message_type = 'temperature'
    sensor_location = self.request.get('sensor_location')
    subject = u'溫度過高警報'
    user_id = self.request.get('user_id')
    tz = pytz.timezone('Asia/Taipei')

    if int(current_temperature) >= 60:
      format_body = """"""
      populate_data = {}
      populate_data['ctime'] = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M")
      populate_data['current_temperature'] = current_temperature
      populate_data['sensor_location'] = sensor_location

      format_body = jinja2_env.from_string(
        u"""
        在 {{ sensor_location}} 溫度是 {{ current_temperature }}
        已經超過安全標準！請儘速的檢查。

        訊息接收時間： {{ ctime }}
        """.replace("        ", "")
        ).render(populate_data)


    redhare.SendMobileMessage(user_id,
                              message_type=redhare_message_type,
                              **{'subject': subject,
                                 'store_id': store_id})


# class AddCancelBuyUserMessageHistory(webapp2.RequestHandler):
#   def post(self):
#     tz = pytz.timezone('Asia/Taipei')
#     buy_type = self.request.get('buy_type')
#     format_body = """"""

#     if buy_type == config.BUY_TYPE[0]:  # togo
#       price = self.request.get('price')
#       product = json.loads(self.request.get('product')) #string to json object
#       product_name = product.get('product_name')
#       product_unit = product.get('product_unit')
#       status = self.request.get('status')
#       store_id = self.request.get('store_id')
#       store_name = self.request.get('store_name')
#       togo_id = self.request.get('togo_id')
#       user_id = self.request.get('user_id')
#       user_notes = self.request.get('user_notes')
#       redhare_message_type = config.BUY_TYPE[0]
#       subject = u'外帶取消編號:%s' % (togo_id)
#       case_id = togo_id

#       populate_data = {}
#       populate_data['ctime'] = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M")
#       populate_data['price'] = price
#       populate_data['product_name'] = product_name
#       populate_data['product_unit'] = product_unit
#       populate_data['reason'] = config.BUY_CANCEL_REASON.get(self.request.get('value'))
#       populate_data['store_name'] = store_name
#       populate_data['user_notes'] = user_notes

#       format_body = jinja2_env.from_string(
#         u"""
#         我們很遺憾，你在:
#         {{ store_name }}的外帶訂單已經取消。
#         取消原因：{{ reason }}

#         以下是取消的外帶訂單明細：

#         {% for item_name, item_unit in zip(product_name, product_unit) %}
#           {{ item_name }}  x  {{ item_unit }}
#         {% endfor %}
        
#         總價：{{ price }} 元

#         備註：{{ user_notes }}


#         ＊ 若需要修改或有任何問題，歡迎來電 ＊
#         訊息接收時間：{{ ctime }}
#         """.replace("        ", "")
#         ).render(populate_data)

#     elif buy_type == config.BUY_TYPE[1]:  # delivery
#       price = self.request.get('price')
#       product = json.loads(self.request.get('product')) #string to json object
#       product_name = product.get('product_name')
#       product_unit = product.get('product_unit')
#       status = self.request.get('status')
#       store_id = self.request.get('store_id')
#       store_name = self.request.get('store_name')
#       delivery_id = self.request.get('delivery_id')
#       user_id = self.request.get('user_id')
#       user_notes = self.request.get('user_notes')
#       redhare_message_type = config.BUY_TYPE[1]
#       case_id = delivery_id
#       subject = u'外送取消編號:%s' % (delivery_id)

#       populate_data = {}
#       populate_data['ctime'] = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M")
#       populate_data['price'] = price
#       populate_data['product_name'] = product_name
#       populate_data['product_unit'] = product_unit
#       populate_data['reason'] = config.BUY_CANCEL_REASON.get(self.request.get('value'))
#       populate_data['store_name'] = store_name
#       populate_data['user_notes'] = user_notes

#       format_body = jinja2_env.from_string(
#         u"""
#         我們很遺憾，你在:
#         {{ store_name}}的外送訂單已經取消。
#         取消原因：{{ reason }}

#         以下是取消的外送訂單明細：

#         {% for item_name, item_unit in zip(product_name, product_unit) %}
#           {{ item_name }}  x  {{ item_unit }}
#         {% endfor %}
        
#         總價：{{ price }} 元

#         備註：{{ user_notes }}


#         ＊ 若需要修改或有任何問題，歡迎來電 ＊
#         訊息接收時間：{{ ctime }}
#         """.replace("        ", "")
#         ).render(populate_data)


#     # Save them to StoreMessageHistory
#     store_message = {}
#     store_message['body'] = format_body
#     store_message['image'] = ''
#     store_message['message_type'] = config.MESSAGE_TYPE_FOR_USERONLY
#     store_message['store_id'] = store_id
#     store_message['store_name'] = store_name
#     store_message['subject'] = subject
#     store_message_saved_result = history.StoreMessageHistory.AddPersonalMessageHistory(store_message)
#     store_message_id = store_message_saved_result.get().key.id()
#     store_message_urlsafe = store_message_saved_result.get().key.urlsafe()

#     # Save them to UserMessageHistory
#     user_message = {}
#     user_message['expire_date'] = config.DEFAULT_EXPIREATION_DATE_MESSAGE
#     user_message['store_id'] = store_id
#     user_message['store_name'] = store_name
#     user_message['store_message_id'] = store_message_id
#     user_message['store_message_urlsafe'] = store_message_urlsafe
#     history.UserMessageHistory.AddMessageHistory(user_message, [user_id])

#     redhare.SendMobileMessage(user_id,
#                               message_type=redhare_message_type,
#                               message_status=status,
#                               **{'store_name': store_name,
#                                  'case_id':case_id})


# class AddCancelCaseUserMessageHistory(webapp2.RequestHandler):
#   def post(self):
#     expect_date = self.request.get('expect_date')
#     expect_time = self.request.get('expect_time')
#     case_id = self.request.get('case_id')
#     case_type = self.request.get('case_type')
#     service = self.request.get('service')
#     people = self.request.get('people')
#     store_id = self.request.get('store_id')
#     store_name = self.request.get('store_name')
#     user_id = self.request.get('user_id')
#     user_notes = self.request.get('user_notes')
#     tz = pytz.timezone('Asia/Taipei')

#     format_body = """"""
#     populate_data = {}

#     if case_type == config.CASE_TYPE[0]:  # service
#       redhare_message_type = config.CASE_TYPE[0]
#       subject = u'預約取消編號:%s' % (case_id)

#       populate_data['case_id'] = case_id
#       populate_data['ctime'] = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M")
#       populate_data['expect_date'] = expect_date
#       populate_data['expect_time'] = expect_time
#       populate_data['service'] = service
#       populate_data['people'] = people
#       populate_data['reason'] = config.CASE_CANCEL_REASON.get(self.request.get('value'))
#       populate_data['store_name'] = store_name
#       populate_data['user_notes'] = user_notes

#       format_body = jinja2_env.from_string(
#         u"""
#         我們很遺憾，你在:
#         {{ store_name }}的預約已經取消。
#         取消原因：{{ reason }}

#         以下是取消的預約明細：

#         預約日期：{{ expect_date }}
#         預約時間：{{ expect_time }}
#         人數：{{ people }}
#         你預約的服務：{{ service }}


#         備註：{{ user_notes }}


#         ＊ 若需要修改或有任何問題，歡迎來電 ＊
#         訊息接收時間：{{ ctime }}
#         """.replace("        ", "")
#         ).render(populate_data)

#     elif case_type == config.CASE_TYPE[1]:  # table
#       redhare_message_type = config.CASE_TYPE[1]
#       subject = u'訂位取消編號:%s' % (case_id)

#       populate_data['case_id'] = case_id
#       populate_data['ctime'] = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M")
#       populate_data['expect_date'] = expect_date
#       populate_data['expect_time'] = expect_time
#       populate_data['people'] = people
#       populate_data['reason'] = config.CASE_CANCEL_REASON.get(self.request.get('value'))
#       populate_data['store_name'] = store_name
#       populate_data['user_notes'] = user_notes

#       format_body = jinja2_env.from_string(
#         u"""
#         我們很遺憾，你在:
#         {{ store_name }}的訂位已經取消。
#         取消原因：{{ reason }}

#         以下是取消的訂位明細：

#         訂位日期：{{ expect_date }}
#         訂位時間：{{ expect_time }}
#         人數：{{ people }}


#         備註：{{ user_notes }}
        

#         ＊ 若需要修改或有任何問題，歡迎來電 ＊
#         訊息接收時間：{{ ctime }}
#         """.replace("        ", "")
#         ).render(populate_data)

#     # Save them to StoreMessageHistory
#     store_message = {}
#     store_message['body'] = format_body
#     store_message['image'] = ''
#     store_message['message_type'] = config.MESSAGE_TYPE_FOR_USERONLY
#     store_message['store_id'] = store_id
#     store_message['store_name'] = store_name
#     store_message['subject'] = subject
#     store_message_saved_result = history.StoreMessageHistory.AddPersonalMessageHistory(store_message)
#     store_message_id = store_message_saved_result.get().key.id()
#     store_message_urlsafe = store_message_saved_result.get().key.urlsafe()

#     # Save them to UserMessageHistory
#     user_message = {}
#     user_message['expire_date'] = config.DEFAULT_EXPIREATION_DATE_MESSAGE
#     user_message['store_id'] = store_id
#     user_message['store_name'] = store_name
#     user_message['store_message_id'] = store_message_id
#     user_message['store_message_urlsafe'] = store_message_urlsafe

#     if user_id:
#       history.UserMessageHistory.AddMessageHistory(user_message, [user_id])
#       redhare.SendMobileMessage(user_id,
#                                 message_type=redhare_message_type,
#                                 message_status=config.CASE_STATUS[4], #cancel
#                                 **{'store_name': store_name,
#                                    'case_id':case_id})
#     else:
#       logging.info('User doesn\'t have user_id, so we will not send gcm/apn......')


# class AddDeliveryUserMessageHistory(webapp2.RequestHandler):
#   def post(self):
#     tz = pytz.timezone('Asia/Taipei')
#     delivery_id =  self.request.get('delivery_id')
#     price = self.request.get('price')
#     shipping_fee = self.request.get('shipping_fee')
#     product = json.loads(self.request.get('product')) #string to json object
#     store_id = self.request.get('store_id')
#     store_name = self.request.get('store_name')
#     user_id = self.request.get('user_id')
#     user_notes = self.request.get('user_notes')
#     product_name = product.get('product_name')
#     product_unit = product.get('product_unit')
#     subject = u'外送訂單編號:%s' % (delivery_id)
#     redhare_message_type = config.BUY_TYPE[1]
#     total_price = int(price) + int(shipping_fee)

#     populate_data = {}
#     populate_data['ctime'] = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M")
#     populate_data['store_name'] = store_name
#     populate_data['product_name'] = product_name
#     populate_data['product_unit'] = product_unit
#     populate_data['user_notes'] = user_notes
#     populate_data['price'] = price
#     populate_data['shipping_fee'] = shipping_fee
#     populate_data['total_price'] = total_price

#     format_body = jinja2_env.from_string(
#       u"""
#       你的外送訂單已經收到。
#       {{ store_name }}的工作人員將儘快為你安排外送。
#       我們會發訊通知你外送的狀態。
#       以下是你的外送商品明細：

#       {% for item_name, item_unit in zip(product_name, product_unit) %}
#         {{ item_name }}  x  {{ item_unit }}
#       {% endfor %}


#       運   費：{{ shipping_fee }}
#       商品價格：{{ price }}
#       結帳總價：{{ total_price }}

#       備註：{{ user_notes }}


#       ＊ 若需要修改或有任何問題，歡迎來電 ＊
#       訊息接收時間：{{ ctime }}
#       """.replace("      ", "")
#       ).render(populate_data)

#     # Save them to StoreMessageHistory
#     store_message = {}
#     store_message['body'] = format_body
#     store_message['image'] = ''
#     store_message['message_type'] = config.MESSAGE_TYPE_FOR_USERONLY
#     store_message['store_id'] = store_id
#     store_message['store_name'] = store_name
#     store_message['subject'] = subject
#     store_message_saved_result = history.StoreMessageHistory.AddPersonalMessageHistory(store_message)
#     store_message_id = store_message_saved_result.get().key.id()
#     store_message_urlsafe = store_message_saved_result.get().key.urlsafe()

#     # Save them to UserMessageHistory
#     user_message = {}
#     user_message['expire_date'] = config.DEFAULT_EXPIREATION_DATE_MESSAGE
#     user_message['store_id'] = store_id
#     user_message['store_name'] = store_name
#     user_message['store_message_id'] = store_message_id
#     user_message['store_message_urlsafe'] = store_message_urlsafe
#     history.UserMessageHistory.AddMessageHistory(user_message, [user_id])

#     redhare.SendMobileMessage(user_id,
#                               message_type=redhare_message_type,
#                               message_status=config.BUY_STATUS[0], #open
#                               **{'subject': subject,
#                                  'store_id': store_id})


# class AddToGoUserMessageHistory(webapp2.RequestHandler):
#   def post(self): # should run at most 1/s
#     eta = self.request.get('eta')
#     price = self.request.get('price')
#     product = json.loads(self.request.get('product')) #string to json object
#     product_name = product.get('product_name')
#     product_unit = product.get('product_unit')
#     redhare_message_type = config.BUY_TYPE[0]
#     store_id = self.request.get('store_id')
#     store_name = self.request.get('store_name')
#     togo_id = self.request.get('togo_id')
#     subject = u'外帶訂單編號:%s' % (togo_id)
#     tz = pytz.timezone('Asia/Taipei')
#     user_id = self.request.get('user_id')
#     user_notes = self.request.get('user_notes')

#     populate_data = {}
#     populate_data['eta'] = eta
#     populate_data['ctime'] = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M")
#     populate_data['store_name'] = store_name
#     populate_data['product_name'] = product_name
#     populate_data['product_unit'] = product_unit
#     populate_data['user_notes'] = user_notes
#     populate_data['price'] = price

#     format_body = jinja2_env.from_string(
#       u"""
#       你的外帶訂單已經收到。
#       {{ store_name }}的工作人員將儘快為你準備外帶。
#       我們會發訊通知你外帶的狀態。
#       以下是你的外帶商品明細：

#       {% for item_name, item_unit in zip(product_name, product_unit) %}
#         {{ item_name }}  x  {{ item_unit }}
#       {% endfor %}


#       總價：{{ price }}

#       預計來店時間：{{ eta }}

#       備註：{{ user_notes }}


#       ＊ 若需要修改或有任何問題，歡迎來電 ＊
#       訊息接收時間：{{ ctime }}
#       """.replace("      ", "")
#       ).render(populate_data)

#     # Save them to StoreMessageHistory
#     store_message = {}
#     store_message['body'] = format_body
#     store_message['image'] = ''
#     store_message['message_type'] = config.MESSAGE_TYPE_FOR_USERONLY
#     store_message['store_id'] = store_id
#     store_message['store_name'] = store_name
#     store_message['subject'] = subject
#     store_message_saved_result = history.StoreMessageHistory.AddPersonalMessageHistory(store_message)
#     store_message_id = store_message_saved_result.get().key.id()
#     store_message_urlsafe = store_message_saved_result.get().key.urlsafe()

#     # Save them to UserMessageHistory
#     user_message = {}
#     user_message['expire_date'] = config.DEFAULT_EXPIREATION_DATE_MESSAGE
#     user_message['store_id'] = store_id
#     user_message['store_name'] = store_name
#     user_message['store_message_id'] = store_message_id
#     user_message['store_message_urlsafe'] = store_message_urlsafe
#     history.UserMessageHistory.AddMessageHistory(user_message, [user_id])

#     redhare.SendMobileMessage(user_id,
#                               message_type=redhare_message_type,
#                               message_status=config.BUY_STATUS[0], #open
#                               **{'subject': subject,
#                                  'store_id': store_id})


# class ChartNewUser(webapp2.RequestHandler):
#   def post(self):
#     populate_data={}
#     populate_data['_from'] = self.request.get('_from')
#     populate_data['store_id'] = self.request.get('store_id')
#     populate_data['user_id'] = self.request.get('user_id')
#     chart.Chart.AddNewUser(populate_data)


# class SendFirstPromoMesg(webapp2.RequestHandler):
#   def post(self): # should run at most 1/s
#     store_id = self.request.get('store_id')
#     user_id = self.request.get('user_id')

#     ### Query Store Promotion Message
#     first_message = history.StoreMessageHistory.QueryFirstMessageHistory(store_id)

#     if first_message:
#       logging.info('Going to send first promotion message to:%s', user_id)
#       user_message = {}
#       for item in first_message:
#         # Save them to UserMessageHistory
#         user_message['expire_date'] = item.expire_date.strftime('%Y%m%d')
#         user_message['store_id'] = item.store_id
#         user_message['store_name'] = item.store_name
#         user_message['store_message_id'] = item.key.id()
#         user_message['store_message_urlsafe'] = item.key.urlsafe()
#         user_message['subject'] = item.subject

#       history.UserMessageHistory.AddMessageHistory(user_message, [user_id])
  	  
#       ### 發送 APN/GCM
#       mobile_type, mobile_id = user.User.QueryUserMobileTypeAndMobileIdByUserId(user_id)
#       if mobile_type == 'ios':
#         payload = {'aps':{'alert':u'%s' % (user_message.get('store_name')),
#                           'badge':'3'}}
#         SendAPN(''.join(mobile_id), payload)

#       elif mobile_type == 'android':
#         gcm = GCM(config.API_KEY)
#         populate_data = {'message':user_message.get('subject'),
#                          'title':user_message.get('store_name'),
#                          'msgcnt':'3'}
#         gcm.send(JSONMessage([mobile_id], populate_data))
    
#     else:
#       logging.warning('This store:%s doesnt have by_all message...Please create one for them...', store_id)


# class AddGiftQueue(BaseHandler):
#   def post(self): # should run at most 1/s
#     to_oauth_type = self.request.get('to_oauth_type')
#     to_oauth_uid  = self.request.get('to_oauth_uid')

#     populate_data = {}
#     populate_data['user_id'] = self.request.get('user_id')
#     populate_data['point'] = abs(int(self.request.get('point')))
#     populate_data['point_type'] = 'redeem'
#     populate_data['product'] = config.DEFAULT_GIFT_PRODUCT
#     populate_data['product_id'] = config.DEFAULT_GIFT_PRODUCT_ID

#     populate_data['store_id'] = self.request.get('store_id')
#     populate_data['store_name'] = self.request.get('store_name')
#     populate_data['to_oauth_uid'] = self.request.get('to_oauth_uid')
#     populate_data['to_oauth_type'] = self.request.get('to_oauth_type')
#     populate_data['oauth_uid'] = self.request.get('oauth_uid')  # For QueryGiftQueue used
#     populate_data['oauth_type'] = self.request.get('oauth_type')  # For QueryGiftQueue used

#     logging.warning(u'點數分享：Point:(%s)---From:(%s) To:(%s)',
#                     populate_data.get('point'),
#                     populate_data.get('user_id'),
#                     populate_data.get('to_oauth_uid'))
    
#     # # Welcome check.
#     # populate_data['_from'] = config.CHART_NEWUSER_FROM[2]
#     # point.Point.Wellcome(populate_data)

#     if to_oauth_type == 'facebook':
#       # 開始扣點
#       # From    
#       _subtract_result = point.Point.SubtractPoint(populate_data)
#       #history.PointHistory.AddPointHistory(populate_data)
    
#       facebook_user_entity = user.User.QueryUserByFacebookId(to_oauth_uid)
#       logging.info('facebook_user_entity:%s', facebook_user_entity)

#       for entity in _subtract_result:
#         populate_data['point'] = entity.get('point')
#         populate_data['point_type'] = 'redeem'
#         #populate_data['gift_owner'] = to_oauth_uid  # BUG?
#         populate_data['gift_owner'] = facebook_user_entity[0].user_id  # BUG?
#         populate_data['point_expire_date'] = entity.get('expire_date')
#         populate_data['expire_date'] = entity.get('expire_date') #this is for AddPointHistory

#         logging.info('Point subtracting to:%s', populate_data)
#         history.PointHistory.AddPointHistory(populate_data)
#         gift.GiftQueue.AddGiftQueue(populate_data)

#         populate_data['to_oauth_uid'] = facebook_user_entity[0].user_id
#         user.Friend.AddFriend(populate_data)

#       # If the facebook to_oauth_uid is our existing user, then
#       # We can give the point straightforward to user right after done AddGiftQueue
#       if facebook_user_entity:
#         gift_result = gift.GiftQueue.QueryGiftQueue(populate_data)
#         logging.info('gift_result::::::::::::%s', gift_result)

#         if gift_result:
#           gift_data = {}
#           for item in gift_result:
#             # 開始加點
#             # To 
#             gift_data['difference'] =  item.point
#             gift_data['expire_date'] = item.point_expire_date
#             gift_data['gift_owner'] = self.request.get('user_id')
#             gift_data['issue_points'] =  item.point
#             gift_data['oauth_type'] =  'ggstore'  #(TODO) it'd be changed sometime when implementing other Oauth.
#             gift_data['point_type'] =  'sell'
#             gift_data['product'] = config.DEFAULT_GIFT_PRODUCT
#             gift_data['product_id'] = config.DEFAULT_GIFT_PRODUCT_ID
#             gift_data['store_id'] =  item.store_id
#             gift_data['store_name'] =  item.store_name
#             gift_data['user_id'] =  facebook_user_entity[0].user_id
#             gift_data['to_oauth_uid'] =  self.request.get('user_id')

#             # Welcome check.
#             gift_data['_from'] = config.CHART_NEWUSER_FROM[2]
#             point.Point.Wellcome(gift_data)

#             # Then, add gift point
#             point.Point.AddPoint(gift_data)
#             history.PointHistory.AddPointHistory(gift_data)
#             user.Friend.AddFriend(gift_data)

#           for i in gift_result:
#             i.used = True
#             i.put()

#           # ### 發送 APN/GCM
#           user_id = self.request.get('user_id')
#           store_name = self.request.get('store_name')
#           shared_point = self.request.get('point')

#           mobile_type, mobile_id = user.User.QueryUserMobileTypeAndMobileIdByUserId(user_id)
#           if mobile_type == 'ios' and mobile_id:
#             payload = {'aps':{'alert':u'你贈送了 %s的 %s點給你朋友' % (store_name, shared_point),
#                               'badge':'7'}}
#             SendAPN(''.join(mobile_id), payload)

#           elif mobile_type == 'android' and mobile_id:
#             title = u'你贈送了 %s的 %s點給你朋友' % (store_name, shared_point)
#             data = '請到"我的集點"查詳細資料吧...'
#             populate_data = {'message': data,
#                              'title':title,
#                              'msgcnt':'7'}
#             gcm = GCM(config.API_KEY)      
#             gcm.send(JSONMessage([mobile_id], populate_data))


#     elif to_oauth_type == 'ggstore':
#       # 開始扣點
#       # From
#       _subtract_result = point.Point.SubtractPoint(populate_data)
      
#       # 如果把下面的註解拿掉，當gift扣點時，就會直接顯示扣的點數
#       # 例如：扣100點而這100點來自20+50+30 的話，他在扣點的AddPointHistory就只會顯示
#       # 一筆 -100的點數而他們也不會有expire_date,因為我們不會知道這100點他們
#       # 20,50,30點數分別的expire_date
#       #history.PointHistory.AddPointHistory(populate_data)
#       #logging.info('From _subtract_result:%s', _subtract_result)
      
#       for entity in _subtract_result:
#         populate_data['gift_owner'] = to_oauth_uid
#         populate_data['user_id'] = self.request.get('user_id')
#         populate_data['point'] = entity.get('point')
#         populate_data['point_type'] = 'redeem'
#         populate_data['point_expire_date'] = entity.get('expire_date') # this is for AddGiftQueue
#         populate_data['expire_date'] = entity.get('expire_date') #this is for AddPointHistory
        
#         # 以下的AddPointHistory 是改良上面AddPointHistory註解的問題
#         # 我們把AddPointHistory放在這個forloop裡面後，就可以抓出所有要扣的點數他們分別的expire_date
#         # 然後一筆一筆寫入到AddPointHistory，以上面 -100的例子，他就會寫入3筆分別是
#         # 20,50,30這三個點數的expire_date到AddPointHistory 裡面去～
#         # 這樣會比較清楚debug, 但是可能會造成使用者的混淆～因為他們只知道要扣100點，而不會知道這
#         # 100點其實是來自20,50,30不同的點數來的....
#         #logging.info('Point subtracting to:%s', populate_data)
#         history.PointHistory.AddPointHistory(populate_data)
#         gift.GiftQueue.AddGiftQueue(populate_data)
#         user.Friend.AddFriend(populate_data)


#         # 開始加點
#         # To
#         populate_data['gift_owner'] = self.request.get('user_id')
#         populate_data['difference'] =  entity.get('point')
#         populate_data['expire_date'] = entity.get('expire_date')
#         populate_data['issue_points'] =  entity.get('point')
#         populate_data['point_type'] =  'sell'
#         populate_data['user_id'] =  self.request.get('to_oauth_uid')
#         populate_data['to_oauth_uid'] =  self.request.get('user_id')

#         # Welcome check.
#         populate_data['_from'] = config.CHART_NEWUSER_FROM[2]
#         point.Point.Wellcome(populate_data)
       
#         # Then, add point.
#         point.Point.AddPoint(populate_data)
#         history.PointHistory.AddPointHistory(populate_data)
#         user.Friend.AddFriend(populate_data)


#       ### 發送 APN/GCM
#       user_id = self.request.get('user_id')
#       store_name = self.request.get('store_name')
#       shared_point = self.request.get('point')

#       mobile_type, mobile_id = user.User.QueryUserMobileTypeAndMobileIdByUserId(user_id)
#       to_mobile_type, to_mobile_id = user.User.QueryUserMobileTypeAndMobileIdByUserId(self.request.get('to_oauth_uid'))
      
#       ### From
#       if mobile_type == 'ios' and mobile_id:
#         ### From APN
#         payload = {'aps':{'alert':u'你贈送了 %s的 %s點給你朋友' % (store_name, shared_point),
#                           'badge':'7'}}
#         SendAPN(''.join(mobile_id), payload)


#       elif mobile_type == 'android' and mobile_id and to_mobile_id:
#         ### From GCM
#         title = u'你贈送了 %s的 %s點給你朋友' % (store_name, shared_point)
#         data = '請到"我的集點"查詳細資料吧...'
#         populate_data = {'message': data,
#                          'title':title,
#                          'msgcnt':'7'}
#         gcm = GCM(config.API_KEY)      
#         gcm.send(JSONMessage([mobile_id], populate_data))


#       ### To
#       if to_mobile_type == 'android':
#         ### To Android GCM
#         to_user_name = user.User.QueryUserByParent(user_id).name
#         title = u'%s 贈送了 %s的 %s點給你' % (to_user_name, store_name, shared_point)
#         data = '請到"我的集點"查詳細資料吧...'
#         populate_data = {'message': data,
#                          'title':title,
#                          'msgcnt':'8'}
#         gcm = GCM(config.API_KEY)      
#         gcm.send(JSONMessage([to_mobile_id], populate_data))

#       elif to_mobile_type == 'ios':
#         ### To ios APN
#         to_user_name = user.User.QueryUserByParent(user_id).name
#         payload = {'aps':{'alert':u'%s 贈送了 %s的 %s點給你' %(to_user_name, store_name, shared_point),
#                           'badge':'8'}}
#         SendAPN(''.join(to_mobile_id), payload)


# class AddStore(BaseHandler):
#   def post(self):
#     redhare_message_type = config.POINT_ACTION[0]
#     redhare_message_status = None

#     _expire_date = self.request.get('expire_date')
#     expire_date = datetime.datetime.strptime(_expire_date, "%Y-%m-%d %H:%M:%S")

#     populate_data = {}
#     populate_data['difference'] = int(self.request.get('difference'))
#     populate_data['expire_date'] = expire_date
#     populate_data['issue_points'] = int(self.request.get('issue_points'))
#     populate_data['point_type'] = self.request.get('point_type')
#     populate_data['product'] = []
#     populate_data['product_id'] = []
#     populate_data['staff_id'] = self.request.get('staff_id')
#     populate_data['store_id'] = self.request.get('store_id')
#     populate_data['store_name'] = self.request.get('store_name')
#     populate_data['user_id'] = self.request.get('user_id')

#     # Welcome check.
#     populate_data['_from'] = config.CHART_NEWUSER_FROM[1]
#     point.Point.Wellcome(populate_data)

#     # Then, add zero(0) point to user.
#     result = point.Point.AddPoint(populate_data)

#     if result:
#       history.PointHistory.AddPointHistory(populate_data)
#       redhare.SendMobileMessage(self.request.get('user_id'),
#                                 message_type=redhare_message_type,
#                                 message_status=redhare_message_status,
#                                 **{'store_name': self.request.get('store_name')})


# class SendPromotionMessage(BaseHandler):
#   def post(self):
#     ### Get _user_ids generator to fetch user_ids
#     _user_ids = json.loads(self.request.get('_user_ids'))
#     expire_date = self.request.get('expire_date')
#     store_id = self.request.get('store_id')
#     store_name = self.request.get('store_name')
#     subject = self.request.get('subject')
#     store_message_id = self.request.get('store_message_id')
#     store_message_urlsafe = self.request.get('store_message_urlsafe')


#     ### Step1. Save them to UserMessageHistory
#     user_message = {}
#     user_message['expire_date'] = expire_date
#     user_message['store_id'] = store_id
#     user_message['store_name'] = store_name
#     user_message['store_message_id'] = store_message_id
#     user_message['store_message_urlsafe'] = store_message_urlsafe
#     history.UserMessageHistory.AddMessageHistory(user_message, _user_ids)


#     ### Step2. GCM/APN
#     def _mobile_type_with_mobile_id():
#       for user_id in _user_ids:
#         yield user.User.QueryUserMobileTypeAndMobileIdByUserId(user_id)

#     mobile_type_and_mobile_id = collections.defaultdict(list) #collections.defaultdict
#     for mobile_type, mobile_id in filter(None, list(_mobile_type_with_mobile_id())):
#       mobile_type_and_mobile_id[mobile_type].append(mobile_id)

#     #logging.info('mobile_type_and_mobile_id:%s', mobile_type_and_mobile_id)
#     for mobile_type, mobile_id in mobile_type_and_mobile_id.items():
#       if mobile_type == 'ios':
#         try:
#           #logging.info('Sending APN...:%s', mobile_id)
#           payload = {'aps':{'alert':u'%s' % (store_name),
#                             'badge':'3' }}
#           for m in mobile_id:
#             SendAPN(m, payload)

#           #SendAPN(''.join(mobile_id), payload)  # (TODO) need to loop mobile_ids list
#           # ios_success+=ios_success
#           # ios_success = 0
#           # ios_failed = 0
#           # ios_canonical = 0
#         except:
#           #raise
#           pass

#       elif mobile_type == 'android':
#         try:
#           #logging.info('Sending GCM...')
#           gcm = GCM(config.API_KEY)
#           populate_data = {'message':subject,
#                            'title':store_name,
#                            'msgcnt':'3'
#                           }
#           mobile_ids = [item for sublist in mobile_type_and_mobile_id.values() for item in sublist]
#           gcm_sent_result = gcm.send(JSONMessage(mobile_ids, populate_data))
#           # android_success = len(gcm_sent_result.success.keys())
#           # android_failed = len(gcm_sent_result.failed.keys())
#           # android_canonical = len(gcm_sent_result.canonical.keys())
#         except:
#           #raise
#           pass

