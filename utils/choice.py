from enum import Enum, unique

@unique
class Choice(Enum):
    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)

    @classmethod
    def name_from_value(cls, value):
        for item in cls:
            if item.value == value:
                return item.name

        return ""
