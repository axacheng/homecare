import jinja2
import json
import logging
import os
import webapp2

from google.appengine.api import channel


class IssueChannelAPIToken(webapp2.RequestHandler):
  def get(self, rpi_id):
      token = channel.create_channel(rpi_id)
      self.response.headers['Content-Type'] = 'application/json'
      self.response.out.write(json.dumps({'token': token}))


class MainPage(webapp2.RequestHandler):
  def get(self):
    pass
      # token = channel.create_channel('axa')
      # template_values = {'token': token}
      # template = jinja_environment.get_template('index.html')
      # self.response.out.write(template.render(template_values))


class SendMessage(webapp2.RequestHandler):
  def get(self, rpi_id, gear_type, action, gpio_pin):
    logging.info('Sending message for mobile...')
    channel.send_message(rpi_id, json.dumps({'gear_type':gear_type,
                                             'action':action,
                                             'gpio_pin':gpio_pin}))
    #channel.send_message('axa', 'this is my first test')


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/issue_channel_api_token/(.*)', IssueChannelAPIToken),
                               ('/send_message/(.*)/(.*)/(.*)/(.*)', SendMessage)
                              ],
                              debug=True)
