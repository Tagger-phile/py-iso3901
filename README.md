# py-iso3901
Structured parsing of International Standard Recording Code (ISRC) in python, as defined in ISO 3901:2019.

## Usage Example

The most usual way to create object is via `ISRC.parse` method:

```pycon
>>> from iso3901 import ISRC

>>> data = ISRC.parse('GBAJY1234567')  # 'ISRC GB-AJY-12-34567' is fine too
>>> data.country.name
'United Kingdom of Great Britain and Northern Ireland'
>>> data.owner
'GBAJY'
>>> data.year
12
>>> str(data)
'GBAJY1234567'
>>> data.stringify()
'GB-AJY-12-34567'
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

## Reference

Following documents are consulted when writing code:

- [ISRC Handbook, 4th edition](https://www.ifpi.org/wp-content/uploads/2021/02/ISRC_Handbook.pdf)
- [ISRC Agency Bulletin 2015/01](https://isrc.ifpi.org/downloads/ISRC_Bulletin-2015-01.pdf)

## Q&A

1. _Is there any plan to detect modern ISRC Registrant allocations and do a mapping between newer prefixes and countries?_

   It is still open for consideration. List of currently accepted 'country codes' are [available here](https://isrc.ifpi.org/downloads/Valid_Characters.pdf).

2. _Why is there no validation for invalid registrants, such as `US-S1Z` which is mentioned in document?_

   Registrant allocation info is not public; it is held privately within allocator of each nation (and most likely International ISRC Agency itself). It is practically impossible to exhaust and blacklist all examples used in various documents on internet.

3. _Why is the year kept as integer and not python `datetime` structure?_

   In ISRC standard, only the last 2 digit of year is available. It is easier to tell the actual year in some cases, but for years like '20', it is impossible to distinguish 1920 from 2020 via ISRC alone. Acoustic recording already existed during 1920 era.
