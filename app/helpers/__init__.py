from typing import Type


def assign_dict_values_to_object(dictionary: dict, obj: object):
    for key, value in dictionary.items():
        if hasattr(obj, key):
            setattr(obj, key, value)
