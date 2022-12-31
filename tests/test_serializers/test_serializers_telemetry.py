from serializers.telemetry import serialize_body_telemetry


def test_telemetry_no_values():
    data_input: dict = {
        "seq": 123,
    }

    data_expected: str = "T#123"

    data_actual: str = serialize_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_no_values_with_empty_bits():
    data_input: dict = {
        "seq": 123,
        "bits": []
    }

    data_expected: str = "T#123"

    data_actual: str = serialize_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_no_values_with_some_bits():
    data_input: dict = {
        "seq": 123,
        "bits": [True, True]
    }

    data_expected: str = "T#123"

    data_actual: str = serialize_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_empty_values():
    data_input: dict = {
        "seq": 123,
        "values": []
    }

    data_expected: str = "T#123"

    data_actual: str = serialize_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_empty_values_empty_bits():
    data_input: dict = {
        "seq": 123,
        "values": [],
        "bits": []
    }

    data_expected: str = "T#123"

    data_actual: str = serialize_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_empty_values_some_bits():
    data_input: dict = {
        "seq": 123,
        "values": [],
        "bits": [False, True]
    }

    data_expected: str = "T#123"

    data_actual: str = serialize_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_one_value():
    data_input: dict = {
        "seq": 123,
        "values": [1.2]
    }

    data_expected: str = "T#123,1.20"

    data_actual: str = serialize_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_one_value_with_bits():
    data_input: dict = {
        "seq": 123,
        "values": [1.2],
        "bits": [True, False, True]
    }

    data_expected: str = "T#123,1.20"

    data_actual: str = serialize_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_two_values():
    data_input: dict = {
        "seq": 123,
        "values": [1.2, 3.4]
    }

    data_expected: str = "T#123,1.20,3.40"

    data_actual: str = serialize_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_two_values_with_bits():
    data_input: dict = {
        "seq": 123,
        "values": [1.2, 3.4],
        "bits": [True, False, True]
    }

    data_expected: str = "T#123,1.20,3.40"

    data_actual: str = serialize_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_three_values():
    data_input: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 5.6]
    }

    data_expected: str = "T#123,1.20,3.40,5.60"

    data_actual: str = serialize_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_three_values_with_bits():
    data_input: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 5.6],
        "bits": [True, False, True]
    }

    data_expected: str = "T#123,1.20,3.40,5.60"

    data_actual: str = serialize_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_four_values():
    data_input: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8],
    }

    data_expected: str = "T#123,1.20,3.40,5.60,7.80"

    data_actual: str = serialize_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_four_values_with_bits():
    data_input: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8],
        "bits": [True, False, True]
    }

    data_expected: str = "T#123,1.20,3.40,5.60,7.80"

    data_actual: str = serialize_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_all_values_no_bits():
    data_input: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8, 9.0]
    }

    data_expected: str = "T#123,1.20,3.40,5.60,7.80,9.00"

    data_actual: str = serialize_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_only_five_values():
    data_input: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8, 9.0, 10.1]
    }

    data_expected: str = "T#123,1.20,3.40,5.60,7.80,9.00"

    data_actual: str = serialize_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_no_bits():
    data_input: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8, 9.0],
    }

    data_expected: str = "T#123,1.20,3.40,5.60,7.80,9.00"

    data_actual: str = serialize_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_some_bits():
    data_input: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8, 9.0],
        "bits": [True, False, True, False, True, False, True, False]
    }

    data_expected: str = "T#123,1.20,3.40,5.60,7.80,9.00,10101010"

    data_actual: str = serialize_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_all_bits():
    data_input: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8, 9.0],
        "bits": [True, False, True, False, True, False, True, False]
    }

    data_expected: str = "T#123,1.20,3.40,5.60,7.80,9.00,10101010"

    data_actual: str = serialize_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_too_much_bits():
    data_input: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8, 9.0],
        "bits": [True, False, True, False, True, False, True, False, True]
    }

    data_expected: str = "T#123,1.20,3.40,5.60,7.80,9.00,10101010"

    data_actual: str = serialize_body_telemetry(data_input)

    assert data_actual == data_expected
