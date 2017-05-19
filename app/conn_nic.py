import socket, ssl, struct, json
from commands import Command


class ConnNic:
  def __init__(self, domain, action):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(60)
    sock = ssl.wrap_socket(sock, keyfile="/home/bitnami/flask-epp/app/occasio.key", certfile="/home/bitnami/flask-epp/app/cacert.pem", server_side=False, cert_reqs=ssl.CERT_REQUIRED,
                           ca_certs="/home/bitnami/occasio/python2713/lib/python2.7/site-packages/certifi/cacert.pem")

    try:
      sock.connect(('ote.nic.io', 700))
      sock.recv().decode("latin1")

      self.command = Command(domain, action, sock)
      self.command.login()

      perform = {
        'create' : self.command.createDomain,
        'backorder' : self.command.backorder,
      }

      if action in perform:
        perform[action]()

    finally:
      sock.close()