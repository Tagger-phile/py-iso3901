from iso3166 import Country

from iso3901 import Agency, Allocation


def test_attributes_exist():
    assert all(isinstance(a.agency, Agency) for a in Allocation)
    assert all(isinstance(a.country, Country) for a in Allocation)

def test_worldwide_entries():
    entry = Allocation.ZZ
    assert entry.agency == Agency.IIRA
    assert entry.country.name == 'Worldwide'

    entry2 = Allocation['TC']
    assert entry2.agency == Agency.TC
    assert entry2.country == entry.country

def test_country_has_multi():
    for code in ('BC', 'BK', 'BP', 'BX'):
        assert Allocation[code].agency == Allocation.BR.agency
        assert Allocation[code].country == Allocation.BR.country

def test_shared_agency():
    for code in ('FJ', 'TO'):
        assert Allocation[code].agency == Allocation.NZ.agency
        assert Allocation[code].country != Allocation.NZ.country
