def test_complex_fields(user_advance_dataclass):
    data = {
        "name": "juan",
        "age": 20,
        "pets": ["dog"],
        "accounts": {"ing": 100},
        "has_car": True,
        "favorite_colors": "GREEN",
        "md5": b"u00ffffffffffffx",
    }

    expected_data = {
        "name": "juan",
        "age": 20,
        "pets": ["dog"],
        "accounts": {"ing": 100},
        "has_car": True,
        "favorite_colors": "GREEN",
        "md5": b"u00ffffffffffffx",
        "country": "Argentina",
        "address": None,
    }

    data_json = {
        "name": "juan",
        "age": 20,
        "pets": ["dog"],
        "accounts": {"ing": 100},
        "has_car": True,
        "favorite_colors": "GREEN",
        "md5": "u00ffffffffffffx",
        "country": "Argentina",
        "address": None,
    }

    user = user_advance_dataclass(**data)

    avro_binary = user.serialize()
    avro_json = user.serialize(serialization_type="avro-json")

    assert user_advance_dataclass.deserialize(avro_binary, create_instance=False) == expected_data
    assert (
        user_advance_dataclass.deserialize(avro_json, serialization_type="avro-json", create_instance=False)
        == expected_data
    )
    assert user.to_json() == data_json

    assert user_advance_dataclass.deserialize(avro_binary) == user
    assert user_advance_dataclass.deserialize(avro_json, serialization_type="avro-json") == user


def test_complex_fields_with_defaults(user_advance_with_defaults_dataclass):
    data = {
        "name": "juan",
        "age": 20,
    }

    expected_data = {
        "name": "juan",
        "age": 20,
        "pets": ["dog", "cat"],
        "accounts": {"key": 1},
        "has_car": False,
        "favorite_colors": "BLUE",
        "country": "Argentina",
        "address": None,
    }

    user = user_advance_with_defaults_dataclass(**data)
    expected_user = user_advance_with_defaults_dataclass(
        name="juan",
        age=20,
        favorite_colors="BLUE",
    )

    avro_binary = user.serialize()
    avro_json = user.serialize(serialization_type="avro-json")

    assert user_advance_with_defaults_dataclass.deserialize(avro_binary, create_instance=False) == expected_data
    assert (
        user_advance_with_defaults_dataclass.deserialize(
            avro_json, serialization_type="avro-json", create_instance=False
        )
        == expected_data
    )
    assert user.to_json() == expected_data

    assert user_advance_with_defaults_dataclass.deserialize(avro_binary) == expected_user
    assert user_advance_with_defaults_dataclass.deserialize(avro_json, serialization_type="avro-json") == expected_user

    # check that is possible to continue doing serialization and dedesialization operations
    expected_user.favorite_colors = "YELLOW"
    assert expected_user.serialize() == b"\x08juan(\x04\x06dog\x06cat\x00\x02\x06key\x02\x00\x00\x02\x12Argentina\x00"
    assert user.avro_schema() == expected_user.avro_schema()
