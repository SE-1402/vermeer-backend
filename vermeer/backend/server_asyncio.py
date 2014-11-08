# ##############################################################################
# #
# #  Copyright (C) 2013-2014 Tavendo GmbH
# #
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
import struct

from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory


class ObjectLocation:
    def __init__(self, object_id, x, y):
        self.x = x
        self.y = y
        self.object_id = object_id

    def __str__(self):
        return "Object {}, X location {}, Y location {}".format(self.object_id, self.x, self.y)


class MacroObject:
    def __init__(self, event_id, macro_id):
        self.event_id = event_id
        self.macro_id = macro_id

    def __str__(self):
        return "Macro {}, Event ID {}".format(self.macro_id, self.event_id)


class IopParser:
    def __init__(self):
        self.iop_file = None

    def parse(self, iop_file_name=None):
        if not iop_file_name:
            print(".iop file must be set")
            raise NotImplementedError
        else:
            try:
                self.iop_file = open(iop_file_name, 'rb')
            except IOError:
                print("Couldn't open file ", iop_file_name)
                raise IOError
        done = False
        objects = []

        while not done:
            data = struct.unpack('<HB', self.iop_file.read(3))
            print("Print Object ID: " + str(data[0]) + " Type " + str(data[1]))
            self.parse_object(data[0], data[1], file)

        self.iop_file.close()
        return objects

    def parse_data_mask(self, object_id, type_id, file):
        data_mask = struct.unpack('<BHBB', file.read(5))
        background_color = data_mask[0]
        softkey_mask = data_mask[1]
        number_objects = data_mask[2]
        number_macros = data_mask[3]
        objects = []
        macros = []

        for _ in range(number_objects):
            a = struct.unpack('<Hhh', file.read(6))
            objects.append(ObjectLocation(a[0], a[1], a[2]))

        for _ in range(number_macros):
            a = struct.unpack('<BB', file.read(2))
            macros.append(MacroObject(a[0], a[1]))

        print("Object ID : ", object_id, ", Type ", type_id, " Background color ", background_color, " Soft key mask ",
              softkey_mask, " Objets ", number_objects, " Macros ", number_macros)
        for obj in objects:
            print(obj)
        for macro in macros:
            print(macro)

    def parse_alarm_mask(self, object_id, type_id, file):
        temp = struct.unpack('<BHBBBB', file.read(7))
        background_color = temp[0]
        softkey_mask = temp[1]
        priority = temp[2]
        acoustic_signal = temp[3]
        number_objects = temp[4]
        number_macros = temp[5]
        objects = []
        macros = []

        for _ in range(number_objects):
            a = struct.unpack('<Hhh', file.read(6))
            objects.append(ObjectLocation(a[0], a[1], a[2]))

        for _ in range(number_macros):
            a = struct.unpack('<BB', file.read(2))
            macros.append(MacroObject(a[0], a[1]))

        print("Object ID : ", object_id,
              ", Type ", type_id,
              " Background color ", background_color,
              " Soft key mask ", softkey_mask,
              " Priority ", priority,
              " Acoustic Signal ", acoustic_signal,
              " Objets ", number_objects,
              " Macros ", number_macros)

        for obj in objects:
            print(obj)
        for macro in macros:
            print(macro)

    def parse_macro(self, object_id, type_id, file):
        temp = struct.unpack('<H', file.read(2))
        command_length = temp[0]
        commands = file.read(command_length)

        print("Object ID : ", object_id,
              ", Type ", type_id,
              " command_length ", command_length,
              " UNSUPPORTED PARSING OF COMMAND YET")

    def parse_object(self, object_id, object_type, file):
        return {
            1: self.parse_data_mask,
            2: self.parse_alarm_mask,
            28: self.parse_macro
        }[object_type](object_id, object_type, file)


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
                iop_parser = IopParser()
                try:
                    # TODO: Get .iop from CAN, currently hardcoded
                    objects = iop_parser.parse("./vermeer/backend/util/example.iop")
                    # TODO: Broadcast the objects in json format
                    self.sendMessage(payload, isBinary)
                    self.sendMessage(payload, isBinary)
                except Exception, e:
                    print e
            elif 'update' in message:
                pass
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