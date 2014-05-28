#!/usr/bin/python

import endpoints

from model import temperature
from protorpc import messages
from protorpc import message_types
from protorpc import remote


class TemperatureMessageRequest(messages.Message):
  ctime = message_types.DateTimeField(1)
  current_temperature = messages.StringField(2, required=True)
  user_id = messages.StringField(3, required=True)


class TemperatureMessageResponse(messages.Message):
  errmsg = messages.StringField(1)
  items = messages.MessageField(TemperatureMessageRequest, 2, repeated=True)
  status = messages.StringField(3)


@endpoints.api(name='homecare', version='v1', description='RPI Endpoints API')
class HomeCareApi(remote.Service):
  @endpoints.method(TemperatureMessageRequest,
                    TemperatureMessageResponse,
                    name='temperature',
                    path='addTemperature',
                    http_method='POST')


  def AddTemperature(self, request):
    populate_data = {}
    populate_data['current_temperature'] = request.current_temperature
    populate_data['user_id'] = '1'
    result = temperature.Temperature.AddTemperature(populate_data).get()

    def message_result():
      yield TemperatureMessageRequest(current_temperature=result.current_temperature,
                                      user_id=result.user_id)

    _message_result = list(message_result())

    return TemperatureMessageResponse(items=_message_result,
                                      status='ok', errmsg='')


application = endpoints.api_server([HomeCareApi])
