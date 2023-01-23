from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, Tuple, Type

import iso3166

__all__ = ("ISRC",)


@dataclass
class ISRC:
    """Objectified ISRC structure defined in ISO 3901:2019

    Attributes:
        owner (str): 5-letter registrant code of issuer of ISRC, with
            first 2 characters strictly alphabetic and remaining alphanumeric
        year (int): last 2 digit of reference year (usually means recording year)
        designation (int): 5-digit identifier for recording, unique within
            above reference year.
        country (:obj:`str` or :obj:`None`): During earlier years of ISRC
            allocation, first 2 letters of registrant code was ISO 3166 country
            code. This country attribute is set if it is found. Newer allocation
            of ISRC registrant may not follow previous rule.
        raw (:obj:`str` or :obj:`None`): If ISRC is parsed via `parse` method,
            this attribute preserves the original string.
    """

    owner: str
    year: int
    designation: int
    country: Optional[iso3166.Country] = field(default=None, init=False, compare=False)
    raw: Optional[str] = field(default=None, init=False, repr=False, compare=False)

    def __post_init__(self):
        try:
            self.country = iso3166.countries.get(self.owner[:2])
        except KeyError:
            pass

    def __str__(self):
        return self.stringify(False)

    def stringify(self, separator: bool = True) -> str:
        """Print ISRC as string

        Args:
            separator (:obj:`bool`, optional): Whether hyphen should be inserted
                between segments. Defaults to True. If hyphenation is not
                intended, it is much simpler to call `str()` on the object.

        Returns:
            str: Resulting ISRC string
        """
        sep = "-" if separator else ""
        return sep.join(
            [
                self.owner[:2],
                self.owner[2:],
                "{:02d}".format(self.year),
                "{:05d}".format(self.designation),
            ]
        )

    @classmethod
    def _parse(cls, _raw: str) -> Tuple[str, int, int]:
        if not isinstance(_raw, str):
            raise TypeError("Argument must be a string")
        canon = _raw.upper()
        if canon.startswith("ISRC "):
            canon = canon[5:]
        if "-" in canon:
            (country, owner, year, desig) = canon[:15].split("-")
        else:
            (country, owner, year, desig) = (
                canon[:2],
                canon[2:5],
                canon[5:7],
                canon[7:12],
            )
        if TYPE_CHECKING:
            segment: str
            length: int
            method: str
        for (segment, length) in [(country, 2), (owner, 3), (year, 2), (desig, 5)]:
            if len(segment) != length:
                raise ValueError(
                    f'Wrong length for segment "{segment}", expected {length} characters'
                )
        for (segment, method) in [
            (country, "isalpha"),
            (owner, "isalnum"),
            (year, "isdigit"),
            (desig, "isdigit"),
        ]:
            if not segment.isascii() or not getattr(segment, method)():
                raise ValueError(f'Unexpected character found for segment "{segment}"')
        return (country + owner, int(year), int(desig))

    @classmethod
    def parse(cls: "Type[ISRC]", _raw: str) -> "ISRC":
        """Parses ISRC string into structure

        It checks for "CCXXXYYNNNNN" or "CC-XXX-YY-NNNNN" pattern
        as mandated by ISRC Handbook, optionally prefixed with "ISRC ".
        Any trailing text is ignored.

        Args:
            _raw (str): The string to be parsed

        Raises:
            TypeError: If supplied argument is not a string
            ValueError: If ISRC segments do not conform to standard

        Returns:
            ISRC: The structured object to return
        """
        owner, year, desig = cls._parse(_raw)
        result = cls(owner, year, desig)
        result.raw = _raw
        return result

    @classmethod
    def validate(cls, _raw: str) -> bool:
        """Similar to `parse` method, but only for validation purpose

        Args:
            _raw (str): The string to be validated

        Returns:
            bool: Whether string is plausible ISRC code
        """
        try:
            _ = cls._parse(_raw)
        except:
            return False
        else:
            return True

ISRC.validate('abc')
