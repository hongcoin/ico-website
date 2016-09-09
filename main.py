#!/usr/bin/env python
from datetime import datetime
import logging
import MySQLdb
import os
import webapp2
from google.appengine.ext.webapp import template
from config import MYSQL_DB_CONFIG_APP_ENGINE
from config import MYSQL_DB_CONFIG_LOCALHOST


if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
    _db_config = MYSQL_DB_CONFIG_APP_ENGINE
else:
    _db_config = MYSQL_DB_CONFIG_LOCALHOST


def totimestamp(dt, epoch=datetime(1970, 1, 1)):
    td = dt - epoch
    return td.total_seconds()


class MainHandler(webapp2.RequestHandler):
    def get(self):
        env = os.getenv('SERVER_SOFTWARE')
        if (env and env.startswith('Google App Engine/')):
            # Connecting from App Engine
            db = MySQLdb.connect(
                db=_db_config["database"],
                unix_socket='/cloudsql/berry-cloud-project:us-central1:hongcoin-prod',
                user='root')

        else:
            # Connecting from an external network.
            # Make sure your network is whitelisted
            db = MySQLdb.connect(
                db=_db_config["database"],
                host=_db_config["host"],
                port=_db_config["port"],
                user=_db_config["user"],
                passwd=_db_config["password"]
            )


        cursor = db.cursor()
        cursor.execute('SELECT * FROM `ico_data` ORDER BY `record_datetime` DESC LIMIT 1')

        for r in cursor.fetchall():
            # logging.info('{}\n'.format(r))

            # result = r
            update_datetime = r[1]
            total_ether = r[2]
            current_tier = r[6]
            tokens_current_tier = r[7]
            total_tokens_sold = r[8]

        # process result values
        # display in UI

        template_values = {
            "update_datetime": update_datetime,
            "total_ether": total_ether,
            "total_tokens_sold": total_tokens_sold,
            "total_tokens_price": 1 + (5 * current_tier) / 100.0,
            "tokens_current_tier": tokens_current_tier,
        }

        path = os.path.join(os.path.dirname(__file__), 'template/home.html')
        self.response.out.write(template.render(path, template_values))



class TeamProfileHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'template/team.html')
        self.response.out.write(template.render(path, template_values))


class StatsHandler(webapp2.RequestHandler):
    def get(self):
        env = os.getenv('SERVER_SOFTWARE')
        if (env and env.startswith('Google App Engine/')):
            # Connecting from App Engine
            db = MySQLdb.connect(
                db=_db_config["database"],
                unix_socket='/cloudsql/berry-cloud-project:us-central1:hongcoin-prod',
                user='root')

        else:
            # Connecting from an external network.
            # Make sure your network is whitelisted
            db = MySQLdb.connect(
                db=_db_config["database"],
                host=_db_config["host"],
                port=_db_config["port"],
                user=_db_config["user"],
                passwd=_db_config["password"]
            )

        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM `ico_data` WHERE "
            " `record_datetime` >= NOW() - INTERVAL 1 DAY "
            "AND ((`record_datetime` like '%:00:%') or (`record_datetime` like '%:30:%')) ;")

        result = []
        for r in cursor.fetchall():
            result.append({
                "time": totimestamp(r[1]) * 1000,
                "ether": r[2],
                "current_tier_remaining": r[7],
                "tokens_issued": r[8]
            })
            # logging.info('{}'.format(r))

        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM `ico_data` WHERE "
            " `record_datetime` >= NOW() - INTERVAL 7 DAY "
            "AND `record_datetime` like '%:00:%' ;")

        result2 = []
        for r in cursor.fetchall():
            result2.append({
                "time": totimestamp(r[1]) * 1000,
                "ether": r[2],
                "current_tier_remaining": r[7],
                "tokens_issued": r[8]
            })
            # logging.info('{}'.format(r))


        template_values = {
            "result": result,
            "result2": result2
        }

        path = os.path.join(os.path.dirname(__file__), 'template/stats.html')
        self.response.out.write(template.render(path, template_values))


class HowItWorksHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect("/")


class FAQHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'template/faq.html')
        self.response.out.write(template.render(path, template_values))


class ContractViewerHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'template/contract.html')
        self.response.out.write(template.render(path, template_values))


class LetsEncryptHandler(webapp2.RequestHandler):

    def get(self, challenge):
        self.response.headers['Content-Type'] = 'text/plain'
        responses = {
            'PZTXvEQPtQGGzSO8u64TpXDPPgxZ9IhwyQLFNmFC67c':
                'PZTXvEQPtQGGzSO8u64TpXDPPgxZ9IhwyQLFNmFC67c.RsigBj-ozOspGpgMnUBw2IA5cIM3br3oVEkTd5I20CA',
            'qXJL_GKT4WdR75QOLZIjQ8sVGPlaBykTRDwBxhRJ2H8':
                'qXJL_GKT4WdR75QOLZIjQ8sVGPlaBykTRDwBxhRJ2H8.RsigBj-ozOspGpgMnUBw2IA5cIM3br3oVEkTd5I20CA'
        }
        self.response.write(responses.get(challenge, ''))


class NotFoundPageHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("NotFoundPageHandler triggered from " + os.path.basename(__file__))
        self.error(404)
        template_values = {}

        path = os.path.join(os.path.dirname(__file__), 'template/404.html')
        self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/team', TeamProfileHandler),
    ('/stats', StatsHandler),
    ('/faq', FAQHandler),
    ('/how-it-works', HowItWorksHandler),
    ('/contract', ContractViewerHandler),
    ('/.well-known/acme-challenge/([\w-]+)', LetsEncryptHandler),
    ('/.*', NotFoundPageHandler),
], debug=True)

