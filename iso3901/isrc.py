from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, NamedTuple, Optional, Tuple, Type

import iso3166

__all__ = ("ISRC", "Agency", "Allocation")

#
# All allocation data taken from
# https://isrc.ifpi.org/downloads/Valid_Characters.pdf
# Last updated: 2023-02-08
#


class Agency(str, enum.Enum):
    """Name of national or worldwide agency responsible for allocating
    ISRC prefixes
    """

    IIRA = "International ISRC Registration Authority"
    AR = "CAPIF"
    AT = "LSG"
    AU = "ARIA"
    BB = "COSCAP"
    BE = "SIMIM"
    BR = "Pro‐música Brazil"
    CA = "Connect"
    CH = "IFPI Switzerland"
    CL = "IFPI Chile"
    CZ = "INTERGRAM"
    DE = "BVMI"
    DK = "GRAMEK DK"
    DO = "SODINPRO"
    EE = "EFU"
    ES = "AGEDI"
    FI = "IFPI Finland"
    FR = "SCPP"
    GB = "PPL UK"
    GR = "IFPI Greece"
    HK = "IFPI Hong Kong"
    ID = "ASIRI"
    IE = "PPI"
    IL = "IFPI"
    IN = "IMI"
    IS = "SFH"
    IT = "FIMI"
    JM = "JAMMS"
    JP = "RIAJ"
    KR = "KMCA"
    LT = "AGATA"
    LV = "LaIPA"
    MX = "AMPROFON"
    MY = "RIM"
    NL = "SENA"
    NO = "Gramo"
    NZ = "Recorded Music NZ"
    PA = "PRODUCE"
    PE = "UNIMPRO"
    PH = "PARI"
    PL = "ZPAV"
    PT = "AFP"
    PY = "SGP"
    RO = "UPFR"
    SE = "IFPI Sweden"
    SG = "Recording Industry Association Singapore"
    SK = "SLOVGRAM"
    TC = "TuneCore Inc"
    TH = "TECA"
    TR = "MU‐YAP"
    TT = "COTT"
    TW = "RIT"
    UA = "Ukrainian Music Alliance"
    US = "RIAA"
    UY = "Camara Uruguaya Del Disco"
    ZA = "RISA"

    if TYPE_CHECKING:

        @property
        def value(self) -> str:
            ...


#
# Python ISO 3166 record eliminates all ceased countries,
# so we need to recreate ourselves. Also create entry for
# Worldwide, for API coherence.
#
class PseudoCountry(iso3166.Country):
    """Ceased entities or non-countries used in ISO 3901"""


_Yugoslavia = PseudoCountry(
    "Yugoslavia",
    "YU",
    "YUG",
    "891",
    "Yugoslavia",
)
"Prefix allocated to producers in Yugoslavia (before 2003)"

_SerbiaMontenegro = PseudoCountry(
    "Serbia and Montenegro",
    "CS",
    "SCG",
    "891",
    "Serbia and Montenegro",
)
"Prefix allocated to producers in Serbia & Montenegro (before 2006)"

_Worldwide = PseudoCountry("Worldwide", "", "", "", "Worldwide")
"Fake country indicating certain ISRC prefix is allocated worldwide"


class _AllocationType(NamedTuple):
    agency: Agency
    country: iso3166.Country


_alpha2 = iso3166.countries_by_alpha2

# fmt: off
class Allocation(_AllocationType, enum.Enum):
    """Current allocation status for ISRC prefixes

    Parameters
    ----------
    agency : `Agency`
        Agency enum responsible for allocation of concerned ISRC prefix
    country : `iso3166.Country`
        The country using concerned ISRC prefix
    """
    # IIRA Reserved
    # XXX In ISO 3166, country code "TC" represents Turks and Caicos Islands.
    # However, IIRA has allocated "TC" prefix under TuneCore Inc.,
    # and moved potential uses of Turks and Caicos Islands under one
    # of IIRA's own reserved prefix ("DG"). There is not enough info
    # to conclude if such confusion is intentional or an oversight.
    CP = Agency.IIRA, _Worldwide
    DG = Agency.IIRA, _Worldwide
    ZZ = Agency.IIRA, _Worldwide
    TC = Agency.TC  , _Worldwide

    # Brazil
    BC = Agency.BR  , _alpha2["BR"]
    BK = Agency.BR  , _alpha2["BR"]
    BP = Agency.BR  , _alpha2["BR"]
    BR = Agency.BR  , _alpha2["BR"]
    BX = Agency.BR  , _alpha2["BR"]

    # Denmark
    DK = Agency.DK  , _alpha2["DK"]
    FO = Agency.DK  , _alpha2["DK"]
    GL = Agency.DK  , _alpha2["DK"]

    # UK
    GB = Agency.GB  , _alpha2["GB"]
    GX = Agency.GB  , _alpha2["GB"]
    UK = Agency.GB  , _alpha2["GB"]

    # US
    QM = Agency.US  , _alpha2["US"]
    QZ = Agency.US  , _alpha2["US"]
    US = Agency.US  , _alpha2["US"]

    # Canada
    CA = Agency.CA  , _alpha2["CA"]
    CB = Agency.CA  , _alpha2["CA"]

    # France
    FR = Agency.FR  , _alpha2["FR"]
    FX = Agency.FR  , _alpha2["FR"]

    # South Africa
    ZA = Agency.ZA  , _alpha2["ZA"]
    ZB = Agency.ZA  , _alpha2["ZA"]

    # South Korea
    KR = Agency.KR  , _alpha2["KR"]
    KS = Agency.KR  , _alpha2["KR"]

    # Belgium, Luxembourg
    BE = Agency.BE  , _alpha2["BE"]
    LU = Agency.BE  , _alpha2["LU"]

    # New Zealand, Fiji, Tonga
    FJ = Agency.NZ  , _alpha2["FJ"]
    NZ = Agency.NZ  , _alpha2["NZ"]
    TO = Agency.NZ  , _alpha2["TO"]

    # Switzerland, Liechtenstein
    CH = Agency.CH  , _alpha2["CH"]
    LI = Agency.CH  , _alpha2["LI"]

    # Obsolete
    PR = Agency.IIRA, _alpha2["PR"]  # Puerto Rico, now managed under US
    CS = Agency.IIRA, _SerbiaMontenegro
    YU = Agency.IIRA, _Yugoslavia

    # Other Existing entries
    AD = Agency.IIRA, _alpha2["AD"]
    AE = Agency.IIRA, _alpha2["AE"]
    AG = Agency.IIRA, _alpha2["AG"]
    AI = Agency.IIRA, _alpha2["AI"]
    AL = Agency.IIRA, _alpha2["AL"]
    AM = Agency.IIRA, _alpha2["AM"]
    AO = Agency.IIRA, _alpha2["AO"]
    AR = Agency.AR  , _alpha2["AR"]
    AT = Agency.AT  , _alpha2["AT"]
    AU = Agency.AU  , _alpha2["AU"]
    AW = Agency.IIRA, _alpha2["AW"]
    AZ = Agency.IIRA, _alpha2["AZ"]
    BA = Agency.IIRA, _alpha2["BA"]
    BB = Agency.BB  , _alpha2["BB"]
    BD = Agency.IIRA, _alpha2["BD"]
    BF = Agency.IIRA, _alpha2["BF"]
    BG = Agency.IIRA, _alpha2["BG"]
    BH = Agency.IIRA, _alpha2["BH"]
    BM = Agency.IIRA, _alpha2["BM"]
    BO = Agency.IIRA, _alpha2["BO"]
    BS = Agency.IIRA, _alpha2["BS"]
    BY = Agency.IIRA, _alpha2["BY"]
    BZ = Agency.IIRA, _alpha2["BZ"]
    CD = Agency.IIRA, _alpha2["CD"]
    CI = Agency.IIRA, _alpha2["CI"]
    CL = Agency.CL  , _alpha2["CL"]
    CM = Agency.IIRA, _alpha2["CM"]
    CN = Agency.IIRA, _alpha2["CN"]
    CO = Agency.IIRA, _alpha2["CO"]
    CU = Agency.IIRA, _alpha2["CU"]
    CW = Agency.IIRA, _alpha2["CW"]
    CY = Agency.IIRA, _alpha2["CY"]
    CZ = Agency.CZ  , _alpha2["CZ"]
    DE = Agency.DE  , _alpha2["DE"]
    DM = Agency.IIRA, _alpha2["DM"]
    DO = Agency.DO  , _alpha2["DO"]
    DZ = Agency.IIRA, _alpha2["DZ"]
    EC = Agency.IIRA, _alpha2["EC"]
    EE = Agency.EE  , _alpha2["EE"]
    EG = Agency.IIRA, _alpha2["EG"]
    ES = Agency.ES  , _alpha2["ES"]
    ET = Agency.IIRA, _alpha2["ET"]
    FI = Agency.FI  , _alpha2["FI"]
    GD = Agency.IIRA, _alpha2["GD"]
    GE = Agency.IIRA, _alpha2["GE"]
    GG = Agency.IIRA, _alpha2["GG"]
    GH = Agency.IIRA, _alpha2["GH"]
    GI = Agency.IIRA, _alpha2["GI"]
    GM = Agency.IIRA, _alpha2["GM"]
    GR = Agency.GR  , _alpha2["GR"]
    GT = Agency.IIRA, _alpha2["GT"]
    GY = Agency.IIRA, _alpha2["GY"]
    HK = Agency.HK  , _alpha2["HK"]
    HN = Agency.IIRA, _alpha2["HN"]
    HR = Agency.IIRA, _alpha2["HR"]
    HT = Agency.IIRA, _alpha2["HT"]
    HU = Agency.IIRA, _alpha2["HU"]
    ID = Agency.ID  , _alpha2["ID"]
    IE = Agency.IE  , _alpha2["IE"]
    IL = Agency.IL  , _alpha2["IL"]
    IN = Agency.IN  , _alpha2["IN"]
    IQ = Agency.IIRA, _alpha2["IQ"]
    IR = Agency.IIRA, _alpha2["IR"]
    IS = Agency.IS  , _alpha2["IS"]
    IT = Agency.IT  , _alpha2["IT"]
    JE = Agency.IIRA, _alpha2["JE"]
    JM = Agency.JM  , _alpha2["JM"]
    JO = Agency.IIRA, _alpha2["JO"]
    JP = Agency.JP  , _alpha2["JP"]
    KE = Agency.IIRA, _alpha2["KE"]
    KN = Agency.IIRA, _alpha2["KN"]
    KY = Agency.IIRA, _alpha2["KY"]
    KZ = Agency.IIRA, _alpha2["KZ"]
    LA = Agency.IIRA, _alpha2["LA"]
    LB = Agency.IIRA, _alpha2["LB"]
    LC = Agency.IIRA, _alpha2["LC"]
    LK = Agency.IIRA, _alpha2["LK"]
    LS = Agency.IIRA, _alpha2["LS"]
    LT = Agency.LT  , _alpha2["LT"]
    LV = Agency.LV  , _alpha2["LV"]
    MA = Agency.IIRA, _alpha2["MA"]
    MC = Agency.IIRA, _alpha2["MC"]
    MD = Agency.IIRA, _alpha2["MD"]
    ME = Agency.IIRA, _alpha2["ME"]
    MK = Agency.IIRA, _alpha2["MK"]
    MO = Agency.IIRA, _alpha2["MO"]
    MP = Agency.IIRA, _alpha2["MP"]
    MS = Agency.IIRA, _alpha2["MS"]
    MT = Agency.IIRA, _alpha2["MT"]
    MU = Agency.IIRA, _alpha2["MU"]
    MV = Agency.IIRA, _alpha2["MV"]
    MW = Agency.IIRA, _alpha2["MW"]
    MX = Agency.MX  , _alpha2["MX"]
    MY = Agency.MY  , _alpha2["MY"]
    MZ = Agency.IIRA, _alpha2["MZ"]
    NA = Agency.IIRA, _alpha2["NA"]
    NG = Agency.IIRA, _alpha2["NG"]
    NL = Agency.NL  , _alpha2["NL"]
    NO = Agency.NO  , _alpha2["NO"]
    NP = Agency.IIRA, _alpha2["NP"]
    PA = Agency.PA  , _alpha2["PA"]
    PE = Agency.PE  , _alpha2["PE"]
    PF = Agency.IIRA, _alpha2["PF"]
    PG = Agency.IIRA, _alpha2["PG"]
    PH = Agency.PH  , _alpha2["PH"]
    PK = Agency.IIRA, _alpha2["PK"]
    PL = Agency.PL  , _alpha2["PL"]
    PT = Agency.PT  , _alpha2["PT"]
    PY = Agency.PY  , _alpha2["PY"]
    QA = Agency.IIRA, _alpha2["QA"]
    RO = Agency.RO  , _alpha2["RO"]
    RS = Agency.IIRA, _alpha2["RS"]
    RU = Agency.IIRA, _alpha2["RU"]
    SA = Agency.IIRA, _alpha2["SA"]
    SB = Agency.IIRA, _alpha2["SB"]
    SC = Agency.IIRA, _alpha2["SC"]
    SE = Agency.SE  , _alpha2["SE"]
    SG = Agency.SG  , _alpha2["SG"]
    SI = Agency.IIRA, _alpha2["SI"]
    SK = Agency.SK  , _alpha2["SK"]
    SL = Agency.IIRA, _alpha2["SL"]
    SM = Agency.IIRA, _alpha2["SM"]
    SN = Agency.IIRA, _alpha2["SN"]
    SV = Agency.IIRA, _alpha2["SV"]
    SX = Agency.IIRA, _alpha2["SX"]
    SZ = Agency.IIRA, _alpha2["SZ"]
    TH = Agency.TH  , _alpha2["TH"]
    TN = Agency.IIRA, _alpha2["TN"]
    TR = Agency.TR  , _alpha2["TR"]
    TT = Agency.TT  , _alpha2["TT"]
    TW = Agency.TW  , _alpha2["TW"]
    TZ = Agency.IIRA, _alpha2["TZ"]
    UA = Agency.UA  , _alpha2["UA"]
    UG = Agency.IIRA, _alpha2["UG"]
    UY = Agency.UY  , _alpha2["UY"]
    UZ = Agency.IIRA, _alpha2["UZ"]
    VC = Agency.IIRA, _alpha2["VC"]
    VE = Agency.IIRA, _alpha2["VE"]
    VG = Agency.IIRA, _alpha2["VG"]
    VN = Agency.IIRA, _alpha2["VN"]
    VU = Agency.IIRA, _alpha2["VU"]
    XK = Agency.IIRA, _alpha2["XK"]
    ZM = Agency.IIRA, _alpha2["ZM"]
    ZW = Agency.IIRA, _alpha2["ZW"]
# fmt: on


@dataclass(frozen=True)
class ISRC:
    """Objectified ISRC structure defined in ISO 3901:2019

    Attributes
    ----------
    owner : str
        5-character registrant code of issuer of ISRC, with first 2 letters
        strictly alphabetic and remaining alphanumeric
    year : int
        last 2 digit of reference year (usually means recording year)
    designation : int
        5-digit identifier for recording, unique within above reference year.
    raw : str or None
        If ISRC is parsed via `parse` method, this attribute preserves the
        original string.
    prefix : str
        First 2 letters of ISRC string. See `country` property below.
    country : iso3166.Country or None
        Read-only property corresponding to country represented by first
        2 letter of ISRC. This is most likely the same as ISO 3166 2-letter
        country code, but there are exceptions. The property could be None
        if ISRC object is manually created with illegal prefix
        (not via ``.parse()`` method).
    agency : str or None
        Read-only property corresponding to national (or international)
        ISRC allocation agency. Like the `country` property above, this property
        can be None if ISRC object contains illegal prefix.
    """

    owner: str
    year: int
    designation: int
    raw: Optional[str] = field(default=None, init=False, repr=False, compare=False)

    def __str__(self) -> str:
        return self.stringify(False)

    @property
    def prefix(self) -> str:
        return self.owner[:2]

    @property
    def country(self) -> Optional[iso3166.Country]:
        try:
            alloc = Allocation[self.prefix]
        except KeyError:
            return None
        return alloc.country

    @property
    def agency(self) -> Optional[str]:
        try:
            alloc = Allocation[self.prefix]
        except KeyError:
            return None
        return alloc.agency.value

    def stringify(self, separator: bool = True) -> str:
        """Print ISRC as string

        Parameters
        ----------
        separator : bool, optional
            Whether hyphen should be inserted between segments. Defaults to True.
            If hyphenation is not intended, it is much simpler to call `str()`
            on the object.

        Returns
        -------
        str
            Resulting ISRC string
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
        if not TYPE_CHECKING:
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
        # fmt: off
        for (segment, length, method) in [
            (country, 2, "isalpha"),
            (owner  , 3, "isalnum"),
            (year   , 2, "isdigit"),
            (desig  , 5, "isdigit"),
        ]:
        # fmt: on
            if len(segment) != length:
                raise ValueError(
                    f'Wrong length for segment "{segment}", expected {length} characters'
                )
            if not segment.isascii() or not getattr(segment, method)():
                raise ValueError(f'Unexpected character found for segment "{segment}"')

        try:
            _ = Allocation[country]
        except KeyError:
            raise ValueError(f'First segment "{country}" is not a known ISRC prefix')

        return (country + owner, int(year), int(desig))

    @classmethod
    def parse(cls: Type[ISRC], _raw: str) -> ISRC:
        """Parses ISRC string into structure

        It checks for ``CCOOOYYNNNNN`` or ``CC-OOO-YY-NNNNN`` pattern
        as mandated by ISRC Handbook, optionally prefixed with "ISRC ".
        Any trailing text is ignored.

        Since ``0.3.0``, it also determines if country code belongs to
        newest published prefixes by IFPI. If this check is undesirable,
        construct ISRC object directly instead of using this method.

        Note
        ----
        This package will *never* check if ISRC string is used in
        some sort of document as illustration purpose (and
        therefore known invalid codes). Collecting those codes is
        impractical.

        Parameters
        ----------
        _raw : str
            The ISRC string to be validated and parsed

        Raises
        ------
        TypeError
            If supplied argument is not a string
        ValueError
            If ISRC segments do not conform to standard

        Returns
        -------
        ISRC
            The structured object representing ISRC data
        """
        owner, year, desig = cls._parse(_raw)
        result = cls(owner, year, desig)
        object.__setattr__(result, "raw", _raw)
        return result

    @classmethod
    def validate(cls, _raw: str) -> bool:
        """Validates if supplied ISRC string is parseable.

        It is almost the same as ``parse()`` method, but instead of returning
        the ``ISRC`` object, ``validate()`` only determines if it is parseable.

        See Also
        --------
        - ``parse()`` method for more detail

        Parameters
        ----------
        _raw : str
            The string to be validated

        Returns
        -------
        bool
            Whether string is plausible ISRC code
        """
        try:
            _ = cls._parse(_raw)
        except:
            return False
        else:
            return True
