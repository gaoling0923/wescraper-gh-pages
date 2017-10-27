# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os.path
import subprocess
import sys

import tornado.web as tw
from tornado.ioloop import IOLoop

import wescraper.config

directory = os.path.dirname(os.path.realpath(sys.argv[0]))
scraper = os.path.join(directory, 'scraper.py')


class WeHandler(tw.RequestHandler):
    def get(self, s):
        key_type, accounts = s.split(u'/')[0], s.split(u'/')[1:]
        print('Dealing request with', key_type, accounts)
        if key_type in wescraper.config.types and accounts:
            p = subprocess.Popen(
                ['python', scraper, key_type] + map(lambda x: x.encode('utf-8'), accounts),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            out, err = p.communicate()
            print(str(err))
            self.write(out)
        else:
            self.write('Change url to http://host/type/key1/key2 to search.\n')
            self.write('For example, these urls are valid:\n')
            for t in wescraper.config.types:
                self.write('http://host/{}/liriansu\n'.format(t))


app = tw.Application([
    (r'/(favicon.ico)', tw.StaticFileHandler, {'path': ''}),
    (r'/(.*)', WeHandler)
])
app.listen(wescraper.config.tornado_port)
print('Server is up on port {} now.'.format(wescraper.config.tornado_port))
IOLoop.current().start()
