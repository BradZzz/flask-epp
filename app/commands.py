import struct, json
from env import STATICS

class Command:

  def __init__(self, domain, action, conn):
    self.conn = conn
    self.info = STATICS
    self.info["testDomain"] = domain
    self.info["testBackorder"]= domain

  def login(self):
    login_com = """
    <?xml version="1.0" encoding="UTF-8" standalone="no"?>
      <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
        <command>
          <login>
            <clID>""" + self.info['clID'] + """</clID>
            <pw>""" +self.info['pw'] + """</pw>
            <options>
              <version>1.0</version>
              <lang>en</lang>
            </options>
            <svcs>
              <objURI>urn:ietf:params:xml:ns:domain-1.0</objURI>
              <objURI>urn:ietf:params:xml:ns:contact-1.0</objURI>
              <objURI>urn:ietf:params:xml:ns:secDNS-1.1</objURI>
              <objURI>http://www.dir.org/xsd/account-1.0</objURI>
              <objURI>http://www.dir.org/xsd/future-1.0</objURI>
            </svcs>
          </login>
        <clTRID>""" + self.info['clTRID'] + """</clTRID>
        </command>
      </epp>
    """

    print json.dumps({ "sent" : login_com })
    self.send_(login_com)
    return json.dumps({ "received" : self.receive() })

  def hello(self):
    hello = """
    <?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
      <hello/>
    </epp>
    """

    print json.dumps({ "sent" : hello })
    self.send_(hello)
    return json.dumps({ "received" : self.receive() })

  def info(self):
    info = """
    <?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
      <command>
        <info>
          <domain:info
           xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
            <domain:name hosts="all">""" + self.info['infoDomain'] + """</domain:name>
          </domain:info>
        </info>
        <clTRID>""" + self.info['clTRID'] + """</clTRID>
      </command>
    </epp>
    """

    print json.dumps({ "sent" : info })
    self.send_(info)
    return json.dumps({ "received" : self.receive() })

  def createDomain(self):
    create = """
    <?xml version="1.0" encoding="UTF-8"?>
    <epp xmlns="urn:ietf:params:xml:ns:epp-1.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0
    epp-1.0.xsd">
      <command>
        <create>
          <domain:create xmlns:domain="urn:ietf:params:xml:ns:domain-1.0"
          xsi:schemaLocation="urn:ietf:params:xml:ns:domain-1.0
          domain-1.0.xsd">
            <domain:name>""" + self.info['testDomain'] + """</domain:name>
            <domain:period unit="y">""" + self.info['years'] + """</domain:period>
            <domain:ns>
              <domain:hostAttr>
                <domain:hostName>""" + self.info['ns1'] + """</domain:hostName>
              </domain:hostAttr>
              <domain:hostAttr>
                <domain:hostName>""" + self.info['ns2'] + """</domain:hostName>
              </domain:hostAttr>
            </domain:ns>
            <domain:registrant>""" + self.info['clID'] + """</domain:registrant>
            <domain:contact type="admin">""" + self.info['clID'] + """</domain:contact>
            <domain:contact type="tech">""" + self.info['clID'] + """</domain:contact>
            <domain:contact type="billing">""" + self.info['clIDBilling'] + """</domain:contact>
          </domain:create>
        </create>
        <clTRID>""" + self.info['clTRID'] + """</clTRID>
      </command>
    </epp>
    """

    print json.dumps({ "sent" : create })
    self.send_(create)
    return json.dumps({ "received" : self.receive() })

  def backorder(self):
    order = """
      <?xml version="1.0" encoding="UTF-8"?>
      <epp xmlns="urn:ietf:params:xml:ns:epp-1.0"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0
      epp-1.0.xsd">
        <command>
          <create>
            <future:create xmlns:future="http://www.dir.org/xsd/future1.0">
              <future:name>""" + self.info['testBackorder'] + """</future:name>
              <future:period unit="y">""" + self.info['years'] + """</future:period>
              <future:registrant>""" + self.info['clID'] + """</future:registrant>
            </future:create>
          </create>
          <clTRID>""" + self.info['clTRID'] + """</clTRID>
        </command>
      </epp>
    """

    print json.dumps({ "sent" : order })
    self.send_(order)
    return json.dumps({ "received" : self.receive() })

  def check(self):
    check = """
      <?xml version="1.0" encoding="UTF-8"?>
      <epp xmlns="urn:ietf:params:xml:ns:epp-1.0"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0
        epp-1.0.xsd">
       <command>
         <check>
           <future:check xmlns:future="http://www.dir.org/xsd/future1.0">
             <future:name>""" + self.info['testBackorder'] + """</future:name>
             <future:name>""" + self.info['testCheck01'] + """</future:name>
             <future:name>""" + self.info['testCheck02'] + """</future:name>
           </future:check>
         </check>
         <clTRID>""" + self.info['clTRID'] + """</clTRID>
       </command>
      </epp>
    """

    print json.dumps({ "sent" : check })
    self.send_(check)
    return json.dumps({ "received" : self.receive() })

  def receive(self):
    # Read first four bytes to retrieve message length.
    length = self.conn.recv(4)
    if length:
      # unpack() returns a one-element tuple.
      msg_length = struct.unpack(">I", length)[0] - 4
      received = b""
      while msg_length > len(received):
        chunk = self.conn.recv(4096)
        if chunk == b"":
          break
          # raise RuntimeError("socket connection broken")
        received += chunk
      return received

  def send_(self, msg):
    length = struct.pack(">I", len(msg) + 4 + 2)
    # Why "\r\n" has to be sent? Otherwise an connection error will occur.
    msg = msg.encode("utf-8") + b"\r\n"
    self.conn.sendall(length)
    self.conn.sendall(msg)