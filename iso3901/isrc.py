from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import date
from typing import TYPE_CHECKING, NamedTuple, Optional, Tuple, Type

import iso3166

__all__ = ("DB_DATE", "ISRC", "Agency", "Allocation")

#
# All allocation data taken from
# https://isrc.ifpi.org/images/downloads/Valid_Characters_in_the_ISRC_Prefix.pdf
# Old link: https://isrc.ifpi.org/downloads/Valid_Characters.pdf
#

DB_DATE = date(2025, 11, 4)


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
    BW = "COSBOTS"
    CA = "Re:Sound"
    CH = "IFPI Switzerland"
    CL = "IFPI Chile"
    CR = "FONOTICA"
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
    HK = "IFPI (Hong Kong Group) Ltd"
    ID = "ASIRI"
    IE = "PPI"
    IL = "IFPI Israel"
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
    TC = "TuneCore"
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
        def value(self) -> str: ...


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
    prefix_retired: bool


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
    CP = Agency.IIRA, _Worldwide, False
    DG = Agency.IIRA, _Worldwide, False  # also to Turks and Caicos Islands
    QN = Agency.IIRA, _Worldwide, False  # 2024-06
    VV = Agency.IIRA, _Worldwide, False  # 2025-11
    ZZ = Agency.IIRA, _Worldwide, False
    TC = Agency.TC  , _Worldwide, False

    # Brazil
    BC = Agency.BR  , _alpha2["BR"], False
    BK = Agency.BR  , _alpha2["BR"], False
    BP = Agency.BR  , _alpha2["BR"], False
    BR = Agency.BR  , _alpha2["BR"], False
    BX = Agency.BR  , _alpha2["BR"], False

    # Denmark
    DK = Agency.DK  , _alpha2["DK"], False
    FO = Agency.DK  , _alpha2["DK"], False
    GL = Agency.DK  , _alpha2["DK"], False

    # UK
    GB = Agency.GB  , _alpha2["GB"], False
    GX = Agency.GB  , _alpha2["GB"], False
    UK = Agency.GB  , _alpha2["GB"], False

    # US
    QM = Agency.US  , _alpha2["US"], False
    QT = Agency.US  , _alpha2["US"], False  # 2024-06
    QZ = Agency.US  , _alpha2["US"], False
    US = Agency.US  , _alpha2["US"], False

    # Canada
    CA = Agency.CA  , _alpha2["CA"], False
    CB = Agency.CA  , _alpha2["CA"], False

    # France
    FR = Agency.FR  , _alpha2["FR"], False
    FX = Agency.FR  , _alpha2["FR"], False

    # South Africa
    ZA = Agency.ZA  , _alpha2["ZA"], False
    ZB = Agency.ZA  , _alpha2["ZA"], False

    # South Korea
    KR = Agency.KR  , _alpha2["KR"], False
    KS = Agency.KR  , _alpha2["KR"], False

    # Belgium, Luxembourg
    BE = Agency.BE  , _alpha2["BE"], False
    LU = Agency.BE  , _alpha2["LU"], False

    # New Zealand, Fiji, Tonga
    FJ = Agency.NZ  , _alpha2["FJ"], False
    NZ = Agency.NZ  , _alpha2["NZ"], False
    TO = Agency.NZ  , _alpha2["TO"], False

    # Switzerland, Liechtenstein
    CH = Agency.CH  , _alpha2["CH"], False
    LI = Agency.CH  , _alpha2["LI"], False

    # Obsolete
    PR = Agency.IIRA, _alpha2["PR"], True  # Puerto Rico, now managed under US
    CS = Agency.IIRA, _SerbiaMontenegro, True
    IM = Agency.IIRA, _alpha2["IM"], True  # Isle of Mann  # 2024-12
    YU = Agency.IIRA, _Yugoslavia, True

    # Other Existing entries
    AD = Agency.IIRA, _alpha2["AD"], False
    AE = Agency.IIRA, _alpha2["AE"], False
    AF = Agency.IIRA, _alpha2["AF"], False  # 2024-12
    AG = Agency.IIRA, _alpha2["AG"], False
    AI = Agency.IIRA, _alpha2["AI"], False
    AL = Agency.IIRA, _alpha2["AL"], False
    AM = Agency.IIRA, _alpha2["AM"], False
    AO = Agency.IIRA, _alpha2["AO"], False
    AR = Agency.AR  , _alpha2["AR"], False
    AT = Agency.AT  , _alpha2["AT"], False
    AU = Agency.AU  , _alpha2["AU"], False
    AW = Agency.IIRA, _alpha2["AW"], False
    AZ = Agency.IIRA, _alpha2["AZ"], False
    BA = Agency.IIRA, _alpha2["BA"], False
    BB = Agency.BB  , _alpha2["BB"], False
    BD = Agency.IIRA, _alpha2["BD"], False
    BF = Agency.IIRA, _alpha2["BF"], False
    BG = Agency.IIRA, _alpha2["BG"], False
    BH = Agency.IIRA, _alpha2["BH"], False
    BI = Agency.IIRA, _alpha2["BI"], False  # 2024-12
    BJ = Agency.IIRA, _alpha2["BJ"], False  # 2024-12
    BM = Agency.IIRA, _alpha2["BM"], False
    BN = Agency.IIRA, _alpha2["BN"], False  # 2024-12
    BO = Agency.IIRA, _alpha2["BO"], False
    BS = Agency.IIRA, _alpha2["BS"], False
    BT = Agency.IIRA, _alpha2["BT"], False  # 2025-11
    BW = Agency.BW  , _alpha2["BW"], False  # 2024-12
    BY = Agency.IIRA, _alpha2["BY"], False
    BZ = Agency.IIRA, _alpha2["BZ"], False
    CD = Agency.IIRA, _alpha2["CD"], False
    CF = Agency.IIRA, _alpha2["CF"], False  # 2024-12
    CG = Agency.IIRA, _alpha2["CG"], False  # 2024-12
    CI = Agency.IIRA, _alpha2["CI"], False
    CL = Agency.CL  , _alpha2["CL"], False
    CM = Agency.IIRA, _alpha2["CM"], False
    CN = Agency.IIRA, _alpha2["CN"], False
    CO = Agency.IIRA, _alpha2["CO"], False
    CR = Agency.CR,   _alpha2["CR"], False  # 2025-11
    CU = Agency.IIRA, _alpha2["CU"], False
    CV = Agency.IIRA, _alpha2["CV"], False  # 2024-12
    CW = Agency.IIRA, _alpha2["CW"], False
    CY = Agency.IIRA, _alpha2["CY"], False
    CZ = Agency.CZ  , _alpha2["CZ"], False
    DE = Agency.DE  , _alpha2["DE"], False
    DM = Agency.IIRA, _alpha2["DM"], False
    DO = Agency.DO  , _alpha2["DO"], False
    DZ = Agency.IIRA, _alpha2["DZ"], False
    EC = Agency.IIRA, _alpha2["EC"], False
    EE = Agency.EE  , _alpha2["EE"], False
    EG = Agency.IIRA, _alpha2["EG"], False
    ES = Agency.ES  , _alpha2["ES"], False
    ET = Agency.IIRA, _alpha2["ET"], False
    FI = Agency.FI  , _alpha2["FI"], False
    GA = Agency.IIRA, _alpha2["GA"], False  # 2024-12
    GD = Agency.IIRA, _alpha2["GD"], False
    GE = Agency.IIRA, _alpha2["GE"], False
    GG = Agency.IIRA, _alpha2["GG"], False
    GH = Agency.IIRA, _alpha2["GH"], False
    GI = Agency.IIRA, _alpha2["GI"], False
    GM = Agency.IIRA, _alpha2["GM"], False
    GN = Agency.IIRA, _alpha2["GN"], False  # 2024-12
    GQ = Agency.IIRA, _alpha2["GQ"], False  # 2024-12
    GR = Agency.GR  , _alpha2["GR"], False
    GT = Agency.IIRA, _alpha2["GT"], False
    GW = Agency.IIRA, _alpha2["GW"], False  # 2024-12
    GY = Agency.IIRA, _alpha2["GY"], False
    HK = Agency.HK  , _alpha2["HK"], False
    HN = Agency.IIRA, _alpha2["HN"], False
    HR = Agency.IIRA, _alpha2["HR"], False
    HT = Agency.IIRA, _alpha2["HT"], False
    HU = Agency.IIRA, _alpha2["HU"], False
    ID = Agency.ID  , _alpha2["ID"], False
    IE = Agency.IE  , _alpha2["IE"], False
    IL = Agency.IL  , _alpha2["IL"], False
    IN = Agency.IN  , _alpha2["IN"], False
    IQ = Agency.IIRA, _alpha2["IQ"], False
    IR = Agency.IIRA, _alpha2["IR"], False
    IS = Agency.IS  , _alpha2["IS"], False
    IT = Agency.IT  , _alpha2["IT"], False
    JE = Agency.IIRA, _alpha2["JE"], False
    JM = Agency.JM  , _alpha2["JM"], False
    JO = Agency.IIRA, _alpha2["JO"], False
    JP = Agency.JP  , _alpha2["JP"], False
    KE = Agency.IIRA, _alpha2["KE"], False
    KG = Agency.IIRA, _alpha2["KG"], False  # 2024-12
    KH = Agency.IIRA, _alpha2["KH"], False  # 2024-12
    KM = Agency.IIRA, _alpha2["KM"], False  # 2024-12
    KN = Agency.IIRA, _alpha2["KN"], False
    KW = Agency.IIRA, _alpha2["KW"], False  # 2024-12
    KY = Agency.IIRA, _alpha2["KY"], False
    KZ = Agency.IIRA, _alpha2["KZ"], False
    LA = Agency.IIRA, _alpha2["LA"], False
    LB = Agency.IIRA, _alpha2["LB"], False
    LC = Agency.IIRA, _alpha2["LC"], False
    LK = Agency.IIRA, _alpha2["LK"], False
    LR = Agency.IIRA, _alpha2["LR"], False  # 2024-12
    LS = Agency.IIRA, _alpha2["LS"], False
    LT = Agency.LT  , _alpha2["LT"], False
    LV = Agency.LV  , _alpha2["LV"], False
    MA = Agency.IIRA, _alpha2["MA"], False
    MC = Agency.IIRA, _alpha2["MC"], False
    MD = Agency.IIRA, _alpha2["MD"], False
    ME = Agency.IIRA, _alpha2["ME"], False
    MF = Agency.IIRA, _alpha2["MF"], False  # 2024-12
    MG = Agency.IIRA, _alpha2["MG"], False  # 2024-12
    MK = Agency.IIRA, _alpha2["MK"], False
    ML = Agency.IIRA, _alpha2["ML"], False  # 2024-12
    MM = Agency.IIRA, _alpha2["MM"], False  # 2024-12
    MN = Agency.IIRA, _alpha2["MN"], False  # 2024-12
    MO = Agency.IIRA, _alpha2["MO"], False
    MP = Agency.IIRA, _alpha2["MP"], False
    MR = Agency.IIRA, _alpha2["MR"], False  # 2024-12
    MS = Agency.IIRA, _alpha2["MS"], False
    MT = Agency.IIRA, _alpha2["MT"], False
    MU = Agency.IIRA, _alpha2["MU"], False
    MV = Agency.IIRA, _alpha2["MV"], False
    MW = Agency.IIRA, _alpha2["MW"], False
    MX = Agency.MX  , _alpha2["MX"], False
    MY = Agency.MY  , _alpha2["MY"], False
    MZ = Agency.IIRA, _alpha2["MZ"], False
    NA = Agency.IIRA, _alpha2["NA"], False
    NE = Agency.IIRA, _alpha2["NE"], False  # 2024-12
    NG = Agency.IIRA, _alpha2["NG"], False
    NI = Agency.IIRA, _alpha2["NI"], False  # 2024-12
    NL = Agency.NL  , _alpha2["NL"], False
    NO = Agency.NO  , _alpha2["NO"], False
    NP = Agency.IIRA, _alpha2["NP"], False
    OM = Agency.IIRA, _alpha2["OM"], False  # 2024-12
    PA = Agency.PA  , _alpha2["PA"], False
    PE = Agency.PE  , _alpha2["PE"], False
    PF = Agency.IIRA, _alpha2["PF"], False
    PG = Agency.IIRA, _alpha2["PG"], False
    PH = Agency.PH  , _alpha2["PH"], False
    PK = Agency.IIRA, _alpha2["PK"], False
    PL = Agency.PL  , _alpha2["PL"], False
    PS = Agency.IIRA, _alpha2["PS"], False  # 2024-12
    PT = Agency.PT  , _alpha2["PT"], False
    PY = Agency.PY  , _alpha2["PY"], False
    QA = Agency.IIRA, _alpha2["QA"], False
    RO = Agency.RO  , _alpha2["RO"], False
    RS = Agency.IIRA, _alpha2["RS"], False
    RU = Agency.IIRA, _alpha2["RU"], False
    RW = Agency.IIRA, _alpha2["RW"], False  # 2024-12
    SA = Agency.IIRA, _alpha2["SA"], False
    SB = Agency.IIRA, _alpha2["SB"], False
    SC = Agency.IIRA, _alpha2["SC"], False
    SD = Agency.IIRA, _alpha2["SD"], False  # 2024-12
    SE = Agency.SE  , _alpha2["SE"], False
    SG = Agency.SG  , _alpha2["SG"], False
    SI = Agency.IIRA, _alpha2["SI"], False
    SK = Agency.SK  , _alpha2["SK"], False
    SL = Agency.IIRA, _alpha2["SL"], False
    SM = Agency.IIRA, _alpha2["SM"], False
    SN = Agency.IIRA, _alpha2["SN"], False
    SO = Agency.IIRA, _alpha2["SO"], False  # 2024-12
    SR = Agency.IIRA, _alpha2["SR"], False  # 2024-12
    SS = Agency.IIRA, _alpha2["SS"], False  # 2024-12
    SV = Agency.IIRA, _alpha2["SV"], False
    SX = Agency.IIRA, _alpha2["SX"], False
    SY = Agency.IIRA, _alpha2["SY"], False  # 2024-12
    SZ = Agency.IIRA, _alpha2["SZ"], False
    TD = Agency.IIRA, _alpha2["TD"], False  # 2024-12
    TG = Agency.IIRA, _alpha2["TG"], False  # 2024-12
    TH = Agency.TH  , _alpha2["TH"], False
    TL = Agency.IIRA, _alpha2["TL"], False  # 2024-12
    TN = Agency.IIRA, _alpha2["TN"], False
    TR = Agency.TR  , _alpha2["TR"], False
    TT = Agency.TT  , _alpha2["TT"], False
    TW = Agency.TW  , _alpha2["TW"], False
    TZ = Agency.IIRA, _alpha2["TZ"], False
    UA = Agency.UA  , _alpha2["UA"], False
    UG = Agency.IIRA, _alpha2["UG"], False
    UY = Agency.UY  , _alpha2["UY"], False
    UZ = Agency.IIRA, _alpha2["UZ"], False
    VC = Agency.IIRA, _alpha2["VC"], False
    VE = Agency.IIRA, _alpha2["VE"], False
    VG = Agency.IIRA, _alpha2["VG"], False
    VN = Agency.IIRA, _alpha2["VN"], False
    VU = Agency.IIRA, _alpha2["VU"], False
    XK = Agency.IIRA, _alpha2["XK"], False
    YE = Agency.IIRA, _alpha2["YE"], False  # 2024-12
    ZM = Agency.IIRA, _alpha2["ZM"], False
    ZW = Agency.IIRA, _alpha2["ZW"], False
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
    prefix_retired : bool
        Sometimes ISRC prefix can be retired because countries cease to
        exist, or under management of another country, rendering existing
        prefix useless. This property reports such status. Illegal
        prefixes are reported as True.
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
    def prefix_retired(self) -> bool:
        try:
            alloc = Allocation[self.prefix]
        except KeyError:
            return True
        return alloc.prefix_retired

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
        return sep.join([
            self.owner[:2],
            self.owner[2:],
            "{:02d}".format(self.year),
            "{:05d}".format(self.designation),
        ])

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
