#!/usr/bin/env python

import logging
import traceback
import webapp2

from config import API_SERVER_HOSTNAME

from webapp2_extras import routes

from google.appengine.api import urlfetch



class UpdateIcoDataCronHandler(webapp2.RequestHandler):
    def get(self):

        url = "http://" + API_SERVER_HOSTNAME + ":5050/api/record"
        logging.info("url => " + url)

        try:
            urlfetch.set_default_fetch_deadline(50)

            result = urlfetch.fetch(
                url=url,
                method=urlfetch.GET,
                headers={'Accept': 'application/json'}
            )

        except:
            stacktrace = traceback.format_exc()
            logging.error("urlfetch URL failure \n\n%s", stacktrace)

            return

        if result.content == "Done":
            self.response.write("Done")
        else:
            logging.info(result.content)
            self.response.write("Error")


app = webapp2.WSGIApplication([
    routes.PathPrefixRoute('/cron', [
        webapp2.Route('/getUpdate', UpdateIcoDataCronHandler),
    ]),
], debug=True)
1
