[![PyPI version](https://img.shields.io/pypi/v/iso3901.svg)](https://pypi.org/project/iso3901/)
![Supported Python](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fgithub.com%2FTagger-phile%2Fpy-iso3901%2Fraw%2Frefs%2Fheads%2Fmain%2Fpyproject.toml)
![Wheel](https://img.shields.io/pypi/wheel/iso3901.svg)

# py-iso3901
Structured parsing of ISRC ([International Standard Recording Code](https://isrc.ifpi.org/en/)) in python, as defined in ISO 3901:2019.

## Install

`pip install -U iso3901`

## Usage Example

The most usual way to create object is via `ISRC.parse` method:

```pycon
>>> from iso3901 import ISRC

>>> data = ISRC.parse('ISRC GB-AJY-12-34567')
>>> data == ISRC.parse('GBAJY1234567')  # Same as compact form
True
>>> data.country.name
'United Kingdom of Great Britain and Northern Ireland'
>>> data.owner
'GBAJY'
>>> data.prefix
'GB'
>>> data.year
12
>>> data.designation
34567
>>> data.agency
'PPL UK'
>>> str(data)
'GBAJY1234567'
>>> data.stringify()
'GB-AJY-12-34567'
>>> data.raw  # Get back the original unparsed string
'ISRC GB-AJY-12-34567'
```

ISRC agency prefix validation is now supported since version `0.3.0`:
```pycon
>>> data = ISRC.parse('QMDA71418090')
>>> data.country.name
'United States of America'
>>> data.country.alpha2, data.prefix
('US', 'QM')
>>> data.agency
'RIAA'
>>> data.prefix_retired
False
>>> data = ISRC.parse('ZZZZZ1234567')
>>> data.country.name
'Worldwide'
>>> data.country.alpha2
''
>>> data.agency
'International ISRC Registration Authority'
```

`validate()` method is provided for simple validation:

```pycon
>>> ISRC.validate('aa-xyz-01-23456')
True
>>> ISRC.validate('aa-xyz-012-3456')
False
```

If desired, ISRC prefix allocation status and agency names can be accessed directly. They are exported directly as standard [`enum`](https://docs.python.org/3/library/enum.html):

```pycon
>>> from iso3901 import Agency, Allocation
>>> Agency.DK
<Agency.DK: 'GRAMEK DK'>
>>> Agency.DK == Agency['DK']
True
>>> Allocation.DK
<Allocation.DK: ......>
>>> Allocation.DK.agency == Agency.DK
True
>>> Allocation['DK'].country
Country(name='Denmark', alpha2='DK', alpha3='DNK', numeric='208', apolitical_name='Denmark')
>>> Allocation['XY']
Traceback (most recent call last):
......
KeyError: 'XY'
```

Finally, it is noteworthy that prefix allocation date is available as [python date](https://docs.python.org/3/library/datetime.html#date-objects) constant:

```pycon
>>> import iso3901
>>> iso3901.DB_DATE
datetime.date(2025, 11, 4)
```

## Caveats

In the _very rare_ case that no data validation is desired, it is possible to initiate object directly. Be warned that supplying free form data would result in illegal ISRC code:

```pycon
>>> data = ISRC('GBAJY', 12, 34567)
>>> str(data)
'GBAJY1234567'
>>> data = ISRC('Some Owner', 123, 456789)
>>> str(data)
'Some Owner123456789'
```

In case ISRC prefix isn't a legal allocated prefix, `.country` and `.agency` properties become `None`:

```pycon
>>> data = ISRC('ZYXWV', 12, 34567)  # Exception if using ISRC.parse()
>>> type(data.country)
<class 'NoneType'>
>>> type(data.agency)
<class 'NoneType'>
```

## Reference

Following documents are consulted when writing code:

- [ISRC Handbook, 4th edition](https://www.ifpi.org/wp-content/uploads/2021/02/ISRC_Handbook.pdf)
- [ISRC Agency Bulletin 2015/01](https://isrc.ifpi.org/downloads/ISRC_Bulletin-2015-01.pdf)
- [Newest valid ISRC prefixes][valid-char-pdf]

[valid-char-pdf]: https://isrc.ifpi.org/images/downloads/Valid_Characters_in_the_ISRC_Prefix.pdf

## Q&A

1. _Why is there no validation for invalid registrants, such as `US-S1Z` which is mentioned in above documents?_

   It is true that ISRC agencies has been repeatedly mentioning that some codes were "for illustrative purposes in documentation and training materials", and therefore are known invalid codes. However, registrant allocation info is not public; it is held privately within allocator of each nation (and most likely International ISRC Agency itself). It is practically impossible to exhaust and blacklist all examples used in various documents on internet. In single word: _unenforceable_.

2. _Why is the year kept as integer and not python `datetime` structure?_

   In ISRC standard, only the last 2 digit of year is available. It is easier to tell the actual year in some cases, but for years like '20', it is impossible to distinguish 1920 from 2020 via ISRC alone. Acoustic recording already existed around 1900; and some ancient recordings are known to directly use recording year (20's) in ISRC, such as [Jimmie Rodgers'](https://open.spotify.com/album/6TXhBKNTITmOTWCbHaQKIG).

3. _The "country code" `QM` is already known for use in United States, and `ZZ` reserved for International ISRC Agency, as described in various ISRC Bulletins. Is there any plan to add modern ISRC Registrant allocations and do a mapping between newer prefixes and countries?_

   Actually, the newest bulletin dated 2015 had pushed a new standard that no more binds country with the 2-letter prefix. That said, since `0.3.0` version, country code is validated to conform to [newest published prefixes][valid-char-pdf] &mdash; Nov 2025 as of writing. There exists quite a number of countries unmanaged by any recording industry agencies, so validation still provides some benefit.

## Alternatives

If one only needs to check for validity of ISRC string, and no objectified access of various segments is needed, other python modules exist to provide such validation routine. For example:

- [python-stdnum](https://pypi.org/project/python-stdnum/)
- [py.validator](https://pypi.org/project/py-validator/)

However, so far this package provides the most rigorous validation among all of the choices, as it contains the newest country prefixes mapping.
