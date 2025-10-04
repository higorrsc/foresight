import uuid

import pytest

from src.core.domain._shared import EntityValidationError
from src.core.domain.entities import Area


class TestCreateAreaEntity:
    """
    Test suite for the Area entity.
    """

    def test_name_is_required(self):
        """
        Test that creating an Area without a description raises a ValueError.
        """

        with pytest.raises(
            EntityValidationError,
            match="Description must be a non-empty string.",
        ):
            Area(description="")

    def test_name_cannot_be_longer_than_100_characters(self):
        """
        Test that creating an Area with a description longer
        than 100 characters raises a ValueError.
        """

        long_description = "A" * 101  # 101 characters long

        with pytest.raises(
            EntityValidationError,
            match="Description must be at most 100 characters long.",
        ):
            Area(description=long_description)

    def test_id_is_auto_generated(self):
        """
        Test that the Area entity automatically generates a unique ID.
        """

        area1 = Area(description="Area 1")
        area2 = Area(description="Area 2")

        assert area1.id is not None
        assert area2.id is not None
        assert area1.id != area2.id

    def test_area_creation(self):
        """
        Test that an Area entity is created successfully with valid data.
        """

        description = "Test Area"
        area = Area(description=description)

        assert area.description == description
        assert area.id is not None

    def test_area_representation(self):
        """
        Test the __repr__ method of the Area entity.
        """

        description = "Test Area"
        area = Area(description=description)

        expected_repr = f"<Area {description} ({area.id})>"
        assert repr(area) == expected_repr

    def test_area_str(self):
        """
        Test the __str__ method of the Area entity.
        """

        description = "Test Area"
        area = Area(description=description)

        expected_str = f"Area(id={area.id}, description='{description}')"
        assert str(area) == expected_str


class TestUpdateAreaEntity:
    """
    Test suite for updating the description of the Area entity.
    """

    def test_update_area_description(self):
        """
        Test updating the description of the Area entity.
        """

        area = Area(description="Initial Description")
        new_description = "Updated Description"
        area.update_area(new_description)

        assert area.description == new_description

    def test_update_area_with_empty_description_raises_value_error(self):
        """
        Test that updating the Area with an empty description raises a EntityValidationError.
        """

        area = Area(description="Initial Description")

        with pytest.raises(
            EntityValidationError,
            match="Description must be a non-empty string.",
        ):
            area.update_area("")

    def test_update_area_with_long_description_raises_value_error(self):
        """
        Test that updating the Area with a description longer
        than 100 characters raises a EntityValidationError.
        """

        area = Area(description="Initial Description")
        long_description = "A" * 101  # 101 characters long

        with pytest.raises(
            EntityValidationError,
            match="Description must be at most 100 characters long.",
        ):
            area.update_area(long_description)


class TestAreaEquality:
    """
    Test suite for equality comparison of Area entities.
    """

    def test_areas_with_same_id_are_equal(self):
        """
        Test that two Area entities with the same ID are considered equal.
        """
        area_id = uuid.uuid4()
        area1 = Area(description="Area 1", id=area_id)
        area2 = Area(description="Area 2", id=area_id)

        assert area1 == area2

    def test_areas_with_different_ids_are_not_equal(self):
        """
        Test that two Area entities with different IDs are not considered equal.
        """

        area1 = Area(description="Area 1")
        area2 = Area(description="Area 2")

        assert area1 != area2

    def test_area_not_equal_to_different_type(self):
        """
        Test that an Area entity is not equal to an object of a different type.
        """

        area = Area(description="Area 1")
        non_area_object = "Not an Area"

        assert area != non_area_object
