import random
from enum import Enum
import colorsys
from PIL import Image
from copy import copy

class RebrickableColor:
    def __init__(self, id, name, rebrickable_hex, bartneck_hex, is_transparent):
       self.id = id
       self.name = name
       self.rebrickable_hex = self._pad_hex(rebrickable_hex)
       self.bartneck_hex = self._pad_hex(bartneck_hex)
       self.is_transparent = is_transparent

    @property
    def rebrickable_blender(self):
        return self._hex_to_rgb(self.rebrickable_hex)

    @property
    def bartneck_blender(self):
        if self.bartneck_hex is None:
            return None
        print(f"Converting {self.bartneck_hex} to RGB")
        return self._hex_to_rgb(self.bartneck_hex)

    @property
    def best_hex(self):
        if self.is_transparent:
            # Transparent color render more accurately when we
            # brighten them but apply gamma correction again even
            # through they are already gamma corrected sRGB
            rgb = self._parse_hex_string(self.rebrickable_hex)
            r = self._linear_to_srgb(rgb[0])
            g = self._linear_to_srgb(rgb[1])
            b = self._linear_to_srgb(rgb[2])
            return self._rgb_to_hex((r, g, b))

        return self.rebrickable_hex or self.bartneck_hex

    # Generally the Bartneck colors seem to be more accurate
    # However they are only available in for the main Lego color
    @property
    def blender(self):
        return self.bartneck_blender or self.rebrickable_blender

    def _pad_hex(self, hex):
        if hex is None:
            return None

        hex = hex.replace("#", "")
        # left pad string with 0 if shorter 6 characters
        hex = hex.zfill(6)
        return f"#{hex}"

    def _hex_to_rgb(self, hex_str):
        # Ensure the hex string starts with #
        if not hex_str.startswith('#'):
            hex_str = '#' + hex_str

        # Convert the hex values to integer, and then to floats in range 0-1
        r = self._srgb_to_linearrgb(int(hex_str[1:3], 16) / 255.0)
        g = self._srgb_to_linearrgb(int(hex_str[3:5], 16) / 255.0)
        b = self._srgb_to_linearrgb(int(hex_str[5:7], 16) / 255.0)

        return (r, g, b, 1)

    # #RRGGBB -> (r, g, b) range 0-1
    def _parse_hex_string(self, hex_str):
        # Ensure the hex string starts with #
        if not hex_str.startswith('#'):
            hex_str = '#' + hex_str

        # Convert the hex values to integer, and then to floats in range 0-1
        r = int(hex_str[1:3], 16) / 255.0
        g = int(hex_str[3:5], 16) / 255.0
        b = int(hex_str[5:7], 16) / 255.0

        return (r, g, b)

    def _rgb_to_hex(self, rgb):
        r = int(rgb[0] * 255)
        g = int(rgb[1] * 255)
        b = int(rgb[2] * 255)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _linear_to_srgb(self, c):
        if c < 0:       return 0
        elif c < 0.0031308: return c * 12.92
        else:             return 1.055 * (c**(1/2.4)) - 0.055

    def _srgb_to_linearrgb(self, c):
        # Most hex codes are in sRGB which I believe is gamma corrected: adjusted
        # to compensate for the fact screens emit light in a non-linear fashion.
        # Blender uses linear RGB: the values are proportional to the amount of light.
        # So we need to convert. Except for transparent colors, which seem to be
        # a better representation without any conversion. I don't understand why
        # which makes me worry I am missing something important.
        if self.is_transparent:
            return c
        else:
            if   c < 0:       return 0
            elif c < 0.04045: return c/12.92
            else:             return ((c+0.055)/1.055)**2.4


class RebrickableColors(Enum):
    Black = RebrickableColor(0, 'Black', '#05131D', '#27251F', False)
    Blue = RebrickableColor(1, 'Blue', '#0055BF', '#003DA5', False)
    Green = RebrickableColor(2, 'Green', '#237841', '#00843D', False)
    DarkTurquoise = RebrickableColor(3, 'Dark Turquoise', '#008F9B', '#008675', False)
    Red = RebrickableColor(4, 'Red', '#C91A09', '#EF3340', False)
    DarkPink = RebrickableColor(5, 'Dark Pink', '#C870A0', '#E93CAC', False)
    Brown = RebrickableColor(6, 'Brown', '#583927', '#603D20', False)
    # Brown = RebrickableColor(6, 'Brown', '#583927', '#693F23', False)
    LightGray = RebrickableColor(7, 'Light Gray', '#9BA19D', '#9EA2A2', False)
    DarkGray = RebrickableColor(8, 'Dark Gray', '#6D6E5C', '#51534A', False)
    LightBlue = RebrickableColor(9, 'Light Blue', '#B4D2E3', '#C6DAE7', False)
    BrightGreen = RebrickableColor(10, 'Bright Green', '#4B9F4A', '#009639', False)
    LightTurquoise = RebrickableColor(11, 'Light Turquoise', '#55A5AF', '#00B2A9', False)
    Salmon = RebrickableColor(12, 'Salmon', '#F2705E', '#FF8674', False)
    Pink = RebrickableColor(13, 'Pink', '#FC97AC', '#ECB3CB', False)
    Yellow = RebrickableColor(14, 'Yellow', '#F2CD37', '#FFCD00', False)
    White = RebrickableColor(15, 'White', '#FFFFFF', '#D9D9D6', False)
    LightGreen = RebrickableColor(17, 'Light Green', '#C2DAB8', '#A2E4B8', False)
    LightYellow = RebrickableColor(18, 'Light Yellow', '#FBE696', '#FBD872', False)
    Tan = RebrickableColor(19, 'Tan', '#E4CD9E', '#D3BC8D', False)
    LightViolet = RebrickableColor(20, 'Light Violet', '#C9CAE2', '#CBD3EB', False)
    GlowInDarkOpaque = RebrickableColor(21, 'Glow In Dark Opaque', '#D4D5C9', None, False)
    Purple = RebrickableColor(22, 'Purple', '#81007B', '#9B26B6', False)
    DarkBlueViolet = RebrickableColor(23, 'Dark Blue-Violet', '#2032B0', '#0033A0', False)
    Orange = RebrickableColor(25, 'Orange', '#FE8A18', '#FF8200', False)
    Magenta = RebrickableColor(26, 'Magenta', '#923978', '#AF1685', False)
    Lime = RebrickableColor(27, 'Lime', '#BBE90B', '#B5BD00', False)
    DarkTan = RebrickableColor(28, 'Dark Tan', '#958A73', '#9B945F', False)
    BrightPink = RebrickableColor(29, 'Bright Pink', '#E4ADC8', '#F1A7DC', False)
    MediumLavender = RebrickableColor(30, 'Medium Lavender', '#AC78BA', '#A05EB5', False)
    Lavender = RebrickableColor(31, 'Lavender', '#E1D5ED', '#CAA2DD', False)
    TransBlackIRLens = RebrickableColor(32, 'Trans-Black IR Lens', '#635F52', None, True)
    TransDarkBlue = RebrickableColor(33, 'Trans-Dark Blue', '#0020A0', None, True)
    TransGreen = RebrickableColor(34, 'Trans-Green', '#84B68D', None, True)
    TransBrightGreen = RebrickableColor(35, 'Trans-Bright Green', '#D9E4A7', None, True)
    TransRed = RebrickableColor(36, 'Trans-Red', '#C91A09', None, True)
    TransBrown = RebrickableColor(40, 'Trans-Brown', '#635F52', None, True)
    TransLightBlue = RebrickableColor(41, 'Trans-Light Blue', '#AEEFEC', None, True)
    TransNeonGreen = RebrickableColor(42, 'Trans-Neon Green', '#F8F184', None, True)
    TransVeryLtBlue = RebrickableColor(43, 'Trans-Very Lt Blue', '#C1DFF0', None, True)
    TransDarkPink = RebrickableColor(45, 'Trans-Dark Pink', '#DF6695', None, True)
    TransYellow = RebrickableColor(46, 'Trans-Yellow', '#F5CD2F', None, True)
    TransClear = RebrickableColor(47, 'Trans-Clear', '#FCFCFC', None, True)
    TransPurple = RebrickableColor(52, 'Trans-Purple', '#A5A5CB', None, True)
    TransNeonYellow = RebrickableColor(54, 'Trans-Neon Yellow', '#DAB000', None, True)
    TransNeonOrange = RebrickableColor(57, 'Trans-Neon Orange', '#FF800D', None, True)
    ChromeAntiqueBrass = RebrickableColor(60, 'Chrome Antique Brass', '#645A4C', None, False)
    ChromeBlue = RebrickableColor(61, 'Chrome Blue', '#6C96BF', None, False)
    ChromeGreen = RebrickableColor(62, 'Chrome Green', '#3CB371', None, False)
    ChromePink = RebrickableColor(63, 'Chrome Pink', '#AA4D8E', None, False)
    ChromeBlack = RebrickableColor(64, 'Chrome Black', '#1B2A34', None, False)
    VeryLightOrange = RebrickableColor(68, 'Very Light Orange', '#F3CF9B', '#FECB8B', False)
    LightPurple = RebrickableColor(69, 'Light Purple', '#CD6298', '#981D97', False)
    ReddishBrown = RebrickableColor(70, 'Reddish Brown', '#582A12', '#7A3E3A', False)
    LightBluishGray = RebrickableColor(71, 'Light Bluish Gray', '#A0A5A9', '#A2AAAD', False)
    DarkBluishGray = RebrickableColor(72, 'Dark Bluish Gray', '#6C6E68', '#5B6770', False)
    MediumBlue = RebrickableColor(73, 'Medium Blue', '#5A93DB', '#6CACE4', False)
    MediumGreen = RebrickableColor(74, 'Medium Green', '#73DCA1', '#80E0A7', False)
    SpeckleBlackCopper = RebrickableColor(75, 'Speckle Black-Copper', '#05131D', None, False)
    SpeckleDBGraySilver = RebrickableColor(76, 'Speckle DBGray-Silver', '#6C6E68', None, False)
    LightPink = RebrickableColor(77, 'Light Pink', '#FECCCF', '#FC9BB3', False)
    LightNougat = RebrickableColor(78, 'Light Nougat', '#F6D7B3', '#FCC89B', False)
    MilkyWhite = RebrickableColor(79, 'Milky White', '#FFFFFF', None, False)
    MetallicSilver = RebrickableColor(80, 'Metallic Silver', '#A5A9B4', None, False)
    MetallicGreen = RebrickableColor(81, 'Metallic Green', '#899B5F', None, False)
    MetallicGold = RebrickableColor(82, 'Metallic Gold', '#DBAC34', None, False)
    MediumNougat = RebrickableColor(84, 'Medium Nougat', '#AA7D55', None, False)
    DarkPurple = RebrickableColor(85, 'Dark Purple', '#3F3691', '#330072', False)
    LightBrown = RebrickableColor(86, 'Light Brown', '#7C503A', '#603D20', False)
    RoyalBlue = RebrickableColor(89, 'Royal Blue', '#4C61DB', '#0047BB', False)
    Nougat = RebrickableColor(92, 'Nougat', '#D09168', '#E59E6D', False)
    LightSalmon = RebrickableColor(100, 'Light Salmon', '#FEBABD', '#FFB3AB', False)
    Violet = RebrickableColor(110, 'Violet', '#4354A3', '#1E22AA', False)
    MediumBluishViolet = RebrickableColor(112, 'Medium Bluish Violet', '#6874CA', '#485CC7', False)
    # MediumBluishViolet = RebrickableColor(112, 'Medium Bluish Violet', '#6874CA', '#307FE2', False)
    GlitterTransDarkPink = RebrickableColor(114, 'Glitter Trans-Dark Pink', '#DF6695', None, True)
    MediumLime = RebrickableColor(115, 'Medium Lime', '#C7D23C', '#CEDC00', False)
    GlitterTransClear = RebrickableColor(117, 'Glitter Trans-Clear', '#FFFFFF', None, True)
    Aqua = RebrickableColor(118, 'Aqua', '#B3D7D1', '#9CDBD9', False)
    LightLime = RebrickableColor(120, 'Light Lime', '#D9E4A7', '#C2E189', False)
    LightOrange = RebrickableColor(125, 'Light Orange', '#F9BA61', '#FFB549', False)
    GlitterTransPurple = RebrickableColor(129, 'Glitter Trans-Purple', '#A5A5CB', None, True)
    SpeckleBlackSilver = RebrickableColor(132, 'Speckle Black-Silver', '#05131D', None, False)
    SpeckleBlackGold = RebrickableColor(133, 'Speckle Black-Gold', '#05131D', None, False)
    Copper = RebrickableColor(134, 'Copper', '#AE7A59', None, False)
    PearlLightGray = RebrickableColor(135, 'Pearl Light Gray', '#9CA3A8', None, False)
    PearlSandBlue = RebrickableColor(137, 'Pearl Sand Blue', '#7988A1', None, False)
    PearlLightGold = RebrickableColor(142, 'Pearl Light Gold', '#DCBC81', None, False)
    TransMediumBlue = RebrickableColor(143, 'Trans-Medium Blue', '#CFE2F7', None, True)
    PearlDarkGray = RebrickableColor(148, 'Pearl Dark Gray', '#575857', None, False)
    PearlVeryLightGray = RebrickableColor(150, 'Pearl Very Light Gray', '#ABADAC', None, False)
    VeryLightBluishGray = RebrickableColor(151, 'Very Light Bluish Gray', '#E6E3E0', '#C1C6C8', False)
    YellowishGreen = RebrickableColor(158, 'Yellowish Green', '#DFEEA5', '#D4EB8E', False)
    FlatDarkGold = RebrickableColor(178, 'Flat Dark Gold', '#B48455', None, False)
    FlatSilver = RebrickableColor(179, 'Flat Silver', '#898788', None, False)
    TransOrange = RebrickableColor(182, 'Trans-Orange', '#F08F1C', None, True)
    PearlWhite = RebrickableColor(183, 'Pearl White', '#F2F3F2', None, False)
    BrightLightOrange = RebrickableColor(191, 'Bright Light Orange', '#F8BB3D', '#FFA300', False)
    BrightLightBlue = RebrickableColor(212, 'Bright Light Blue', '#9FC3E9', '#69B3E7', False)
    Rust = RebrickableColor(216, 'Rust', '#B31004', None, False)
    BrightLightYellow = RebrickableColor(226, 'Bright Light Yellow', '#FFF03A', '#FBDB65', False)
    TransPink = RebrickableColor(230, 'Trans-Pink', '#E4ADC8', None, True)
    SkyBlue = RebrickableColor(232, 'Sky Blue', '#7DBFDD', '#05C3DE', False)
    TransLightPurple = RebrickableColor(236, 'Trans-Light Purple', '#96709F', None, True)
    DarkBlue = RebrickableColor(272, 'Dark Blue', '#0A3463', '#003865', False)
    DarkGreen = RebrickableColor(288, 'Dark Green', '#184632', '#2C5234', False)
    GlowInDarkTrans = RebrickableColor(294, 'Glow In Dark Trans', '#BDC6AD', None, True)
    PearlGold = RebrickableColor(297, 'Pearl Gold', '#AA7F2E', None, False)
    DarkBrown = RebrickableColor(308, 'Dark Brown', '#352100', '#31261D', False)
    MaerskBlue = RebrickableColor(313, 'Maersk Blue', '#3592C3', None, False)
    DarkRed = RebrickableColor(320, 'Dark Red', '#720E0F', '#9B2743', False)
    DarkAzure = RebrickableColor(321, 'Dark Azure', '#078BC9', None, False)
    MediumAzure = RebrickableColor(322, 'Medium Azure', '#36AEBF', '#71C5E8', False)
    LightAqua = RebrickableColor(323, 'Light Aqua', '#ADC3C0', '#B9DCD2', False)
    OliveGreen = RebrickableColor(326, 'Olive Green', '#9B9A5A', '#737B4C', False)
    ChromeGold = RebrickableColor(334, 'Chrome Gold', '#BBA53D', None, False)
    SandRed = RebrickableColor(335, 'Sand Red', '#D67572', '#9C6169', False)
    MediumDarkPink = RebrickableColor(351, 'Medium Dark Pink', '#F785B1', '#E277CD', False)
    EarthOrange = RebrickableColor(366, 'Earth Orange', '#FA9C1C', '#D57800', False)
    SandPurple = RebrickableColor(373, 'Sand Purple', '#8.45E+86', '#A192B2', False)
    SandGreen = RebrickableColor(378, 'Sand Green', '#A0BCAC', '#789F90', False)
    SandBlue = RebrickableColor(379, 'Sand Blue', '#6074A1', '#5B7F95', False)
    ChromeSilver = RebrickableColor(383, 'Chrome Silver', '#E0E0E0', None, False)
    FabulandBrown = RebrickableColor(450, 'Fabuland Brown', '#B67B50', '#E56A54', False)
    MediumOrange = RebrickableColor(462, 'Medium Orange', '#FFA70B', '#FFA300', False)
    DarkOrange = RebrickableColor(484, 'Dark Orange', '#A95500', '#B86125', False)
    VeryLightGray = RebrickableColor(503, 'Very Light Gray', '#E6E3DA', '#B2B4B2', False)
    GlowinDarkWhite = RebrickableColor(1000, 'Glow in Dark White', '#D9D9D9', None, False)
    MediumViolet = RebrickableColor(1001, 'Medium Violet', '#93910000', '#685BC7', False)
    GlitterTransNeonGreen = RebrickableColor(1002, 'Glitter Trans-Neon Green', '#C0F500', None, True)
    GlitterTransLightBlue = RebrickableColor(1003, 'Glitter Trans-Light Blue', '#68BCC5', None, True)
    TransFlameYellowishOrange = RebrickableColor(1004, 'Trans-Flame Yellowish Orange', '#FCB76D', None, True)
    TransFireYellow = RebrickableColor(1005, 'Trans-Fire Yellow', '#FBE890', None, True)
    TransLightRoyalBlue = RebrickableColor(1006, 'Trans-Light Royal Blue', '#B4D4F7', None, True)
    ReddishLilac = RebrickableColor(1007, 'Reddish Lilac', '#8E5597', '#B884CB', False)
    VintageBlue = RebrickableColor(1008, 'Vintage Blue', '#039CBD', None, False)
    VintageGreen = RebrickableColor(1009, 'Vintage Green', '#1E601E', None, False)
    VintageRed = RebrickableColor(1010, 'Vintage Red', '#CA1F08', None, False)
    VintageYellow = RebrickableColor(1011, 'Vintage Yellow', '#F3C305', None, False)
    FabulandOrange = RebrickableColor(1012, 'Fabuland Orange', '#EF9121', '#DB8A06', False)
    ModulexWhite = RebrickableColor(1013, 'Modulex White', '#F4F4F4', None, False)
    ModulexLightBluishGray = RebrickableColor(1014, 'Modulex Light Bluish Gray', '#AfB5C7', None, False)
    ModulexLightGray = RebrickableColor(1015, 'Modulex Light Gray', '#9C9C9C', None, False)
    ModulexCharcoalGray = RebrickableColor(1016, 'Modulex Charcoal Gray', '#595D60', None, False)
    ModulexTileGray = RebrickableColor(1017, 'Modulex Tile Gray', '#6B5A5A', None, False)
    ModulexBlack = RebrickableColor(1018, 'Modulex Black', '#4D4C52', None, False)
    ModulexTileBrown = RebrickableColor(1019, 'Modulex Tile Brown', '#330000', None, False)
    ModulexTerracotta = RebrickableColor(1020, 'Modulex Terracotta', '#5C5030', None, False)
    ModulexBrown = RebrickableColor(1021, 'Modulex Brown', '#907450', None, False)
    ModulexBuff = RebrickableColor(1022, 'Modulex Buff', '#DEC69C', None, False)
    ModulexRed = RebrickableColor(1023, 'Modulex Red', '#B52C20', None, False)
    ModulexPinkRed = RebrickableColor(1024, 'Modulex Pink Red', '#F45C40', None, False)
    ModulexOrange = RebrickableColor(1025, 'Modulex Orange', '#F47B30', None, False)
    ModulexLightOrange = RebrickableColor(1026, 'Modulex Light Orange', '#F7AD63', None, False)
    ModulexLightYellow = RebrickableColor(1027, 'Modulex Light Yellow', '#FFE371', None, False)
    ModulexOchreYellow = RebrickableColor(1028, 'Modulex Ochre Yellow', '#FED557', None, False)
    ModulexLemon = RebrickableColor(1029, 'Modulex Lemon', '#BDC618', None, False)
    ModulexPastelGreen = RebrickableColor(1030, 'Modulex Pastel Green', '#7DB538', None, False)
    ModulexOliveGreen = RebrickableColor(1031, 'Modulex Olive Green', '#7C9051', None, False)
    ModulexAquaGreen = RebrickableColor(1032, 'Modulex Aqua Green', '#27867E', None, False)
    ModulexTealBlue = RebrickableColor(1033, 'Modulex Teal Blue', '#467083', None, False)
    ModulexTileBlue = RebrickableColor(1034, 'Modulex Tile Blue', '#0057A6', None, False)
    ModulexMediumBlue = RebrickableColor(1035, 'Modulex Medium Blue', '#61AFFF', None, False)
    ModulexPastelBlue = RebrickableColor(1036, 'Modulex Pastel Blue', '#68AECE', None, False)
    ModulexViolet = RebrickableColor(1037, 'Modulex Violet', '#BD7D85', None, False)
    ModulexPink = RebrickableColor(1038, 'Modulex Pink', '#F785B1', None, False)
    ModulexClear = RebrickableColor(1039, 'Modulex Clear', '#FFFFFF', None, False)
    ModulexFoilDarkGray = RebrickableColor(1040, 'Modulex Foil Dark Gray', '#595D60', None, False)
    ModulexFoilLightGray = RebrickableColor(1041, 'Modulex Foil Light Gray', '#9C9C9C', None, False)
    ModulexFoilDarkGreen = RebrickableColor(1042, 'Modulex Foil Dark Green', '#006400', None, False)
    ModulexFoilLightGreen = RebrickableColor(1043, 'Modulex Foil Light Green', '#7DB538', None, False)
    ModulexFoilDarkBlue = RebrickableColor(1044, 'Modulex Foil Dark Blue', '#0057A6', None, False)
    ModulexFoilLightBlue = RebrickableColor(1045, 'Modulex Foil Light Blue', '#68AECE', None, False)
    ModulexFoilViolet = RebrickableColor(1046, 'Modulex Foil Violet', '#4B0082', None, False)
    ModulexFoilRed = RebrickableColor(1047, 'Modulex Foil Red', '#8B0000', None, False)
    ModulexFoilYellow = RebrickableColor(1048, 'Modulex Foil Yellow', '#FED557', None, False)
    ModulexFoilOrange = RebrickableColor(1049, 'Modulex Foil Orange', '#F7AD63', None, False)
    Coral = RebrickableColor(1050, 'Coral', '#FF698F', None, False)
    PastelBlue = RebrickableColor(1051, 'Pastel Blue', '#5AC4DA', '#ABCAE9', False)
    GlitterTransOrange = RebrickableColor(1052, 'Glitter Trans-Orange', '#F08F1C', None, True)
    TransBlueOpal = RebrickableColor(1053, 'Trans-Blue Opal', '#68BCC5', None, True)
    TransDarkPinkOpal = RebrickableColor(1054, 'Trans-Dark Pink Opal', '#CE1D9B', None, True)
    TransClearOpal = RebrickableColor(1055, 'Trans-Clear Opal', '#FCFCFC', None, True)
    TransBrownOpal = RebrickableColor(1056, 'Trans-Brown Opal', '#583927', None, True)
    TransLightBrightGreen = RebrickableColor(1057, 'Trans-Light Bright Green', '#C9E788', None, True)
    TransLightGreen = RebrickableColor(1058, 'Trans-Light Green', '#94E5AB', None, True)
    TransPurpleOpal = RebrickableColor(1059, 'Trans-Purple Opal', '#8320B7', None, True)
    TransGreenOpal = RebrickableColor(1060, 'Trans-Green Opal', '#84B68D', None, True)
    TransDarkBlueOpal = RebrickableColor(1061, 'Trans-Dark Blue Opal', '#0020A0', None, True)
    VibrantYellow = RebrickableColor(1062, 'Vibrant Yellow', '#EBD800', None, False)
    PearlCopper = RebrickableColor(1063, 'Pearl Copper', '#B46A00', None, False)
    FabulandRed = RebrickableColor(1064, 'Fabuland Red', '#FF8014', '#FF8200', False)
    ReddishGold = RebrickableColor(1065, 'Reddish Gold', '#AC8247', None, False)
    Curry = RebrickableColor(1066, 'Curry', '#DD982E', '#CC8A00', False)
    DarkNougat = RebrickableColor(1067, 'Dark Nougat', '#AD6140', '#B86125', False)
    BrightReddishOrange = RebrickableColor(1068, 'Bright Reddish Orange', '#EE5434', '#FF671F', False)
    PearlRed = RebrickableColor(1069, 'Pearl Red', '#D60026', None, False)
    PearlBlue = RebrickableColor(1070, 'Pearl Blue', '#0059A3', None, False)
    PearlGreen = RebrickableColor(1071, 'Pearl Green', '#008E3C', None, False)
    PearlBrown = RebrickableColor(1072, 'Pearl Brown', '#57392C', None, False)
    PearlBlack = RebrickableColor(1073, 'Pearl Black', '#0A1327', None, False)
    DuploBlue = RebrickableColor(1074, 'Duplo Blue', '#009ECE', None, False)
    DuploMediumBlue = RebrickableColor(1075, 'Duplo Medium Blue', '#3E95B6', '#4298B5', False)
    DuploLime = RebrickableColor(1076, 'Duplo Lime', '#FFF230', '#ECE81A', False)
    FabulandLime = RebrickableColor(1077, 'Fabuland Lime', '#78FC78', None, False)
    DuploMediumGreen = RebrickableColor(1078, 'Duplo Medium Green', '#468A5F', '#4A7729', False)
    DuploLightGreen = RebrickableColor(1079, 'Duplo Light Green', '#60BA76', None, False)
    LightTan = RebrickableColor(1080, 'Light Tan', '#F3C988', '#D9C89E', False)
    RustOrange = RebrickableColor(1081, 'Rust Orange', '#872B17', '#963821', False)
    ClikitsPink = RebrickableColor(1082, 'Clikits Pink', '#FE78B0', None, False)
    TwotoneCopper = RebrickableColor(1083, 'Two-tone Copper', '#945148', None, False)
    TwotoneGold = RebrickableColor(1084, 'Two-tone Gold', '#AB673A', None, False)
    TwotoneSilver = RebrickableColor(1085, 'Two-tone Silver', '#737271', None, False)
    PearlLime = RebrickableColor(1086, 'Pearl Lime', '#6A7944', None, False)
    DuploPink = RebrickableColor(1087, 'Duplo Pink', '#FF879C', None, False)
    MediumBrown = RebrickableColor(1088, 'Medium Brown', '#755945', None, False)
    WarmTan = RebrickableColor(1089, 'Warm Tan', '#CCA373', None, False)
    DuploTurquoise = RebrickableColor(1090, 'Duplo Turquoise', '#3FB69E', None, False)
    WarmYellowishOrange = RebrickableColor(1091, 'Warm Yellowish Orange', '#FFCB78', None, False)
    MetallicCopper = RebrickableColor(1092, 'Metallic Copper', '#764D3B', None, False)
    LightLilac = RebrickableColor(1093, 'Light Lilac', '#9195CA', '#9FAEE5', False)
    TransMediumPurple = RebrickableColor(1094, 'Trans-Medium Purple', '#8D73B3', None, True)
    TransBlack = RebrickableColor(1095, 'Trans-Black', '#635F52', None, True)
    GlitterTransGreeen = RebrickableColor(1098, 'Glitter Trans-Green', '84B68D', None, True)
    GlitterTransPink = RebrickableColor(1099, 'Glitter Trans-Pink', 'E4ADC8', None, True)
    PearlTitanium = RebrickableColor(1103, 'Pearl Titanium', '#3E3C39', None, False)
    ReddishOrange = RebrickableColor(1136, 'Reddish Orange', '#CA4C0B', None, False)
    OpalTransYellow = RebrickableColor(1139, 'Opal Trans-Yellow', 'F5CD2F', None, False)

RebrickableColorsById = {color.value.id: color.value for color in RebrickableColors}

def random_color_for_blender():
  return random.choice(list(RebrickableColors)).value.blender

def random_color_for_pil():
  color = random_color_for_blender()
  return (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))

def random_color_from_ids(ids):
    id = random.choice(ids)
    return RebrickableColorsById[id]

# hsv in floats (0-1), rgb in ints (0-255)
def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
