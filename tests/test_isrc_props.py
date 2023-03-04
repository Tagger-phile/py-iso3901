import pytest

from iso3901 import ISRC, Agency


def test_round_trip():
    code = 'ZZZZZ1234567'
    assert str(ISRC.parse(code)) == code

def test_round_trip_2():
    code = 'ZZ-ZZZ-12-34567'
    assert ISRC.parse(code).stringify() == code

@pytest.mark.parametrize("code", [
    'zz-zzz-12-34567',
    'ISRC ZZ-ZZZ-12-34567',
])
def test_prop_raw(code: str):
    isrc = ISRC.parse(code)
    assert isrc.raw == code

def test_prop_prefix():
    code = 'ZZ-ZZZ-12-34567'
    isrc = ISRC.parse(code)
    assert isrc.prefix == code[:2]

def test_prop_country():
    code = 'ISRC ZZ-ZZZ-12-34567'
    isrc = ISRC.parse(code)
    assert isrc.country is not None
    assert isrc.country.name == 'Worldwide'

def test_prop_agency():
    code = 'ISRC ZZ-ZZZ-12-34567'
    isrc = ISRC.parse(code)
    assert isrc.agency == Agency.IIRA.value

def test_good_isrc_construct():
    isrc_good = ISRC.parse('ZZZZZ1234567')
    isrc_custom = ISRC('ZZZZZ', 12, 34567)
    assert isrc_good == isrc_custom
    assert isrc_custom.country is not None
    assert isrc_custom.agency is not None

def test_bad_isrc_construct():
    code = 'QX1234567890'
    with pytest.raises(ValueError):
        ISRC.parse(code)
    isrc_bad = ISRC('QX123', 45, 67890)
    assert isrc_bad.country is None
    assert isrc_bad.agency is None
