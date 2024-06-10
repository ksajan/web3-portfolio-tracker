from dataclasses import is_dataclass
from typing import Any, Dict, List, TypeVar

from driftpy.drift_client import PerpPosition

from app.models.positions import CustomPerpPosition


def convert_dataclass_to_dict(dataclass_object):
    return dataclass_object.__dict__


def convert_dict_to_dataclass(dataclassObject, data):
    return dataclassObject(**data)


def convert_perp_position_to_response_perp_position(
    perp_position: PerpPosition, data: dict
) -> CustomPerpPosition:
    perp_position_dict = convert_dataclass_to_dict(perp_position)
    for key, value in data.items():
        perp_position_dict[key] = value
    return convert_dict_to_dataclass(CustomPerpPosition, perp_position_dict)


def update_fields(instance: Any, field_name: str, field_new_value: Any):
    if hasattr(instance, field_name):
        setattr(instance, field_name, field_new_value)
    else:
        raise AttributeError(f"{instance} has no attribute {field_name}")


T = TypeVar("T")


def filter_fields_for_dataclass(data: List[Dict[str, Any]], target_class: T) -> List[T]:
    if not is_dataclass(target_class):
        raise ValueError(f"{target_class} is not a dataclass")

    target_fields = target_class.__dataclass_fields__.keys()
    filtered_data = []
    for data_dict in data:
        filtered_dict = {
            key: value for key, value in data_dict.items() if key in target_fields
        }
        filtered_data.append(convert_dict_to_dataclass(target_class, filtered_dict))
    return filtered_data
