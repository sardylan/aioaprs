import pytest

from aioaprs.parsers.message import parse_body_message


def test_parser_message_none():
    data_input: str = None

    with pytest.raises(ValueError):
        parse_body_message(data_input)


def test_parser_message_empty():
    data_input: str = ":"

    with pytest.raises(ValueError):
        parse_body_message(data_input)


def test_parser_message_no_call():
    data_input: str = ":"

    with pytest.raises(ValueError):
        parse_body_message(data_input)


def test_parser_message_empty_call():
    data_input: str = "::"

    with pytest.raises(ValueError):
        parse_body_message(data_input)


def test_parser_message_wrong_length_call():
    data_input: str = ":ABC:"

    with pytest.raises(ValueError):
        parse_body_message(data_input)


def test_parser_message_no_call_ending():
    data_input: str = ":ABC123DEF"

    with pytest.raises(ValueError):
        parse_body_message(data_input)


def test_parser_message_trimmed_call_empty_message():
    data_input: str = ":ABC123   :"

    data_expected: dict = {
        "addressee": "ABC123",
        "message": ""
    }

    data_actual: dict = parse_body_message(data_input)

    assert data_actual == data_expected


def test_parser_message_empty_message():
    data_input: str = ":ABC123DEF:"

    data_expected: dict = {
        "addressee": "ABC123DEF",
        "message": ""
    }

    data_actual: dict = parse_body_message(data_input)

    assert data_actual == data_expected


def test_parser_message_some_message():
    data_input: str = ":ABC123DEF:MESSAGE text"

    data_expected: dict = {
        "addressee": "ABC123DEF",
        "message": "MESSAGE text"
    }

    data_actual: dict = parse_body_message(data_input)

    assert data_actual == data_expected


def test_parser_message_some_message_with_spaces():
    data_input: str = ":ABC123DEF:MESSAGE text  "

    data_expected: dict = {
        "addressee": "ABC123DEF",
        "message": "MESSAGE text"
    }

    data_actual: dict = parse_body_message(data_input)

    assert data_actual == data_expected


def test_parser_message_some_message_with_initial_spaces():
    data_input: str = ":ABC123DEF:  MESSAGE text"

    data_expected: dict = {
        "addressee": "ABC123DEF",
        "message": "MESSAGE text"
    }

    data_actual: dict = parse_body_message(data_input)

    assert data_actual == data_expected


def test_parser_message_telemetry_parm():
    data_input: str = ":N0QBF-11V:PARM.Battery,Btemp,ATemp,Pres,Alt,Camra,Chut,Sun,10m,ATV"

    data_expected: dict = {
        "addressee": "N0QBF-11V",
        "message": "PARM.Battery,Btemp,ATemp,Pres,Alt,Camra,Chut,Sun,10m,ATV",
        "telemetry_data": {
            "type": "PARM",
            "items": ["Battery", "Btemp", "ATemp", "Pres", "Alt", "Camra", "Chut", "Sun", "10m", "ATV"]
        }
    }

    data_actual: dict = parse_body_message(data_input)

    assert data_actual == data_expected


def test_parser_message_telemetry_unit():
    data_input: str = ":N0QBF-11V:UNIT.v/100,deg.F,deg.F,Mbar,Kft,Click,OPEN,on,on,hi"

    data_expected: dict = {
        "addressee": "N0QBF-11V",
        "message": "UNIT.v/100,deg.F,deg.F,Mbar,Kft,Click,OPEN,on,on,hi",
        "telemetry_data": {
            "type": "UNIT",
            "items": ["v/100", "deg.F", "deg.F", "Mbar", "Kft", "Click", "OPEN", "on", "on", "hi"]
        }
    }

    data_actual: dict = parse_body_message(data_input)

    assert data_actual == data_expected


def test_parser_message_telemetry_eqns():
    data_input: str = ":N0QBF-11V:EQNS.0,5.2,0,0,.53,-32,3,4.39,49,-32,3,18,1,2,3"

    data_expected: dict = {
        "addressee": "N0QBF-11V",
        "message": "EQNS.0,5.2,0,0,.53,-32,3,4.39,49,-32,3,18,1,2,3",
        "telemetry_data": {
            "type": "EQNS",
            "items": ["0", "5.2", "0", "0", ".53", "-32", "3", "4.39", "49", "-32", "3", "18", "1", "2", "3"],
            "equations": [
                {"a": 0.0, "b": 5.2, "c": 0.0},
                {"a": 0.0, "b": 0.53, "c": -32.0},
                {"a": 3.0, "b": 4.39, "c": 49.0},
                {"a": -32.0, "b": 3.0, "c": 18.0},
                {"a": 1.0, "b": 2.0, "c": 3.0}
            ]
        }
    }

    data_actual: dict = parse_body_message(data_input)

    assert data_actual == data_expected


def test_parser_message_telemetry_bits():
    data_input: str = ":N0QBF-11V:BITS.10110000,N0QBF’s Big Balloon"

    data_expected: dict = {
        "addressee": "N0QBF-11V",
        "message": "BITS.10110000,N0QBF’s Big Balloon",
        "telemetry_data": {
            "type": "BITS",
            "items": ["10110000", "N0QBF’s Big Balloon"],
            "bits": [True, False, True, True, False, False, False, False],
            "project_name": "N0QBF’s Big Balloon"
        }
    }

    data_actual: dict = parse_body_message(data_input)

    assert data_actual == data_expected
