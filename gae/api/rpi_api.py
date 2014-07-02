#!/usr/bin/python

import datetime
import endpoints
import logging
import RPi.GPIO as GPIO


from model import temperature
from protorpc import messages
from protorpc import message_types
from protorpc import remote


class TemperatureMessageRequest(messages.Message):
  ctime = message_types.DateTimeField(1)
  current_temperature = messages.StringField(2)
  user_id = messages.StringField(3, required=True)


class TemperatureMessageResponse(messages.Message):
  errmsg = messages.StringField(1)
  items = messages.MessageField(TemperatureMessageRequest, 2, repeated=True)
  status = messages.StringField(3)


class LightMessageRequest(messages.Message):
  pin = message_types.DateTimeField(1)
  action = messages.StringField(2)

class LightMessageResponse(messages.Message):
  errmsg = messages.StringField(1)
  items = messages.MessageField(LightMessageRequest, 2, repeated=True)
  status = messages.StringField(3)

@endpoints.api(name='homecare', version='v1', description='RPI Endpoints API')
class HomeCareApi(remote.Service):

  @endpoints.method(LightMessageRequest,
                    LightMessageResponse,
                    name='control lighting',
                    path='controlLighting',
                    http_method='GET')
  def controlLighting(self, request):
    populate_data = {}
    populate_data['pin'] = request.pin
    populate_data['action'] = request.action

    ### Setup GPIO-0(aka:pin 11)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(populate_data.get('pin'), GPIO.OUT)
    
    if populate_data.get('action') == 'on':
      GPIO.output(11, GPIO.HIGH)

    elif populate_data.get('action') == 'off':
      GPIO.output(11, GPIO.LOW)

    return LightMessageResponse(items=[LightMessageRequest(pin='', action='')],
                                      status='ok', errmsg='')


  @endpoints.method(TemperatureMessageRequest,
                    TemperatureMessageResponse,
                    name='add temperature',
                    path='addTemperature',
                    http_method='POST')
  def AddTemperature(self, request):
    populate_data = {}
    populate_data['current_temperature'] = request.current_temperature
    populate_data['user_id'] = request.user_id
    result = temperature.Temperature.AddTemperature(populate_data).get()

    def message_result():
      yield TemperatureMessageRequest(current_temperature=result.current_temperature,
                                      user_id=result.user_id)

    _message_result = list(message_result())

    return TemperatureMessageResponse(items=_message_result,
                                      status='ok', errmsg='')


  @endpoints.method(TemperatureMessageRequest, TemperatureMessageResponse,
    name='query temperature',
    path='queryTemperature',
    http_method='GET')
  def QueryTemperature(self, request):
    populate_data = {}
    populate_data['user_id'] = request.user_id
    entities = temperature.Temperature.QueryCurrentTemperature(populate_data)
    
    if entities:
      def message_result():
        for entity in entities:
          #asia_taipei_time = datetime.datetime.strptime(entity.ctime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=8.0)
          asia_taipei_time = entity.ctime + datetime.timedelta(hours=8.0)

          yield TemperatureMessageRequest(ctime=asia_taipei_time,
                                          current_temperature=entity.current_temperature,
                                          user_id=entity.user_id)

      return TemperatureMessageResponse(items=list(message_result()),
                                        status='ok', errmsg='')
    else:
      return TemperatureMessageResponse(status='ok', errmsg='Can not find current temperature...')  



application = endpoints.api_server([HomeCareApi])
