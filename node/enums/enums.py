from enum import Enum

class Field1(str, Enum):
    field_name = 'field_1'
    value_1 = 'field_1_1'
    value_2 = 'field_1_2'

class Field2(str, Enum):
    field_name = 'field_2'
    value_1 = 'field_2_1'
    value_2 = 'field_2_2'