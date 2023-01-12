import pytest

from aioaprs.parsers.telemetry import parse_body_telemetry


def test_telemetry_no_seq():
    data_input: str = "T"

    with pytest.raises(ValueError):
        parse_body_telemetry(data_input)


def test_telemetry_no_telemetry():
    data_input: str = "Telemetry Message"

    with pytest.raises(ValueError):
        parse_body_telemetry(data_input)


def test_telemetry_short_seq():
    data_input: str = "T23"

    data_expected: dict = {
        "seq": 23,
        "values": []
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_seq():
    data_input: str = "T123"

    data_expected: dict = {
        "seq": 123,
        "values": []
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_seq_long_strict():
    data_input: str = "T1234"

    with pytest.raises(ValueError):
        parse_body_telemetry(data_input, strict_mode=True)


def test_telemetry_seq_long():
    data_input: str = "T1234"

    data_expected: dict = {
        "seq": 1234,
        "values": []
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_seq_invalid():
    data_input: str = "T1a"

    with pytest.raises(ValueError):
        parse_body_telemetry(data_input)


def test_telemetry_no_seq_with_sharp():
    data_input: str = "T#"

    with pytest.raises(ValueError):
        parse_body_telemetry(data_input)


def test_telemetry_short_seq_with_sharp():
    data_input: str = "T#23"

    data_expected: dict = {
        "seq": 23,
        "values": []
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_no_value_no_comma():
    data_input: str = "T#123"

    data_expected: dict = {
        "seq": 123,
        "values": []
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_no_value_with_comma():
    data_input: str = "T#123,"

    data_expected: dict = {
        "seq": 123,
        "values": [0.0]
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_one_value_no_comma():
    data_input: str = "T#123,1.20"

    data_expected: dict = {
        "seq": 123,
        "values": [1.2]
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_one_value_with_comma():
    data_input: str = "T#123,1.20,"

    data_expected: dict = {
        "seq": 123,
        "values": [1.2, 0.0]
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_two_values_with_comma():
    data_input: str = "T#123,1.20,3.40,"

    data_expected: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 0.0]
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_three_values_no_comma():
    data_input: str = "T#123,1.20,3.40,5.60"

    data_expected: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 5.6]
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_three_values_with_comma():
    data_input: str = "T#123,1.20,3.40,5.60,"

    data_expected: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 0.0]
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_four_values_no_comma():
    data_input: str = "T#123,1.20,3.40,5.60,7.80"

    data_expected: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8]
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_four_values_with_comma():
    data_input: str = "T#123,1.20,3.40,5.60,7.80,"

    data_expected: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8, 0.0]
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_no_bits_no_comma():
    data_input: str = "T#123,1.20,3.40,5.60,7.80,9.00"

    data_expected: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8, 9.0]
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_no_bits_no_comma_empty_value():
    data_input: str = "T#123,1.20,3.40,,7.80,9.00"

    data_expected: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 0.0, 7.8, 9.0]
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_no_bits_with_comma():
    data_input: str = "T#123,1.20,3.40,5.60,7.80,9.00,"

    data_expected: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8, 9.0],
        "bits": [False, False, False, False, False, False, False, False]
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_few_bits():
    data_input: str = "T#123,1.20,3.40,5.60,7.80,9.00,101"

    data_expected: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8, 9.0],
        "bits": [True, False, True, False, False, False, False, False]
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_completed():
    data_input: str = "T#123,1.20,3.40,5.60,7.80,9.00,10101010"

    data_expected: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8, 9.0],
        "bits": [True, False, True, False, True, False, True, False]
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_too_many_bits():
    data_input: str = "T#123,1.20,3.40,5.60,7.80,9.00,1010101011"

    data_expected: dict = {
        "seq": 123,
        "values": [1.2, 3.4, 5.6, 7.8, 9.0],
        "bits": [True, False, True, False, True, False, True, False]
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_completed_8bit():
    data_input: str = "T#123,123,234,122,151,0,10101010"

    data_expected: dict = {
        "seq": 123,
        "values": [123, 234, 122, 151, 0],
        "bits": [True, False, True, False, True, False, True, False]
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected


def test_telemetry_completed_some_8bit():
    data_input: str = "T#123,123,234,12.2,151,0,10101010"

    data_expected: dict = {
        "seq": 123,
        "values": [123.0, 234.0, 12.2, 151.0, 0.0],
        "bits": [True, False, True, False, True, False, True, False]
    }

    data_actual: dict = parse_body_telemetry(data_input)

    assert data_actual == data_expected
