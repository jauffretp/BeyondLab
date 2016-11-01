# -*- coding: utf-8 -*-

from scrapy.exceptions import IgnoreRequest
from scrapoxy.commander import Commander

import logging
import random
import time

logger = logging.getLogger(__name__)

class BlacklistDownloaderMiddleware(object):

    def __init__(self, crawler):
        """Access the settings of the crawler to connect to Scrapoxy.
        """
        self._commander = Commander(
            crawler.settings.get('API_SCRAPOXY'),
            crawler.settings.get('API_SCRAPOXY_PASSWORD')
        )

    @classmethod
    def from_crawler(cls, crawler):
        """Call constructor with crawler parameters
        """
        return cls(crawler)


    def process_response(self, request, response, spider):
        """Detect blacklisted response and stop the instance if necessary.
        """
        if response.status != 429:
            # No blacklisted response is detected
            print "NO 429!"
            return response

        print "GOT 429!"
        # Find the instance name
        name = response.headers.get(u'x-cache-proxyname')
        if not name:
            logger.error(u'Cannot find instance name in headers')
            raise IgnoreRequest()

        # Stop the instance
        alive = self._commander.stop_instance(name)
        if alive < 0:
            logger.error(u'Remove: cannot find instance %s', name)
        elif alive == 0:
            logger.warn(u'Remove: instance removed (no instance remaining)')
        else:
            logger.debug(u'Remove: instance removed (%d instances remaining)', alive)

        # Sleep to avoid overhead on other instances
        delay = random.randrange(90, 180)
        logger.info(u'Sleeping %d seconds', delay)
        time.sleep(delay)

        raise IgnoreRequest()

