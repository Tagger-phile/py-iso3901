# py-iso3901
Structured parsing of [International Standard Recording Code](https://isrc.ifpi.org/en/) (ISRC) in python, as defined in ISO 3901:2019.

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
>>> data.year
12
>>> data.designation
34567
>>> str(data)
'GBAJY1234567'
>>> data.stringify()
'GB-AJY-12-34567'
>>> data.raw  # Get back the original unparsed string
'ISRC GB-AJY-12-34567'
```

`validate()` method is provided for simple validation:

```pycon
>>> ISRC.validate('isrc aa-xyz-01-23456')
True
>>> ISRC.validate('aa-xyz-012-3456')
False
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

In case ISRC code does not start with a proper ISO 3166 2-letter country code, `.country` attribute would be `None`:

```pycon
>>> data = ISRC.parse('QMDA71418090')
>>> data.owner
'QMDA7'
>>> type(data.country)
<class 'NoneType'>
```

## Reference

Following documents are consulted when writing code:

- [ISRC Handbook, 4th edition](https://www.ifpi.org/wp-content/uploads/2021/02/ISRC_Handbook.pdf)
- [ISRC Agency Bulletin 2015/01](https://isrc.ifpi.org/downloads/ISRC_Bulletin-2015-01.pdf)

## Q&A

1. _The "country code" `QM` is already known for use in United States, and `ZZ` reserved for International ISRC Agency, as described in various ISRC Bulletins. Why aren't they detected? Is there any plan to add modern ISRC Registrant allocations and do a mapping between newer prefixes and countries?_

   Actually, the newest bulletin dated 2015 had pushed a new standard that no more binds country with the 2-letter prefix. That said, it is still open for consideration. List of currently accepted 'country codes' are [available here](https://isrc.ifpi.org/downloads/Valid_Characters.pdf).

2. _Why is there no validation for invalid registrants, such as `US-S1Z` which is mentioned in above documents?_

   Registrant allocation info is not public; it is held privately within allocator of each nation (and most likely International ISRC Agency itself). It is practically impossible to exhaust and blacklist all examples used in various documents on internet.

3. _Why is the year kept as integer and not python `datetime` structure?_

   In ISRC standard, only the last 2 digit of year is available. It is easier to tell the actual year in some cases, but for years like '20', it is impossible to distinguish 1920 from 2020 via ISRC alone. Acoustic recording already existed during 1920 era.

## Alternatives

If one only needs to check for validity of ISRC string, and no objectified access of various segments is needed, other python modules exist to provide such validation routine. For example:

- [python-stdnum](https://pypi.org/project/python-stdnum/)
- [py.validator](https://pypi.org/project/py-validator/)

Our `ISRC` class also provides a `validate()` method as well.
