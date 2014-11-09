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

    print("Object ID : ", object_id, ", Type ", type_id, " Background color ", background_color, " Soft key mask ",
          soft_key_mask, " Objets ", number_objects, " Macros ", number_macros)
    for obj in objects:
        print(obj)
    for macro in macros:
        print(macro)


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

    print("Object ID : ", object_id,
          ", Type ", type_id,
          " Background color ", background_color,
          " Soft key mask ", soft_key_mask,
          " Priority ", priority,
          " Acoustic Signal ", acoustic_signal,
          " Objets ", number_objects,
          " Macros ", number_macros)

    for obj in objects:
        print(obj)
    for macro in macros:
        print(macro)


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

    print("\n\tObject ID: " + str(object_id) +
          "\n\tType: " + str(type_id) +
          "\n\tWidth: " + str(width) +
          "\n\tHeight: " + str(height) +
          "\n\tHidden: " + str(hidden) +
          "\n\tObjects: " + str(number_objects) +
          "\n\tMacros: " + str(number_macros))

    for obj in objects:
        print(obj)
    for macro in macros:
        print(macro)


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

    print("\n\tObject ID: " + str(object_id) +
          "\n\tType: " + str(type_id) +
          "\n\tbackground_color: " + str(background_color) +
          "\n\tObjects: " + str(number_objects) +
          "\n\tMacros: " + str(number_macros))

    for obj in objects:
        print(obj)
    for macro in macros:
        print(macro)


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

    print("\n\tObject ID: " + str(object_id) +
          "\n\tType: " + str(type_id) +
          "\n\tWidth: " + str(width) +
          "\n\tHeight: " + str(height) +
          "\n\tbackground_color: " + str(background_color) +
          "\n\tborder_color: " + str(border_color) +
          "\n\tkey_code: " + str(key_code) +
          "\n\toptions: " + str(options) +
          "\n\tObjects: " + str(number_objects) +
          "\n\tMacros: " + str(number_macros))

    for obj in objects:
        print(obj)
    for macro in macros:
        print(macro)


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

    print("\n\tObject ID: " + str(object_id) +
          "\n\tType: " + str(type_id) +
          "\n\tbackground_color: " + str(background_color) +
          "\n\tWidth: " + str(width) +
          "\n\tforeground_color: " + str(foreground_color) +
          "\n\tvariable_reference: " + str(variable_reference) +
          "\n\tvalue: " + str(value) +
          "\n\tenabled: " + str(enabled) +
          "\n\tMacros: " + str(number_macros))

    for macro in macros:
        print(macro)


def parse_input_string_field(object_id, type_id, iop_file):
    pass


def parse_input_number_field(object_id, type_id, iop_file):
    pass


def parse_input_list_field(object_id, type_id, iop_file):
    pass


def parse_output_string_field(object_id, type_id, iop_file):
    pass


def parse_output_number_field(object_id, type_id, iop_file):
    pass


def parse_line(object_id, type_id, iop_file):
    pass


def parse_rectangle(object_id, type_id, iop_file):
    pass


def parse_ellipse(object_id, type_id, iop_file):
    pass


def parse_polygon(object_id, type_id, iop_file):
    pass


def parse_meter(object_id, type_id, iop_file):
    pass


def parse_linear_bar_graph(object_id, type_id, iop_file):
    pass


def parse_arched_bar_graph(object_id, type_id, iop_file):
    pass


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