# ##############################################################################
# #
##  Copyright (C) 2013-2014 Tavendo GmbH
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

from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory
from vermeer.backend.util.isobus_converter import IopParser


class MyServerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if not isBinary:
            print("Text message received: {0}".format(payload.decode('utf8')))
            message = payload.decode('utf8')
            if 'connect' in message:
                # First time Client it connecting: Send decoded .iop file.
                msg = "{} from {}".format(message, self.peer)
                iop_parser = IopParser()
                try:
                    objects = iop_parser.parse("./vermeer/backend/util/example.iop")
                    # TODO: Broadcast the objects in json format
                    self.sendMessage(payload, isBinary)
                    self.sendMessage(payload, isBinary)
                except Exception, e:
                    print e
            elif 'test' in message:
                try:
                    json_data = open('./vermeer/backend/util/iop.json')
                    data = json.load(json_data)
                    payload = json.dumps(data, ensure_ascii=False).encode('utf8')
                    ## echo back message verbatim
                    self.sendMessage(payload, isBinary)
                except Exception, e:
                    print e
            else:
                self.sendMessage(payload, isBinary)
        else:
            print("Binary message received: {0} bytes".format(len(payload)))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    try:
        import asyncio
    except ImportError:
        ## Trollius >= 0.3 was renamed
        import trollius as asyncio

    factory = WebSocketServerFactory("ws://localhost:9000", debug=False)
    factory.protocol = MyServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 9000)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()