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
        return "Macro {}, Event ID {}".format(self.macro_id, self.event_id)


class LanguageObject:
    def __init__(self, language_code):
        self.language_code = language_code

    def __str__(self):
        return "Language {}".format(self.language_code)


class PointObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point: X @ {}, Y @ {}".format(self.x, self.y)


# MACRO PARSING

def parse_macro_hide_show_object(byte_length, iop_file):
    iop_file.read(byte_length - 1)


def parse_macro_change_numberic_value(byte_length, iop_file):
    parsed_object = struct.unpack('<HBL', iop_file.read(7))
    object_id_changed = parsed_object[0]
    reserved = parsed_object[1]
    new_value = parsed_object[2]


def parse_macro_change_active_mask(byte_length, iop_file):
    parsed_object = struct.unpack('<HHBBB', iop_file.read(7))
    working_set_object_id = parsed_object[0]
    new_active_mask_object_id = parsed_object[1]
    reserved = parsed_object[2]


def parse_working_set(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<B?HBBB', iop_file.read(7))
    background_color = parsed_object[0]
    selectable = parsed_object[1]
    active_mask = parsed_object[2]
    number_objects = parsed_object[3]
    number_macros = parsed_object[4]
    number_languages = parsed_object[5]
    objects = []
    macros = []
    languages = []

    for _ in range(number_objects):
        a = struct.unpack('<Hhh', iop_file.read(6))
        objects.append(ObjectLocation(a[0], a[1], a[2]))

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))

    for _ in range(number_languages):
        a = struct.unpack('<cc', iop_file.read(2))
        languages.append(LanguageObject(a[0] + a[1]))


def parse_data_mask(object_id, type_id, iop_file):
    data_mask = struct.unpack('<BHBB', iop_file.read(5))
    background_color = data_mask[0]
    soft_key_mask = data_mask[1]
    number_objects = data_mask[2]
    number_macros = data_mask[3]
    objects = []
    macros = []

    for _ in range(number_objects):
        a = struct.unpack('<Hhh', iop_file.read(6))
        objects.append(ObjectLocation(a[0], a[1], a[2]))

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_alarm_mask(object_id, type_id, iop_file):
    temp = struct.unpack('<BHBBBB', iop_file.read(7))
    background_color = temp[0]
    soft_key_mask = temp[1]
    priority = temp[2]
    acoustic_signal = temp[3]
    number_objects = temp[4]
    number_macros = temp[5]
    objects = []
    macros = []

    for _ in range(number_objects):
        a = struct.unpack('<Hhh', iop_file.read(6))
        objects.append(ObjectLocation(a[0], a[1], a[2]))

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_container(object_id, type_id, iop_file):
    container = struct.unpack('<HHBBB', iop_file.read(7))
    width = container[0]
    height = container[1]
    hidden = container[2]
    number_objects = container[3]
    number_macros = container[4]
    objects = []
    macros = []

    for _ in range(number_objects):
        a = struct.unpack('<Hhh', iop_file.read(6))
        objects.append(ObjectLocation(a[0], a[1], a[2]))

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_soft_key_mask(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<BBB', iop_file.read(3))
    background_color = parsed_object[0]
    number_objects = parsed_object[1]
    number_macros = parsed_object[2]
    objects = []
    macros = []

    for _ in range(number_objects):
        a = struct.unpack('<H', iop_file.read(2))
        objects.append(a[0])

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_key(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<BBBB', iop_file.read(4))
    background_color = parsed_object[0]
    key_code = parsed_object[1]
    number_objects = parsed_object[2]
    number_macros = parsed_object[3]
    objects = []
    macros = []

    for _ in range(number_objects):
        a = struct.unpack('<Hhh', iop_file.read(6))
        objects.append(ObjectLocation(a[0], a[1], a[2]))

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_button(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<HHBBBBBB', iop_file.read(10))
    width = parsed_object[0]
    height = parsed_object[1]
    background_color = parsed_object[2]
    border_color = parsed_object[3]
    key_code = parsed_object[4]
    options = parsed_object[5]
    number_objects = parsed_object[6]
    number_macros = parsed_object[7]
    objects = []
    macros = []

    for _ in range(number_objects):
        a = struct.unpack('<Hhh', iop_file.read(6))
        objects.append(ObjectLocation(a[0], a[1], a[2]))

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_input_boolean_field(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<BHHHBBB', iop_file.read(10))
    background_color = parsed_object[0]
    width = parsed_object[1]
    foreground_color = parsed_object[2]
    variable_reference = parsed_object[3]
    value = parsed_object[4]
    enabled = parsed_object[5]
    number_macros = parsed_object[6]
    macros = []

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_input_string_field(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<HHBHHBHBB', iop_file.read(14))
    width = parsed_object[0]
    height = parsed_object[1]
    background_color = parsed_object[2]
    font_attr = parsed_object[3]
    input_attr = parsed_object[4]
    options = parsed_object[5]
    variable_ref = parsed_object[6]
    justification = parsed_object[7]
    length = parsed_object[8]
    characters = []
    value = ''

    for _ in range(length):
        character = struct.unpack('<c', iop_file.read(1))
        characters.append(character[0])

    input_string = struct.unpack('<BB', iop_file.read(2))
    enabled = input_string[0]
    number_macros = input_string[1]
    macros = []

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_input_number_field(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<HHBHBHLLLlfBBBBB', iop_file.read(35))
    width = parsed_object[0]
    height = parsed_object[1]
    background_color = parsed_object[2]
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
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_input_list_field(object_id, type_id, iop_file):
    pass


def parse_output_string_field(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<HHBHBHBH', iop_file.read(13))
    width = parsed_object[0]
    height = parsed_object[1]
    background_color = parsed_object[2]
    font_attr = parsed_object[3]
    options = parsed_object[4]
    variable_ref = parsed_object[5]
    justification = parsed_object[6]
    length = parsed_object[7]
    value = []

    for _ in range(length):
        a = struct.unpack('<c', iop_file.read(1))
        value.append(a[0])

    parsed_object = struct.unpack('<B', iop_file.read(1))
    number_macros = parsed_object[0]
    macros = []

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_output_number_field(object_id, type_id, iop_file):
    pass


def parse_line(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<HHHBB', iop_file.read(8))
    line_attr = parsed_object[0]
    width = parsed_object[1]
    height = parsed_object[2]
    line_direction = parsed_object[3]
    number_macros = parsed_object[4]
    macros = []

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_rectangle(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<HHHBHB', iop_file.read(10))
    line_attr = parsed_object[0]
    width = parsed_object[1]
    height = parsed_object[2]
    line_suppression = parsed_object[3]
    fill_attr = parsed_object[4]
    number_macros = parsed_object[5]
    macros = []

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_ellipse(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<HHHBBBHB', iop_file.read(12))
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
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_polygon(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<HHHHBBB', iop_file.read(11))
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
        a = struct.unpack('<HH', iop_file.read(4))
        points.append(PointObject(a[0], a[1]))

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_meter(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<HBBBBBBBHHHHB', iop_file.read(18))
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
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_linear_bar_graph(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<HHBBBBHHHHHHB', iop_file.read(21))
    width = parsed_object[0]
    height = parsed_object[1]
    color = parsed_object[2]
    target_line_color = parsed_object[3]
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
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_arched_bar_graph(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<HHBBBBBHHHHHHHB', iop_file.read(24))
    width = parsed_object[0]
    height = parsed_object[1]
    color = parsed_object[2]
    target_line_color = parsed_object[3]
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
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_picture_graphic(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<HHHBBBLB', iop_file.read(14))
    width = parsed_object[0]
    actual_width = parsed_object[1]
    actual_height = parsed_object[2]
    format = parsed_object[3]
    options = parsed_object[4]
    transparency_color = parsed_object[5]
    number_bytes_raw_data = parsed_object[6]
    number_macros = parsed_object[7]
    raw_data = []
    macros = []

    for _ in range(number_bytes_raw_data):
        a = struct.unpack('<B', iop_file.read(1))
        raw_data.append(a[0])

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_number_variable(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<L', iop_file.read(4))
    value = parsed_object[0]


def parse_string_variable(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<H', iop_file.read(2))
    length = parsed_object[0]
    value = []

    for _ in range(length):
        a = struct.unpack('<c', iop_file.read(1))
        value.append(a[0])


def parse_font_attr_object(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<BBBBB', iop_file.read(5))
    font_color = parsed_object[0]
    font_size = parsed_object[1]
    font_type = parsed_object[2]
    font_style = parsed_object[3]
    number_macros = parsed_object[4]
    macros = []

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_line_attr_object(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<BBHB', iop_file.read(5))
    line_color = parsed_object[0]
    line_width = parsed_object[1]
    line_art = parsed_object[2]
    number_macros = parsed_object[3]
    macros = []

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_fill_attr_object(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<BBHB', iop_file.read(5))
    fill_type = parsed_object[0]
    fill_color = parsed_object[1]
    fill_pattern = parsed_object[2]
    number_macros = parsed_object[3]
    macros = []

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_input_attr_object(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<BB', iop_file.read(2))
    validation_type = parsed_object[0]
    length = parsed_object[1]
    validation_string = []

    for _ in range(length):
        a = struct.unpack('<c', iop_file.read(1))
        validation_string.append(a[0])

    parsed_object = struct.unpack('<B', iop_file.read(1))
    number_macros = parsed_object[0]
    macros = []

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_object_ptr(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<H', iop_file.read(2))
    value = parsed_object[0]


def parse_macro(object_id, type_id, iop_file):
    parsed_object = struct.unpack('<H', iop_file.read(2))
    number_bytes_follow = parsed_object[0]
    commands = []

    command_type = struct.unpack('<B', iop_file.read(1))
    if command_type[0] == 160:
        # Command: Hide/Show Object
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 161:
        # Command: Enable/Disable Object
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 162:
        # Command: Select Input Object
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 163:
        # Command: Control Audio Signal
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 164:
        # Command: Set Audio Volume
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 165:
        # Command: Change Child Location
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 180:
        # Command: Change Child Position
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 166:
        # Command: Change Size
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 167:
        # Command: Change Background Color
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 168:
        # Command: Change Numeric Value
        parse_macro_change_numberic_value(number_bytes_follow, iop_file)
    elif command_type[0] == 179:
        # Command: Change String Value
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 169:
        # Command: Change End Point
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 170:
        # Command: Change Font Attr
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 171:
        # Command: Change Line Attr
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 172:
        # Command: Change Fill Attr
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 173:
        # Command: Change Active Mask
        parse_macro_change_active_mask(number_bytes_follow, iop_file)
    elif command_type[0] == 174:
        # Command: Change Soft Key Mask
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 175:
        # Command: Change Attr
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 176:
        # Command: Change Priority:
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 177:
        # Command: Change List Item
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 189:
        # Command: Lock/Unlock Mask
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 190:
        # Command: Execute Macro
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 181:
        # Command: Change Object Label
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 182:
        # Command: Change Polygon Point
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 183:
        # Command: Change Polygon Scale
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 184:
        # Command: Graphics Context
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    elif command_type[0] == 186:
        # Command: Select Color Map
        parse_macro_hide_show_object(number_bytes_follow, iop_file)
    else:
        raise KeyError
    commands.append(command_type[0])


def parse_aux_function(object_id, type_id, iop_file):
    pass


def parse_aux_input(object_id, type_id, iop_file):
    pass


def parse_aux_function_two(object_id, type_id, iop_file):
    pass


def parse_aux_input_two(object_id, type_id, iop_file):
    pass


def parse_aux_control_two(object_id, type_id, iop_file):
    pass


def parse_window_mask(object_id, type_id, iop_file):
    pass


def parse_key_group(object_id, type_id, iop_file):
    pass


def parse_graphics_context(object_id, type_id, iop_file):
    pass


def parse_output_list(object_id, type_id, iop_file):
    pass


def parse_extended_input_attr(object_id, type_id, iop_file):
    pass


def parse_color_map(object_id, type_id, iop_file):
    pass


def parse_object_label_ref_list(object_id, type_id, iop_file):
    pass


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
            try:
                data = struct.unpack('<HB', self.iop_file.read(3))
                print("Print Object ID: " + str(data[0]) + " Type " + str(data[1]))
                self.parse_object(data[0], data[1], self.iop_file)
            except Exception, e:
                print e
                self.iop_file.close()
                return objects

        self.iop_file.close()
        return objects

    @staticmethod
    def parse_object(object_id, object_type, iop_file):
        return {
            0: parse_working_set,
            1: parse_data_mask,
            2: parse_alarm_mask,
            3: parse_container,
            4: parse_soft_key_mask,
            5: parse_key,
            6: parse_button,
            7: parse_input_boolean_field,
            8: parse_input_string_field,
            9: parse_input_number_field,
            10: parse_input_list_field,
            11: parse_output_string_field,
            12: parse_output_number_field,
            13: parse_line,
            14: parse_rectangle,
            15: parse_ellipse,
            16: parse_polygon,
            17: parse_meter,
            18: parse_linear_bar_graph,
            19: parse_arched_bar_graph,
            20: parse_picture_graphic,
            21: parse_number_variable,
            22: parse_string_variable,
            23: parse_font_attr_object,
            24: parse_line_attr_object,
            25: parse_fill_attr_object,
            26: parse_input_attr_object,
            27: parse_object_ptr,
            28: parse_macro,
            29: parse_aux_function,
            30: parse_aux_input,
            31: parse_aux_function_two,
            32: parse_aux_input_two,
            33: parse_aux_control_two,
            34: parse_window_mask,
            35: parse_key_group,
            36: parse_graphics_context,
            37: parse_output_list,
            38: parse_extended_input_attr,
            39: parse_color_map,
            40: parse_object_label_ref_list
        }[object_type](object_id, object_type, iop_file)