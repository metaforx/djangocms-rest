from typing import Any, Dict, Tuple, Type, Union
from unittest import TestCase


def assert_field_types(
    test_case: TestCase,
    obj: Dict[str, Any],
    field: str,
    expected_type: Union[Type, Tuple[Type, ...]],
    obj_type: str = "object"
):
    """
    Utility function to check if a field exists and has the correct type in an object.

    Args:
        test_case: TestCase instance (self in test methods)
        obj: Dict containing the fields to check
        field: String name of the field to check
        expected_type: Type or tuple of types that are valid for this field
        obj_type: String describing the type of object being checked (for error messages)
    """
    test_case.assertIn(
        field,
        obj,
        f"Field {field} is missing in {obj_type}"
    )

    if isinstance(expected_type, tuple):
        test_case.assertTrue(
            isinstance(obj[field], expected_type),
            f"Field {field} should be one of types {expected_type}, got {type(obj[field])}"
        )
    else:
        test_case.assertIsInstance(
            obj[field],
            expected_type,
            f"Field {field} should be {expected_type}, got {type(obj[field])}"
        )
