import enum


class PacketType(enum.Enum):
    POSITION_WITHOUT_TIMESTAMP = "Position without timestamp (no APRS messaging), or Ultimeter 2000 WX Station"
    POSITION_WITH_TIMESTAMP = "Position with timestamp (no APRS messaging)"
    POSITION_WITHOUT_TIMESTAMP_APRS = "Position without timestamp (with APRS messaging)"
    POSITION_WITH_TIMESTAMP_APRS = "Position with timestamp (with APRS messaging)"
    PEET_BROS_U_II_WEATHER_STATION = "Peet Bros U-II Weather Station"
    RAW_GPS_DATA = "Raw GPS data or Ultimeter 2000"
    MICROFINDER = "Agrelo DFJr / MicroFinder"
    MIC_E_DATA_OLD = "Old Mic-E Data (but Current data for TM-D700)"
    MIC_E_DATA = "Current Mic-E Data (not used in TM-D700)"
    ITEM = "Item"
    MESSAGE = "Message"
    OBJECT = "Object"
    STATION_CAPABILITIES = "Station Capabilities"
    STATUS = "Status"
    QUERY = "Query"
    TELEMETRY_DATA = "Telemetry data"
    MAIDENHEAD_BEACON = "Maidenhead grid locator beacon (obsolete)"
    WEATHER_REPORT = "Weather Report (without position)"
    USER_DEFINED = "User-Defined APRS packet format"
    THIRD_PARTY = "Third-party traffic"

    UNUSED = "[Unused]"
    DO_NOT_USE = "[Do not use]"
    DO_NOT_USE_TNC = "[Do not use - TNC stream switch character]"
    RESERVER_MAP_FEATURE = "[Reserved - Map Feature]"
    RESERVER_SHELTER_DATA_WITH_TIME = "[Reserved - Shelter data with time]"
    RESERVER_SPACE_WEATHER = "[Reserved - Space weather]"
    INVALID_OR_TEST = "Invalid data or test data"


DATA_TYPE_IDENTIFIER: dict = {
    "!": PacketType.POSITION_WITHOUT_TIMESTAMP,
    "\"": PacketType.UNUSED,
    "#": PacketType.PEET_BROS_U_II_WEATHER_STATION,
    "$": PacketType.RAW_GPS_DATA,
    "%": PacketType.MICROFINDER,
    "&": PacketType.RESERVER_MAP_FEATURE,
    "'": PacketType.MIC_E_DATA_OLD,
    "(": PacketType.UNUSED,
    ")": PacketType.ITEM,
    "*": PacketType.PEET_BROS_U_II_WEATHER_STATION,
    "+": PacketType.RESERVER_SHELTER_DATA_WITH_TIME,
    ",": PacketType.INVALID_OR_TEST,
    "-": PacketType.UNUSED,
    ".": PacketType.RESERVER_SPACE_WEATHER,
    "/": PacketType.POSITION_WITH_TIMESTAMP,
    "0": PacketType.DO_NOT_USE,
    "1": PacketType.DO_NOT_USE,
    "2": PacketType.DO_NOT_USE,
    "3": PacketType.DO_NOT_USE,
    "4": PacketType.DO_NOT_USE,
    "5": PacketType.DO_NOT_USE,
    "6": PacketType.DO_NOT_USE,
    "7": PacketType.DO_NOT_USE,
    "8": PacketType.DO_NOT_USE,
    "9": PacketType.DO_NOT_USE,
    ":": PacketType.MESSAGE,
    ";": PacketType.OBJECT,
    "<": PacketType.STATION_CAPABILITIES,
    "=": PacketType.POSITION_WITHOUT_TIMESTAMP_APRS,
    ">": PacketType.STATUS,
    "?": PacketType.QUERY,
    "@": PacketType.POSITION_WITH_TIMESTAMP_APRS,
    "A": PacketType.DO_NOT_USE,
    "B": PacketType.DO_NOT_USE,
    "C": PacketType.DO_NOT_USE,
    "D": PacketType.DO_NOT_USE,
    "E": PacketType.DO_NOT_USE,
    "F": PacketType.DO_NOT_USE,
    "G": PacketType.DO_NOT_USE,
    "H": PacketType.DO_NOT_USE,
    "I": PacketType.DO_NOT_USE,
    "J": PacketType.DO_NOT_USE,
    "K": PacketType.DO_NOT_USE,
    "L": PacketType.DO_NOT_USE,
    "M": PacketType.DO_NOT_USE,
    "N": PacketType.DO_NOT_USE,
    "O": PacketType.DO_NOT_USE,
    "P": PacketType.DO_NOT_USE,
    "Q": PacketType.DO_NOT_USE,
    "R": PacketType.DO_NOT_USE,
    "S": PacketType.DO_NOT_USE,
    "T": PacketType.TELEMETRY_DATA,
    "U": PacketType.DO_NOT_USE,
    "V": PacketType.DO_NOT_USE,
    "W": PacketType.DO_NOT_USE,
    "X": PacketType.DO_NOT_USE,
    "Y": PacketType.DO_NOT_USE,
    "Z": PacketType.DO_NOT_USE,
    "[": PacketType.MAIDENHEAD_BEACON,
    "\\": PacketType.UNUSED,
    "]": PacketType.UNUSED,
    "^": PacketType.UNUSED,
    "_": PacketType.WEATHER_REPORT,
    "`": PacketType.MIC_E_DATA,
    "a": PacketType.DO_NOT_USE,
    "b": PacketType.DO_NOT_USE,
    "c": PacketType.DO_NOT_USE,
    "d": PacketType.DO_NOT_USE,
    "e": PacketType.DO_NOT_USE,
    "f": PacketType.DO_NOT_USE,
    "g": PacketType.DO_NOT_USE,
    "h": PacketType.DO_NOT_USE,
    "i": PacketType.DO_NOT_USE,
    "j": PacketType.DO_NOT_USE,
    "k": PacketType.DO_NOT_USE,
    "l": PacketType.DO_NOT_USE,
    "m": PacketType.DO_NOT_USE,
    "n": PacketType.DO_NOT_USE,
    "o": PacketType.DO_NOT_USE,
    "p": PacketType.DO_NOT_USE,
    "q": PacketType.DO_NOT_USE,
    "r": PacketType.DO_NOT_USE,
    "s": PacketType.DO_NOT_USE,
    "t": PacketType.DO_NOT_USE,
    "u": PacketType.DO_NOT_USE,
    "v": PacketType.DO_NOT_USE,
    "w": PacketType.DO_NOT_USE,
    "x": PacketType.DO_NOT_USE,
    "y": PacketType.DO_NOT_USE,
    "z": PacketType.DO_NOT_USE,
    "{": PacketType.USER_DEFINED,
    "|": PacketType.DO_NOT_USE_TNC,
    "}": PacketType.THIRD_PARTY,
    "~": PacketType.DO_NOT_USE_TNC
}
