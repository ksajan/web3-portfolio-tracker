from typing import Any, Dict, List, Type, TypeVar

from driftpy.drift_client import PerpPosition, SpotPosition
from pydantic import BaseModel, ValidationError

from app.models.client_response_types import CustomPerpPosition, CustomSpotPosition
from app.src.logger.logger import logger


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


def convert_spot_position_to_custom_spot_position(
    spot_position: SpotPosition, data: dict
) -> CustomSpotPosition:
    spot_position_dict = convert_dataclass_to_dict(spot_position)
    for key, value in data.items():
        spot_position_dict[key] = value
    return convert_dict_to_dataclass(CustomSpotPosition, spot_position_dict)


def update_fields(instance: Any, field_name: str, field_new_value: Any):
    if hasattr(instance, field_name):
        setattr(instance, field_name, field_new_value)
    else:
        raise AttributeError(f"{instance} has no attribute {field_name}")


T = TypeVar("T", bound=BaseModel)


def filter_fields_for_pydantic_model(
    data: List[Dict[str, Any]], target_class: Type[T]
) -> List[T]:
    try:
        if not issubclass(target_class, BaseModel):
            raise ValueError(f"{target_class} is not a subclass of pydantic.BaseModel")

        filtered_data = []
        for data_dict in data:
            try:
                # Create an instance of the Pydantic model, ignoring extra fields
                model_instance = target_class(**data_dict)
                filtered_data.append(model_instance)
            except ValidationError as e:
                logger.error(f"Validation error: {e}")
                continue  # Skip invalid data_dict

        return filtered_data
    except Exception as e:
        logger.error(
            f"Error in filtering fields and transforming the Pydantic model object: {e}"
        )
        return []
