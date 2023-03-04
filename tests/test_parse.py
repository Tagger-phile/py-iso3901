from typing import Any

import pytest

from iso3901 import ISRC
from iso3901.isrc import Allocation


@pytest.mark.parametrize("code", [
    'zzzzz1234567',
    'zzZZz1234567',
])
def test_case_insensitive(code: str):
    norm = 'ZZZZZ1234567'
    assert ISRC.parse(code) == ISRC.parse(norm)


@pytest.mark.parametrize("prefix", ['', 'ISRC '])
@pytest.mark.parametrize("code", [
    'ZZZZZ1234567',
    'ZZ-ZZZ-12-34567',
])
def test_presentation_form(prefix: str, code: str):
    assert ISRC.parse(prefix + code) == ISRC.parse('ZZZZZ1234567')


@pytest.mark.parametrize("code", [
    'ZZ-ZZZ-123-4567',
    'ZZ-ZZZ-1234567',
    'ZZZ-ZZ1-23-4567',
    'ZZ-ZZ-Z12-345-67',
])
def test_illegal_segment(code: str):
    with pytest.raises(ValueError):
        ISRC.parse(code)


@pytest.mark.parametrize("code", [
    'ZZ-ZZZ-12?34567',
    'ZZ–ZZZ-12-34567',  # first dash is \u2013
    ' ZZ-ZZZ-12-34567',
    '(ZZ-ZZZ-12-34567)',
])
def test_illegal_char(code: str):
    with pytest.raises(ValueError):
        ISRC.parse(code)


@pytest.mark.parametrize("data", [15, None, Allocation.AD])
def test_illegal_data(data: Any):
    with pytest.raises(TypeError):
        ISRC.parse(data)


@pytest.mark.parametrize("code", [
    'QX1234567890',
    'ZY-XWV-76-54321',
])
def test_illegal_prefix(code: str):
    with pytest.raises(ValueError):
        ISRC.parse(code)


@pytest.mark.parametrize("code", [
    'NLA508700208',
    'HUA251232713',
    'FROV65736517',
    'GBBBB9905305',
    'USDO19800058',
    'JPA840501147',
    'HKI198590203',
])
def test_real_world_example(code: str):
    isrc = ISRC.parse(code)
    assert isinstance(isrc, ISRC)
