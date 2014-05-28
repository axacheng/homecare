# -*- coding: utf-8 -*-
import logging

from google.appengine.ext import ndb


class Temperature(ndb.Model):
  ctime = ndb.DateTimeProperty(auto_now_add=True)
  current_temperature = ndb.StringProperty()
  user_id = ndb.StringProperty()


  @classmethod
  def AddTemperature(cls, populate_data):
    current_temperature = populate_data.get('current_temperature')
    user_id = populate_data.get('user_id')

    return cls(current_temperature = current_temperature,
               parent = ndb.Key(cls, user_id),
               user_id = user_id).put()


  @classmethod
  def QueryCurrentTemperature(cls, populate_data):
    user_id = populate_data.get('user_id')
    temp_parent = ndb.Key(cls, user_id)
    return cls.query(ancestor=temp_parent).order(-cls.ctime).fetch(1)
