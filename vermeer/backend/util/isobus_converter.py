import sys
import os
import struct


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
        return "Macro {}, Event ID {}".format(self.macro_id,self.event_id) 


class IopParser:
    def __init__(self):
        self.iop_file = None

    def parse(self, iop_file_name=None):
        if not iop_file_name:
            print(".iop file must be set")
            raise NotImplementedError
        else:
            try:
                self.iop_file = open(iop_file_name,'rb')
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
        data_mask = struct.unpack('<BHBB',file.read(5))
        background_color = data_mask[0]
        softkey_mask = data_mask[1]
        number_objects = data_mask[2]
        number_macros = data_mask[3]
        objects = []
        macros = []

        for _ in range(number_objects):
            a = struct.unpack('<Hhh',file.read(6))
            objects.append(ObjectLocation(a[0], a[1], a[2]))

        for _ in range(number_macros):
            a = struct.unpack('<BB',file.read(2))
            macros.append(MacroObject(a[0], a[1]))

        print("Object ID : ", object_id, ", Type ",type_id, " Background color ",background_color, " Soft key mask ", softkey_mask, " Objets ", number_objects, " Macros ", number_macros)
        for obj in objects:
            print(obj)
        for macro in macros:
            print(macro)

    def parse_alarm_mask(self, object_id, type_id, file):
        temp = struct.unpack('<BHBBBB',file.read(7))
        background_color = temp[0]
        softkey_mask = temp[1]
        priority = temp[2]
        acoustic_signal = temp[3]
        number_objects = temp[4]
        number_macros = temp[5]
        objects = []
        macros = []

        for _ in range(number_objects):
            a = struct.unpack('<Hhh',file.read(6))
            objects.append(ObjectLocation(a[0], a[1], a[2]))

        for _ in range(number_macros):
            a = struct.unpack('<BB',file.read(2))
            macros.append(MacroObject(a[0], a[1]))

        print("Object ID : ", object_id,
              ", Type ",type_id,
              " Background color ",background_color,
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
        temp = struct.unpack('<H',file.read(2))
        command_length = temp[0]
        commands = file.read(command_length)

        print("Object ID : ", object_id,
              ", Type ",type_id,
              " command_length ",command_length,
              " UNSUPPORTED PARSING OF COMMAND YET")

    def parse_object(self, object_id, object_type, file):
        return {
                  1:self.parse_data_mask,
                  2:self.parse_alarm_mask,
                  28:self.parse_macro
               }[object_type](object_id, object_type, file)