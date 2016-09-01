#!/usr/bin/env python
import logging
from webapp2_extras import routes
# import os
import json
import webapp2

from google.appengine.api import urlfetch
from config import API_SERVER_HOSTNAME


class GetAddressTokenBalance(webapp2.RequestHandler):

    def get(self):
        self.response.headers["Content-Type"] = "application/json"
        address = self.request.get("address", "")
        if address == "":
            self.response.write(json.dumps({"success": False, "message": "MISSING_PARAMETER"}))
            return

        if len(address) != 42:
            self.response.write(json.dumps({"success": False, "message": "INVALID_ADDRESS"}))
            return

        url = "http://" + API_SERVER_HOSTNAME + ":5050/api/balanceOf?address=" + address
        logging.info("url => " + url)

        try:
            urlfetch.set_default_fetch_deadline(30)
            response = urlfetch.fetch(
                url=url,
                method=urlfetch.GET,
                headers={'Accept': 'application/json'}
            )

            self.response.write(response.content)

        except:
            logging.warning("urlfetch failure")
            self.response.write(json.dumps({"success": False, "message": "SERVER_ERROR"}))
        #





class NotFoundApiHandler(webapp2.RequestHandler):
    def get(self):
        self.response.status = 404
        self.response.headers["Content-Type"] = "application/json"
        self.response.out.write(json.dumps({"status": "failed", "message": "NOT_FOUND"}))




app = webapp2.WSGIApplication([
    routes.PathPrefixRoute('/api', [
        webapp2.Route('/balanceOf', GetAddressTokenBalance),
    ]),
    ('/.*', NotFoundApiHandler),
], debug=True)

