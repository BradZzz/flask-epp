import socket, ssl, struct, json
from commands import Command


class ConnNic:
  def __init__(self, domain, action):

    self.init = {
      domain : domain,
      action : action,
    }

    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.settimeout(60)
    self.sock = ssl.wrap_socket(sock, keyfile="/home/bitnami/flask-epp/app/occasio.key", certfile="/home/bitnami/flask-epp/app/cacert.pem", server_side=False, cert_reqs=ssl.CERT_REQUIRED,
                           ca_certs="/home/bitnami/occasio/python2713/lib/python2.7/site-packages/certifi/cacert.pem")

  def perform(self):
    try:
      empty = { "received" : self.receive() }
      self.sock.connect(('ote.nic.io', 700))
      self.sock.recv().decode("latin1")

      self.command = Command(self.domain, self.action, self.sock)
      self.command.login()

      perform = {
        'create' : self.command.createDomain,
        'backorder' : self.command.backorder,
      }

      if self.action in perform:
        empty = perform[self.action]()

    finally:
      self.sock.close()

    return json.dumps(empty)