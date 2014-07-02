#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
import config
import logging

from lib.gcm import *
from lib.tmlapn import *

from models import store
from models import user


def SendMobileMessage(**kwargs):
  ### 發送 APN/GCM
  mobile_type, mobile_id = user.User.QueryUserMobileTypeAndMobileIdByUserId(user_id)
  message_type = kwargs.get('message_type')

  ##### IOS #####
  if mobile_type == 'ios' and mobile_id:
    apn_populate_data = {}

    if message_type == 'temperature':
      subject = kwargs.get('subject')
      apn_populate_data['message'] = u'\u270C'+ subject
      apn_populate_data['badge'] = '1'

    if message_type == 'emergency':
      pass

    if message_type == 'notification':
      pass

    payload = {'aps':{'alert':apn_populate_data.get('message'),
                      'badge':apn_populate_data.get('badge')}}
    SendAPN(mobile_id, payload)


  ##### Android #####
  elif mobile_type == 'android' and mobile_id:
    gcm_populate_data = {}

    if message_type == 'temperature'
      subject = kwargs.get('subject')
      gcm_populate_data['message'] = u'\u270C'+ subject
      gcm_populate_data['title'] = '緊急事件'
      gcm_populate_data['msgcnt'] = '1'

    if message_type == 'emergency':
      pass

    if message_type == 'notification':
      pass

    # Sending message without having send_to_boss flag in gcm_populate_data.
    else:
      gcm = GCM(config.API_KEY)      
      gcm.send(JSONMessage([mobile_id], gcm_populate_data))


        