#!/usr/bin/python
import config
import json
import logging
import socket
import ssl
import struct


def SendAPN(mobile_id, payload):
  data = json.dumps(payload)
  logging.info('IOS mobile_id:%s', mobile_id)
  byteToken = mobile_id.replace(' ','').decode('hex')
  theFormat = '!BH32sH%ds' % len(data)
  theNotification = struct.pack(theFormat, 0, 32, byteToken, len(data), data)
  
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(config.APN_HOST)
  ssl_sock = ssl.wrap_socket(s, certfile=config.APN_PEM_FILE,
  							                server_side=False)
  ssl_sock.write(theNotification)
  ssl_sock.close()
