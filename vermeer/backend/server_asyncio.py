# ##############################################################################
# #
# #  Copyright (C) 2013-2014 Tavendo GmbH
# #
# #  Licensed under the Apache License, Version 2.0 (the "License");
# #  you may not use this file except in compliance with the License.
# #  You may obtain a copy of the License at
# #
# #      http://www.apache.org/licenses/LICENSE-2.0
# #
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
import time
import serial


class IopParser:
    def __init__(self):
        self.iop_file = None
        self.data = {"include_macro": [], "data_mask": [], "alarm_mask": [], "container": [], "soft_key_mask": [],
                     "key": [],
                     "input_boolean": [], "input_string": [], "input_number": [], "button": [], "output_number": [],
                     "line": [], "rectangle": [], "ellipse": [], "polygon": [], "meter": [], "linear_bar_graph": [],
                     "arched_bar_graph": [], "picture_graphic": [], "number_variable": [], "string_variable": [],
                     "font_attribute": [], "line_attribute": [], "fill_attribute": [], "input_attribute": [],
                     "output_string": [], "object_pointer": [], "macro": []}

    def parse(self, iop_file_name=None):
        if not iop_file_name:
            print(".iop file must be set")
            raise NotImplementedError
        else:
            try:
                self.iop_file = open(iop_file_name, "rb")
            except IOError:
                print('''Couldn"t open file ", iop_file_name''')
                raise IOError
        done = False

        while not done:
            try:
                data = struct.unpack("<HB", self.iop_file.read(3))
                print("Print Object ID: " + str(data[0]) + " Type " + str(data[1]))
                self.parse_object(data[0], data[1], self.iop_file)
            except Exception, e:
                chunk = self.iop_file.read()
                if chunk == '':
                    print data
                self.iop_file.close()
                return self.data

        self.iop_file.close()
        return self.data

    def parse_object(self, object_id, object_type, iop_file):
        return {
            0: self.parse_working_set,
            1: self.parse_data_mask,
            2: self.parse_alarm_mask,
            3: self.parse_container,
            4: self.parse_soft_key_mask,
            5: self.parse_key,
            6: self.parse_button,
            7: self.parse_input_boolean_field,
            8: self.parse_input_string_field,
            9: self.parse_input_number_field,
            10: self.parse_input_list_field,
            11: self.parse_output_string_field,
            12: self.parse_output_number_field,
            13: self.parse_line,
            14: self.parse_rectangle,
            15: self.parse_ellipse,
            16: self.parse_polygon,
            17: self.parse_meter,
            18: self.parse_linear_bar_graph,
            19: self.parse_arched_bar_graph,
            20: self.parse_picture_graphic,
            21: self.parse_number_variable,
            22: self.parse_string_variable,
            23: self.parse_font_attr_object,
            24: self.parse_line_attr_object,
            25: self.parse_fill_attr_object,
            26: self.parse_input_attr_object,
            27: self.parse_object_ptr,
            28: self.parse_macro,
            29: self.parse_aux_function,
            30: self.parse_aux_input,
            31: self.parse_aux_function_two,
            32: self.parse_aux_input_two,
            33: self.parse_aux_control_two,
            34: self.parse_window_mask,
            35: self.parse_key_group,
            36: self.parse_graphics_context,
            37: self.parse_output_list_field,
            38: self.parse_extended_input_attr,
            39: self.parse_color_map,
            40: self.parse_object_label_ref_list
        }[object_type](object_id, object_type, iop_file)

    # MACRO PARSING
    def parse_macro_hide_show_object(self, byte_length, iop_file):
        iop_file.read(byte_length - 1)

    def parse_macro_change_numberic_value(self, byte_length, iop_file):
        parsed_object = struct.unpack("<HBL", iop_file.read(7))
        object_id_changed = parsed_object[0]
        reserved = parsed_object[1]
        new_value = parsed_object[2]

    def parse_macro_change_active_mask(self, command_type, byte_length, iop_file):
        parsed_object = struct.unpack("<HHBBB", iop_file.read(7))
        working_set_object_id = parsed_object[0]
        new_active_mask_object_id = parsed_object[1]
        reserved = parsed_object[2]
        return {"command_type": command_type, "working_set_object_id": working_set_object_id,
                "new_active_mask_object_id": new_active_mask_object_id, "reserved": reserved}

    # OBJECT POOL PARSING
    def parse_working_set(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<B?HBBB", iop_file.read(7))
        background_colour = parsed_object[0]
        selectable = parsed_object[1]
        active_mask = parsed_object[2]
        number_objects = parsed_object[3]
        number_macros = parsed_object[4]
        number_languages = parsed_object[5]
        objects = []
        macros = []
        languages = []

        for _ in range(number_objects):
            a = struct.unpack("<Hhh", iop_file.read(6))
            objects.append({"id": a[0], "pos_x": a[1], "pos_y": a[2]})

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        for _ in range(number_languages):
            a = struct.unpack("<cc", iop_file.read(2))
            languages.append({"code": a[0] + a[1]})

        workingset = {"id": object_id, "background_colour": background_colour, "selectable": selectable,
                      "active_mask": active_mask, "language": languages, "include_object": objects,
                      "include_macro": macros}
        self.data["working_set"] = workingset

    def parse_data_mask(self, object_id, type_id, iop_file):
        data_mask = struct.unpack("<BHBB", iop_file.read(5))
        background_colour = data_mask[0]
        soft_key_mask = data_mask[1]
        number_objects = data_mask[2]
        number_macros = data_mask[3]
        objects = []
        macros = []

        for _ in range(number_objects):
            a = struct.unpack("<Hhh", iop_file.read(6))
            objects.append({"id": a[0], "pos_x": a[1], "pos_y": a[2]})

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "background_colour": background_colour, "soft_key_mask": soft_key_mask,
                 "include_object": objects, "include_macro": macros}
        self.data["data_mask"].append(toadd)

    def parse_alarm_mask(self, object_id, type_id, iop_file):
        temp = struct.unpack("<BHBBBB", iop_file.read(7))
        background_colour = temp[0]
        soft_key_mask = temp[1]
        priority = temp[2]
        acoustic_signal = temp[3]
        number_objects = temp[4]
        number_macros = temp[5]
        objects = []
        macros = []

        for _ in range(number_objects):
            a = struct.unpack("<Hhh", iop_file.read(6))
            objects.append({"id": a[0], "pos_x": a[1], "pos_y": a[2]})

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "background_colour": background_colour, "soft_key_mask": soft_key_mask,
                 "priority": priority, "acoustic_signal": acoustic_signal, "include_object": objects,
                 "include_macro": macros}
        self.data["alarm_mask"].append(toadd)

    def parse_container(self, object_id, type_id, iop_file):
        container = struct.unpack("<HHBBB", iop_file.read(7))
        width = container[0]
        height = container[1]
        hidden = container[2]
        number_objects = container[3]
        number_macros = container[4]
        objects = []
        macros = []

        for _ in range(number_objects):
            a = struct.unpack("<Hhh", iop_file.read(6))
            objects.append({"id": a[0], "pos_x": a[1], "pos_y": a[2]})

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "width": width, "height": height, "hidden": hidden, "include_object": objects,
                 "include_macro": macros}
        self.data["container"].append(toadd)

    def parse_soft_key_mask(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<BBB", iop_file.read(3))
        background_colour = parsed_object[0]
        number_objects = parsed_object[1]
        number_macros = parsed_object[2]
        objects = []
        macros = []

        for _ in range(number_objects):
            a = struct.unpack("<H", iop_file.read(2))
            objects.append({"id": a[0]})  # , "pos_x": 0, "pos_y": 0})

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "background_colour": background_colour, "include_object": objects,
                 "include_macro": macros}
        self.data["soft_key_mask"].append(toadd)

    def parse_key(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<BBBB", iop_file.read(4))
        background_colour = parsed_object[0]
        key_code = parsed_object[1]
        number_objects = parsed_object[2]
        number_macros = parsed_object[3]
        objects = []
        macros = []

        for _ in range(number_objects):
            a = struct.unpack("<Hhh", iop_file.read(6))
            objects.append({"id": a[0], "pos_x": a[1], "pos_y": a[2]})

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "background_colour": background_colour, "key_code": key_code,
                 "include_object": objects, "include_macro": macros}
        self.data["key"].append(toadd)

    def parse_button(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<HHBBBBBB", iop_file.read(10))
        width = parsed_object[0]
        height = parsed_object[1]
        background_colour = parsed_object[2]
        border_color = parsed_object[3]
        key_code = parsed_object[4]
        options = parsed_object[5]
        number_objects = parsed_object[6]
        number_macros = parsed_object[7]
        objects = []
        macros = []

        for _ in range(number_objects):
            a = struct.unpack("<Hhh", iop_file.read(6))
            objects.append({"id": a[0], "pos_x": a[1], "pos_y": a[2]})

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "width": width, "height": height, "background_colour": background_colour,
                 "border_color": border_color, "key_code": key_code, "options": options, "include_object": objects,
                 "include_macro": macros}
        self.data["button"].append(toadd)

    def parse_input_boolean_field(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<BHHHBBB", iop_file.read(10))
        background_colour = parsed_object[0]
        width = parsed_object[1]
        foreground_color = parsed_object[2]
        variable_reference = parsed_object[3]
        value = parsed_object[4]
        enabled = parsed_object[5]
        number_macros = parsed_object[6]
        macros = []

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "background_colour": background_colour, "width": width,
                 "foreground_color": foreground_color, "variable_reference": variable_reference, "value": value,
                 "enabled": enabled, "include_macro": macros}
        self.data["input_boolean"].append(toadd)

    def parse_input_string_field(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<HHBHHBHBB", iop_file.read(14))
        width = parsed_object[0]
        height = parsed_object[1]
        background_colour = parsed_object[2]
        font_attr = parsed_object[3]
        input_attr = parsed_object[4]
        options = parsed_object[5]
        variable_ref = parsed_object[6]
        justification = parsed_object[7]
        length = parsed_object[8]
        value = []

        for _ in range(length):
            character = struct.unpack("<c", iop_file.read(1))
            value.append(character[0])

        input_string = struct.unpack("<BB", iop_file.read(2))
        enabled = input_string[0]
        number_macros = input_string[1]
        macros = []

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "width": width, "height": height, "background_colour": background_colour,
                 "font_attribute": font_attr, "input_attribute": input_attr, "options": options,
                 "variable_reference": variable_ref, "justification": justification, "length": length,
                 "value": "".join(value), "enabled": enabled, "include_macro": macros}
        self.data["input_string"].append(toadd)

    def parse_input_number_field(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<HHBHBHLLLlfBBBBB", iop_file.read(35))
        width = parsed_object[0]
        height = parsed_object[1]
        background_colour = parsed_object[2]
        font_attr = parsed_object[3]
        options = parsed_object[4]
        variable_ref = parsed_object[5]
        value = parsed_object[6]
        min_value = parsed_object[7]
        max_value = parsed_object[8]
        offset = parsed_object[9]
        scale = parsed_object[10]
        num_decimals = parsed_object[11]
        format = parsed_object[12]
        justification = parsed_object[13]
        options_2 = parsed_object[14]
        number_macros = parsed_object[15]
        macros = []

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "width": width, "height": height, "background_colour": background_colour,
                 "font_attribute": font_attr, "options": options, "variable_reference": variable_ref, "value": value,
                 "min_value": min_value, "max_value": max_value, "offset": offset, "scale": scale,
                 "number_of_decimals": num_decimals,
                 "format": format, "justification": justification, "options_2": options_2, "include_macro": macros}
        self.data["input_number"].append(toadd)

    def parse_input_list_field(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<HHHBBBB", iop_file.read(10))
        width = parsed_object[0]
        height = parsed_object[1]
        variable_ref = parsed_object[2]
        value = parsed_object[3]
        number_list_items = parsed_object[4]
        options = parsed_object[5]
        number_macros = parsed_object[6]
        macros = []

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "width": width, "height": height, "variable_reference": variable_ref, "value": value,
                 "number_of_list_items": number_list_items, "options": options, "include_macro": macros}
        self.data["input_list"].append(toadd)

    def parse_output_string_field(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<HHBHBHBH", iop_file.read(13))
        width = parsed_object[0]
        height = parsed_object[1]
        background_colour = parsed_object[2]
        font_attr = parsed_object[3]
        options = parsed_object[4]
        variable_ref = parsed_object[5]
        justification = parsed_object[6]
        length = parsed_object[7]
        value = []

        for _ in range(length):
            a = struct.unpack("<c", iop_file.read(1))
            value.append(a[0])

        parsed_object = struct.unpack("<B", iop_file.read(1))
        number_macros = parsed_object[0]
        macros = []

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "width": width, "height": height, "background_colour": background_colour,
                 "font_attribute": font_attr, "options": options, "variable_ref": variable_ref,
                 "justification": justification, "length": length, "value": "".join(value), "include_macro": macros}
        self.data["output_string"].append(toadd)

    def parse_output_number_field(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<HHBHBHLlfBBB", iop_file.read(25))
        width = parsed_object[0]
        height = parsed_object[1]
        background_colour = parsed_object[2]
        font_attr = parsed_object[3]
        options = parsed_object[4]
        variable_ref = parsed_object[5]
        value = parsed_object[6]
        offset = parsed_object[7]
        scale = parsed_object[8]
        num_decimals = parsed_object[9]
        format = parsed_object[10]
        justification = parsed_object[11]
        number_macros = parsed_object[12]
        macros = []

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "width": width, "height": height, "background_colour": background_colour,
                 "font_attribute": font_attr, "options": options, "variable_ref": variable_ref, "value": value,
                 "offset": offset, "scale": scale, "num_decimals": num_decimals, "format": format,
                 "justification": justification, "include_macro": macros}
        self.data["output_number"].append(toadd)

    def parse_output_list_field(self, object_id, type_id, iop_file):
        # TODO: parse_output_list_field
        pass

    def parse_line(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<HHHBB", iop_file.read(8))
        line_attr = parsed_object[0]
        width = parsed_object[1]
        height = parsed_object[2]
        line_direction = parsed_object[3]
        number_macros = parsed_object[4]
        macros = []

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "line_attribute": line_attr, "width": width, "height": height,
                 "line_direction": line_direction, "include_macro": macros}
        self.data["line"].append(toadd)

    def parse_rectangle(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<HHHBHB", iop_file.read(10))
        line_attr = parsed_object[0]
        width = parsed_object[1]
        height = parsed_object[2]
        line_suppression = parsed_object[3]
        fill_attr = parsed_object[4]
        number_macros = parsed_object[5]
        macros = []

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "line_attribute": line_attr, "width": width, "height": height,
                 "line_suppression": line_suppression, "fill_attribute": fill_attr, "include_macro": macros}
        self.data["rectangle"].append(toadd)

    def parse_ellipse(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<HHHBBBHB", iop_file.read(12))
        line_attr = parsed_object[0]
        width = parsed_object[1]
        height = parsed_object[2]
        ellipse_type = parsed_object[3]
        start_angle = parsed_object[4]
        end_angle = parsed_object[5]
        fill_attr = parsed_object[6]
        number_macros = parsed_object[7]
        macros = []

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "line_attribute": line_attr, "width": width, "height": height,
                 "ellipse_type": ellipse_type, "start_angle": start_angle, "end_angle": end_angle,
                 "fill_attribute": fill_attr, "include_macro": macros}
        self.data["ellipse"].append(toadd)

    def parse_polygon(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<HHHHBBB", iop_file.read(11))
        width = parsed_object[0]
        height = parsed_object[1]
        line_attr = parsed_object[2]
        fill_attr = parsed_object[3]
        polygon_type = parsed_object[4]
        number_of_points = parsed_object[5]
        number_macros = parsed_object[6]
        macros = []
        points = []

        for _ in range(number_of_points):
            a = struct.unpack("<HH", iop_file.read(4))
            points.append({"pos_x": a[0], "pos_y": a[1]})

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "width": width, "height": height, "line_attribute": line_attr,
                 "fill_attribute": fill_attr, "polygon_type": polygon_type, "number_of_points": number_of_points,
                 "number_macros": number_macros, "points": points, "include_macro": macros}
        self.data["polygon"].append(toadd)

    def parse_meter(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<HBBBBBBBHHHHB", iop_file.read(18))
        width = parsed_object[0]
        needle_color = parsed_object[1]
        border_color = parsed_object[2]
        arc_and_tick_color = parsed_object[3]
        options = parsed_object[4]
        number_ticks = parsed_object[5]
        start_angle = parsed_object[6]
        end_angle = parsed_object[7]
        min_value = parsed_object[8]
        max_value = parsed_object[9]
        variable_ref = parsed_object[10]
        value = parsed_object[11]
        number_macros = parsed_object[12]
        macros = []

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "width": width, "needle_color": needle_color, "border_color": border_color,
                 "arc_and_tick_color": arc_and_tick_color, "options": options, "number_ticks": number_ticks,
                 "start_angle": start_angle, "end_angle": end_angle, "min_value": min_value, "max_value": max_value,
                 "variable_reference": variable_ref, "value": value, "number_macros": number_macros,
                 "include_macro": macros}
        self.data["meter"].append(toadd)

    def parse_linear_bar_graph(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<HHBBBBHHHHHHB", iop_file.read(21))
        width = parsed_object[0]
        height = parsed_object[1]
        colour = parsed_object[2]
        target_line_colour = parsed_object[3]
        options = parsed_object[4]
        number_ticks = parsed_object[5]
        min_value = parsed_object[6]
        max_value = parsed_object[7]
        variable_ref = parsed_object[8]
        value = parsed_object[9]
        target_value_variable_ref = parsed_object[10]
        target_value = parsed_object[11]
        number_macros = parsed_object[12]
        macros = []

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "width": width, "height": height, "colour": colour,
                 "target_line_colour": target_line_colour, "options": options, "number_of_ticks": number_ticks,
                 "min_value": min_value, "max_value": max_value, "variable_reference": variable_ref, "value": value,
                 "target_value_variable_reference": target_value_variable_ref, "target_value": target_value,
                 "number_macros": number_macros, "include_macro": macros}
        self.data["linear_bar_graph"].append(toadd)

    def parse_arched_bar_graph(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<HHBBBBBHHHHHHHB", iop_file.read(24))
        width = parsed_object[0]
        height = parsed_object[1]
        colour = parsed_object[2]
        target_line_colour = parsed_object[3]
        options = parsed_object[4]
        start_angle = parsed_object[5]
        end_angle = parsed_object[6]
        bar_graph_width = parsed_object[7]
        min_value = parsed_object[8]
        max_value = parsed_object[9]
        variable_ref = parsed_object[10]
        value = parsed_object[11]
        target_value_variable_ref = parsed_object[12]
        target_value = parsed_object[13]
        number_macros = parsed_object[14]
        macros = []

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "width": width, "height": height, "colour": colour,
                 "target_line_colour": target_line_colour, "options": options, "start_angle": start_angle,
                 "end_angle": end_angle, "bar_graph_width": bar_graph_width, "min_value": min_value,
                 "max_value": max_value, "variable_reference": variable_ref, "value": value,
                 "target_value_variable_reference": target_value_variable_ref, "target_value": target_value,
                 "number_macros": number_macros, "include_macro": macros}
        self.data["arched_bar_graph"].append(toadd)

    def parse_picture_graphic(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<HHHBBBLB", iop_file.read(14))
        width = parsed_object[0]
        actual_width = parsed_object[1]
        actual_height = parsed_object[2]
        format = parsed_object[3]
        options = parsed_object[4]
        transparency_colour = parsed_object[5]
        number_bytes_raw_data = parsed_object[6]
        number_macros = parsed_object[7]
        raw_data = []
        macros = []

        for _ in range(number_bytes_raw_data):
            a = struct.unpack("<B", iop_file.read(1))
            raw_data.append(a[0])

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "width": width, "actual_width": actual_width, "actual_height": actual_height,
                 "format": format, "options": options, "transparency_colour": transparency_colour,
                 "number_bytes_raw_data": number_bytes_raw_data, "number_macros": number_macros, "raw_data": raw_data,
                 "include_macro": macros}
        # self.data["picture_graphic"].append(toadd)

    def parse_number_variable(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<L", iop_file.read(4))
        value = parsed_object[0]

        toadd = {"id": object_id, "value": value}
        self.data["number_variable"].append(toadd)

    def parse_string_variable(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<H", iop_file.read(2))
        length = parsed_object[0]
        value = []

        for _ in range(length):
            a = struct.unpack("<c", iop_file.read(1))
            value.append(a[0])

        toadd = {"id": object_id, "length": length, "value": "".join(value)}
        self.data["string_variable"].append(toadd)

    def parse_font_attr_object(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<BBBBB", iop_file.read(5))
        font_colour = parsed_object[0]
        font_size = parsed_object[1]
        font_type = parsed_object[2]
        font_style = parsed_object[3]
        number_macros = parsed_object[4]
        macros = []

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "font_colour": font_colour, "font_size": font_size, "font_type": font_type,
                 "font_style": font_style, "number_macros": number_macros, "include_macro": macros}
        self.data["font_attribute"].append(toadd)

    def parse_line_attr_object(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<BBHB", iop_file.read(5))
        line_color = parsed_object[0]
        line_width = parsed_object[1]
        line_art = parsed_object[2]
        number_macros = parsed_object[3]
        macros = []

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "line_color": line_color, "line_width": line_width, "line_art": line_art,
                 "number_macros": number_macros, "include_macro": macros}
        self.data["line_attribute"].append(toadd)

    def parse_fill_attr_object(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<BBHB", iop_file.read(5))
        fill_type = parsed_object[0]
        fill_colour = parsed_object[1]
        fill_pattern = parsed_object[2]
        number_macros = parsed_object[3]
        macros = []

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "fill_type": fill_type, "fill_colour": fill_colour, "fill_pattern": fill_pattern,
                 "number_macros": number_macros, "include_macro": macros}
        self.data["fill_attribute"].append(toadd)

    def parse_input_attr_object(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<BB", iop_file.read(2))
        validation_type = parsed_object[0]
        length = parsed_object[1]
        validation_string = []

        for _ in range(length):
            a = struct.unpack("<c", iop_file.read(1))
            validation_string.append(a[0])

        parsed_object = struct.unpack("<B", iop_file.read(1))
        number_macros = parsed_object[0]
        macros = []

        for _ in range(number_macros):
            a = struct.unpack("<BB", iop_file.read(2))
            macros.append({"event_id": a[0], "macro_id": a[1]})

        toadd = {"id": object_id, "validation_type": validation_type, "length": length,
                 "validation_string": "".join(validation_string),
                 "number_macros": number_macros, "include_macro": macros}
        self.data["input_attribute"].append(toadd)

    def parse_object_ptr(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<H", iop_file.read(2))
        value = parsed_object[0]

        toadd = {"id": object_id, "value": value}
        self.data["object_pointer"].append(toadd)

    def parse_macro(self, object_id, type_id, iop_file):
        parsed_object = struct.unpack("<H", iop_file.read(2))
        number_bytes_follow = parsed_object[0]
        commands = []

        command_type = struct.unpack("<B", iop_file.read(1))
        command = {}
        if command_type[0] == 160:
            # Command: Hide/Show Object
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 161:
            # Command: Enable/Disable Object
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 162:
            # Command: Select Input Object
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 163:
            # Command: Control Audio Signal
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 164:
            # Command: Set Audio Volume
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 165:
            # Command: Change Child Location
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 180:
            # Command: Change Child Position
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 166:
            # Command: Change Size
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 167:
            # Command: Change Background Color
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 168:
            # Command: Change Numeric Value
            self.parse_macro_change_numberic_value(number_bytes_follow, iop_file)
        elif command_type[0] == 179:
            # Command: Change String Value
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 169:
            # Command: Change End Point
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 170:
            # Command: Change Font Attr
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 171:
            # Command: Change Line Attr
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 172:
            # Command: Change Fill Attr
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 173:
            # Command: Change Active Mask
            command = self.parse_macro_change_active_mask(command_type[0], number_bytes_follow, iop_file)
        elif command_type[0] == 174:
            # Command: Change Soft Key Mask
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 175:
            # Command: Change Attr
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 176:
            # Command: Change Priority:
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 177:
            # Command: Change List Item
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 189:
            # Command: Lock/Unlock Mask
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 190:
            # Command: Execute Macro
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 181:
            # Command: Change Object Label
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 182:
            # Command: Change Polygon Point
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 183:
            # Command: Change Polygon Scale
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 184:
            # Command: Graphics Context
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        elif command_type[0] == 186:
            # Command: Select Color Map
            self.parse_macro_hide_show_object(number_bytes_follow, iop_file)
        else:
            raise KeyError
        commands.append(command_type[0])
        toadd = {"id": object_id, "number_bytes_follow": number_bytes_follow, "command": command}
        self.data["macro"].append(toadd)

    def parse_color_map(self, object_id, type_id, iop_file):
        pass

    def parse_graphics_context(self, object_id, type_id, iop_file):
        pass

    def parse_window_mask(self, object_id, type_id, iop_file):
        pass

    def parse_aux_function(self, object_id, type_id, iop_file):
        pass

    def parse_aux_input(self, object_id, type_id, iop_file):
        pass

    def parse_aux_function_two(self, object_id, type_id, iop_file):
        pass

    def parse_aux_input_two(self, object_id, type_id, iop_file):
        pass

    def parse_aux_control_two(self, object_id, type_id, iop_file):
        pass

    def parse_key_group(self, object_id, type_id, iop_file):
        pass

    def parse_extended_input_attr(self, object_id, type_id, iop_file):
        pass

    def parse_object_label_ref_list(self, object_id, type_id, iop_file):
        pass


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
                    iop_data = iop_parser.parse("./vermeer/backend/util/example.iop")
                    # TODO: Broadcast the objects in json format
                    payload = json.dumps(iop_data, ensure_ascii=False).encode('utf8')
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


def read_uart(timeout):
    ser = serial.Serial(0)
    i = 0
    while True:
        try:
            val = ser.read(5)
            print(1)
            i += 1

            if val != "":
                ser.close
                return val
            elif i > timeout:
                ser.close
                return ""

            time.sleep(1 / 1000.00)
        except Exception:
            if i == 0:
                print "Port Not Connected"
            elif i > timeout:
                ser.close
                return ""
            i += 1
            time.sleep(1 / 1000.00)


def read_uart_for_value(message_value, uart_timeout):
    if read_uart(uart_timeout) == message_value:
        return True
    return False


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

    print("Server Starting...")
    try:
        while not read_uart_for_value("Start", 3000):
            print("START signal not received, still waiting")
        print("Start signal received.")
        loop.run_forever()
    except KeyboardInterrupt:
        print("Server Error...")
        pass
    finally:
        print("Server Stopped...")
        server.close()
        loop.close()
