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
    soft_key = struct.unpack('<BBB', iop_file.read(3))
    background_color = soft_key[0]
    number_objects = soft_key[1]
    number_macros = soft_key[2]
    objects = []
    macros = []

    for _ in range(number_objects):
        a = struct.unpack('<Hhh', iop_file.read(6))
        objects.append(ObjectLocation(a[0], a[1], a[2]))

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_key(object_id, type_id, iop_file):
    pass


def parse_button(object_id, type_id, iop_file):
    button = struct.unpack('<HHBBBBBB', iop_file.read(10))
    width = button[0]
    height = button[1]
    background_color = button[2]
    border_color = button[3]
    key_code = button[4]
    options = button[5]
    number_objects = button[6]
    number_macros = button[7]
    objects = []
    macros = []

    for _ in range(number_objects):
        a = struct.unpack('<Hhh', iop_file.read(6))
        objects.append(ObjectLocation(a[0], a[1], a[2]))

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_input_boolean_field(object_id, type_id, iop_file):
    boolean_input = struct.unpack('<BHHHBBB', iop_file.read(10))
    background_color = boolean_input[0]
    width = boolean_input[1]
    foreground_color = boolean_input[2]
    variable_reference = boolean_input[3]
    value = boolean_input[4]
    enabled = boolean_input[5]
    number_macros = boolean_input[6]
    macros = []

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_input_string_field(object_id, type_id, iop_file):
    input_string = struct.unpack('<HHBHHBHBB', iop_file.read(14))
    width = input_string[0]
    height = input_string[1]
    background_color = input_string[2]
    font_attr = input_string[3]
    input_attr = input_string[4]
    options = input_string[5]
    variable_ref = input_string[6]
    justification = input_string[7]
    length = input_string[8]
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
    input_number = struct.unpack('<HHBHBHLLLlfBBBBB', iop_file.read(35))
    width = input_number[0]
    height = input_number[1]
    background_color = input_number[2]
    font_attr = input_number[3]
    options = input_number[4]
    variable_ref = input_number[5]
    value = input_number[6]
    min_value = input_number[7]
    max_value = input_number[8]
    offset = input_number[9]
    scale = input_number[10]
    num_decimals = input_number[11]
    format = input_number[12]
    justification = input_number[13]
    options_2 = input_number[14]
    number_macros = input_number[15]
    macros = []

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_input_list_field(object_id, type_id, iop_file):
    pass


def parse_output_string_field(object_id, type_id, iop_file):
    pass


def parse_output_number_field(object_id, type_id, iop_file):
    pass


def parse_line(object_id, type_id, iop_file):
    line = struct.unpack('<HHHBB', iop_file.read(8))
    line_attr = line[0]
    width = line[1]
    height = line[2]
    line_direction = line[3]
    number_macros = line[4]
    macros = []

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_rectangle(object_id, type_id, iop_file):
    rectangle = struct.unpack('<HHHBHB', iop_file.read(10))
    line_attr = rectangle[0]
    width = rectangle[1]
    height = rectangle[2]
    line_suppression = rectangle[3]
    fill_attr = rectangle[4]
    number_macros = rectangle[5]
    macros = []

    for _ in range(number_macros):
        a = struct.unpack('<BB', iop_file.read(2))
        macros.append(MacroObject(a[0], a[1]))


def parse_ellipse(object_id, type_id, iop_file):
    ellipse = struct.unpack('<HHHBBBHB', iop_file.read(12))
    line_attr = ellipse[0]
    width = ellipse[1]
    height = ellipse[2]
    ellipse_type = ellipse[3]
    start_angle = ellipse[4]
    end_angle = ellipse[5]
    fill_attr = ellipse[6]
    number_macros = ellipse[7]
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
    parsed_object = struct.unpack('<HHBBBBHHHHHHB', iop_file.read(21))



def parse_picture_graphic(object_id, type_id, iop_file):
    pass


def parse_number_variable(object_id, type_id, iop_file):
    pass


def parse_string_variable(object_id, type_id, iop_file):
    pass


def parse_font_attr_object(object_id, type_id, iop_file):
    pass


def parse_line_attr_object(object_id, type_id, iop_file):
    pass


def parse_fill_attr_object(object_id, type_id, iop_file):
    pass


def parse_input_attr_object(object_id, type_id, iop_file):
    pass


def parse_object_ptr(object_id, type_id, iop_file):
    pass


def parse_macro(object_id, type_id, iop_file):
    temp = struct.unpack('<H', iop_file.read(2))
    command_length = temp[0]
    # TODO: Fix command parsing
    commands = iop_file.read(command_length)

    print("Object ID : ", object_id,
          ", Type ", type_id,
          " command_length ", command_length,
          " UNSUPPORTED PARSING OF COMMAND YET")


def parse_aux_function(object_id, type_id, iop_file):
    pass


def parse_aux_input(object_id, type_id, iop_file):
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
            data = struct.unpack('<HB', self.iop_file.read(3))
            print("Print Object ID: " + str(data[0]) + " Type " + str(data[1]))
            self.parse_object(data[0], data[1], self.iop_file)

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
            30: parse_aux_input
        }[object_type](object_id, object_type, iop_file)