# ##############################################################################
##
##  Copyright (C) 2011-2013 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################
import json
import os

import sys

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
from vermeer.backend.util.isobus_converter import IopParser


class BroadcastServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        if not isBinary:
            message = payload.decode('utf8')
            if 'connect' in message:
                # First time Client it connecting: Send decoded .iop file.
                msg = "{} from {}".format(message, self.peer)
                iop_parser = IopParser()
                try:
                    objects = iop_parser.parse("./vermeer/backend/util/example.iop")
                    # TODO: Broadcast the objects in json format
                    self.factory.broadcast(msg)
                    self.factory.broadcast(objects)
                except Exception, e:
                    print e
            elif 'test' in message:
                try:
                    json_data = open('./vermeer/backend/util/iop.json')
                    data = json.load(json_data)
                    payload = json.dumps(data, ensure_ascii=False).encode('utf8')
                    ## echo back message verbatim
                    self.sendMessage(payload, isBinary)
                    ## self.factory.broadcast(payload)
                except Exception, e:
                    print e
            else:
                msg = "{} from {}".format(message, self.peer)
                self.factory.broadcast(msg)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):
    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """

    def __init__(self, url, debug=False, debugCodePaths=False):
        WebSocketServerFactory.__init__(self, url, debug=debug, debugCodePaths=debugCodePaths)
        self.clients = []
        self.tickcount = 0
        self.tick()

    def tick(self):
        self.tickcount += 1
        self.broadcast("tick %d from server" % self.tickcount)
        reactor.callLater(60, self.tick)

    def register(self, client):
        if not client in self.clients:
            print("registered client {}".format(client.peer))
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print("unregistered client {}".format(client.peer))
            self.clients.remove(client)

    def broadcast(self, msg):
        print("broadcasting message '{}' ..".format(msg))
        for c in self.clients:
            c.sendMessage(msg.encode('utf8'))
            print("message sent to {}".format(c.peer))


class BroadcastPreparedServerFactory(BroadcastServerFactory):
    """
    Functionally same as above, but optimized broadcast using
    prepareMessage and sendPreparedMessage.
    """

    def broadcast(self, msg):
        print("broadcasting prepared message '{}' ..".format(msg))
        prepared_msg = self.prepareMessage(msg)
        for c in self.clients:
            c.sendPreparedMessage(prepared_msg)
            print("prepared message sent to {}".format(c.peer))


if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        log.startLogging(sys.stdout)
        debug = True
    else:
        debug = False

    ServerFactory = BroadcastServerFactory
    #ServerFactory = BroadcastPreparedServerFactory

    factory = ServerFactory("ws://0.0.0.0:9000", debug=debug, debugCodePaths=debug)

    factory.protocol = BroadcastServerProtocol
    factory.setProtocolOptions(allowHixie76=True)
    listenWS(factory)

    webdir = File(".")
    web = Site(webdir)
    reactor.listenTCP(8080, web)

    reactor.run()