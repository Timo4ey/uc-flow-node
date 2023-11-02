from typing import Literal
from pydantic import BaseModel, root_validator, Field, validator
import re


class SumUp(BaseModel):
    num_1: str = Field(min_length=1)
    num_2: int
    switcher: Literal["string", "number"]

    @validator("num_1")
    def validate_num1(cls, value: str):
        strings = re.findall("\D+", value.lower())
        if strings:
            raise ValueError("Field must contains only digits")
        return value

    def _num1_to_int(self):
        return int(self.num_1)

    def sum_of_digits(self):
        return self._num1_to_int() + self.num_2