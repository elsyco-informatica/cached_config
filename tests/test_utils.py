from cached_config.utils import hex_int_or_none, int_or_none


def test_int_or_none():
    assert int_or_none(None) is None
    assert int_or_none("") is None
    assert int_or_none("1.34") is None
    assert int_or_none("true") is None
    assert int_or_none("12") == 12


def test_hex_int_or_none():
    assert hex_int_or_none(None) is None
    assert hex_int_or_none("") is None
    assert hex_int_or_none("1.34") is None
    assert hex_int_or_none("true") is None
    assert hex_int_or_none("12") == 18
    assert hex_int_or_none("0x01") == 1
    assert hex_int_or_none("0xA1") == 161
