#!/usr/bin/python3

import yaml
import sys

VERSION = "0.1"

KEYNAMES_QWERTY_US = {
    "`": "TLDE",
    "~": "TLDE",
    "grave": "TLDE",
    "tilde": "TLDE",
    "asciitilde": "TLDE",
    "1": "AE01",
    "2": "AE02",
    "3": "AE03",
    "4": "AE04",
    "5": "AE05",
    "6": "AE06",
    "7": "AE07",
    "8": "AE08",
    "9": "AE09",
    "0": "AE10",
    "-": "AE11",
    "hyphen": "AE11",
    "minus": "AE11",
    "dash": "AE11",
    "=": "AE12",
    "equals": "AE12",
    "equal": "AE12",
    "q": "AD01",
    "w": "AD02",
    "e": "AD03",
    "r": "AD04",
    "t": "AD05",
    "y": "AD06",
    "u": "AD07",
    "i": "AD08",
    "o": "AD09",
    "p": "AD10",
    "[": "AD11",
    "left_bracket": "AD11",
    "bracketleft": "AD11",
    "]": "AD12",
    "right_bracket": "AD12",
    "bracketright": "AD12",
    "\\": "BKSL",
    "backslash": "BKSL",
    "a": "AC01",
    "s": "AC02",
    "d": "AC03",
    "f": "AC04",
    "g": "AC05",
    "h": "AC06",
    "j": "AC07",
    "k": "AC08",
    "l": "AC09",
    ";": "AC10",
    "semicolon": "AC10",
    "'": "AC11",
    "apostrophe": "AC11",
    "z": "AB01",
    "x": "AB02",
    "c": "AB03",
    "v": "AB04",
    "b": "AB05",
    "n": "AB06",
    "m": "AB07",
    ",": "AB08",
    "comma": "AB08",
    ".": "AB09",
    "dot": "AB09",
    "period": "AB09",
    "/": "AB10",
    "slash": "AB10",
    "solidus": "AB10"
}

CHARNAMES = {
    " ": "space",
    "!": "exclam",
    "\"": "quotedbl",
    "#": "numbersign",
    "$": "dollar",
    "%": "percent",
    "&": "ampersand",
    "'": "apostrophe",
    "(": "parenleft",
    ")": "parenright",
    "*": "asterisk",
    "+": "plus",
    ",": "comma",
    "-": "minus",
    ".": "period",
    "/": "slash",
    ":": "colon",
    ";": "semicolon",
    "<": "less",
    "=": "equal",
    ">": "greater",
    "?": "question",
    "@": "at",
    "[": "bracketleft",
    "\\": "backslash",
    "]": "bracketright",
    "^": "asciicircum",
    "_": "underscore",
    "`": "grave",
    "{": "braceleft",
    "|": "bar",
    "}": "braceright",
    "~": "asciitilde",
}

DEADKEYS = ["dead_grave", "dead_acute", "dead_circumflex", "dead_tilde", "dead_perispomeni", 
    "dead_macron", "dead_breve", "dead_abovedot", "dead_diaeresis", "dead_abovering", 
    "dead_doubleacute", "dead_caron", "dead_cedilla", "dead_ogonek", "dead_iota", 
    "dead_voiced_sound", "dead_semivoiced_sound", "dead_belowdot", "dead_hook", "dead_horn", 
    "dead_stroke", "dead_abovecomma", "dead_psili", "dead_abovereversedcomma", "dead_dasia", 
    "dead_doublegrave", "dead_belowring", "dead_belowmacron", "dead_belowcircumflex", 
    "dead_belowtilde", "dead_belowbreve", "dead_belowdiaeresis", "dead_invertedbreve", 
    "dead_belowcomma", "dead_currency", "dead_lowline", "dead_aboveverticalline", 
    "dead_belowverticalline", "dead_longsolidusoverlay", "dead_a", "dead_A", "dead_e", "dead_E", 
    "dead_i", "dead_I", "dead_o", "dead_O", "dead_u", "dead_U", "dead_small_schwa", 
    "dead_capital_schwa", "dead_greek"]

HEADER = """////////////////////////////////////////////////
//  Keyboard layout generated with TriXKBGen  //
//  https://github.com/trimill/xkbgen/        //
////////////////////////////////////////////////
// vim: set syn=xkb:
"""

def translate_char(c):
    if len(c) == 0:
        return "NoSymbol"
    elif c in CHARNAMES:
        return CHARNAMES[c]
    elif c in CHARNAMES.values() or c in DEADKEYS:
        return c
    elif len(c) == 1 and c in "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890":
        return c
    elif len(c) == 1:
        return "U%04X" % ord(c)
    elif c[0] == "u" or c[0] == "U":
        return c
    else:
        print("Error: unknown character:", c)
        sys.exit(1)

def genmodfmt(mod, lvl):
    return """    key <%s> {
        type[Group1]="ONE_LEVEL",
        symbols[Group1] = [ISO_Level%s_Shift]
    };""" % (mod, lvl)

print("TriXKBGen v. %s" % VERSION)

if len(sys.argv) > 1:
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print("Usage:\n\t%s <input> <output>\n\t%s --help")
        print("For documentation, visit https://github.com/trimill/xkbgen/")
        print("To install keyboard layouts, move them to the following path:")
        print("\t/usr/share/X11/xkb/symbols/")
        print("(you will need root access to do this)")
        sys.exit(0)

if len(sys.argv) < 3:
    print("Error: must specify input and output file")
    sys.exit(1)

filename = sys.argv[1];
with open(filename) as f:
    data = yaml.safe_load(f)

lines = [HEADER]

lines.append("default partial alphanumeric_keys modifier_keys")
lines.append("xkb_symbols \"%s\" {" % data["name"])
lines.append("    name[Group1]=\"%s\";" % data["groupname"])

if data["layout"] == "qwerty":
    if data["layout-locale"] == "us":
        keynames = KEYNAMES_QWERTY_US
    else:
        print("Error: localization not supported for layout qwerty:", data["layout-locale"])
        sys.exit(1)
else:
    print("Error: keyboard layout not supported:", data["layout"])
    sys.exit(1)

if "level3" in data:
    lines.append("    include \"level3(%s)\"" % data["level3"])

if "level5" in data:
    lines.append("    include \"level5(%s)\"" % data["level5"])
    lines.append("    key.type[Group1] = \"EIGHT_LEVEL_ALPHABETIC_LEVEL_FIVE_LOCK\";")

for k,v in data["keys"].items():
    k = str(k)
    if k in keynames:
        key = keynames[k]
    elif k in keynames.values():
        key = k
    else:
        print("Error: unknown key:", k)
        sys.exit(1)
    chars = v.replace("  ", " ").split(" ")
    chars = [translate_char(c) for c in chars]
    line = "    key <%s> {[ %s ]};" % (key, ", ".join(chars))
    lines.append(line)

lines.append("};")

with open(sys.argv[2], "w") as f:
    f.write("\n".join(lines) + "\n")

print("Success! Created mapping for %s keys." % len(data["keys"]))

