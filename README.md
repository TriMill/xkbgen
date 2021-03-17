# TriXKBGen

This python script allows you to automatically generate XKB keyboard layouts from a YAML file. This greatly speeds up the process of creating keyboards, and makes inputting Unicode characters much easier

## Requirements

PyYAML: `pip install pyyaml`

## Usage

`xkbgen.py <input> <output>`, where `<input>` is the path to the YAML file and `<output>` is the path to the output file.

`xkbgen.py --help` for the builtin help message.

## Input format

The following properties can or must be set in the YAML file:

| Name            | Required | Description                    | Values                                     | Example                   |
| `name`          | yes      | The name of the layout variant | Any string, usually lowercase alphanumeric | `name: "ipa"`             |
| `groupname`     | yes      | The name of the group          | Any string                                 | `groupname: "IPA (US)"`   |
| `layout`        | yes      | The keyboard layout            | `qwerty` (more may be added later)         | `layout: "qwerty"`        |
| `layout-locale` | yes      | The keyboard layout's locale   | `us` (more may be added later)             | `layout-locale: "us"`     |
| `level3`        | no       | The key used to access level 3 | See below                                  | `level3: "ralt_switch"`   |
| `level5`        | no       | The key used to access level 5 | See below                                  | `level5: "rctrl_switch"`  |
| `keys`          | yes      | The keymap (see below)         | An object                                  |                           |

The possible options for `level3` and `level5` can be viewed in `/usr/share/X11/xkb/symbols/level3` and `/usr/share/X11/xkb/symbols/level5`, respectively.

The `keys` property contains all of the key mappings. For each field, the name is the original value of the key (determined by how `layout` and `layout-locale` were set), and the value is a list of keycodes. Here are the keycode formats:

* A space: no character is typed
* A single character: that character is typed
* `Uxxxx`: the Unicode character with the corresponding codepoint is typed
* `dead_xxxx`: a deadkey is typed (used for inserting diacritical marks)

Each keycode is separated by a space. The index of the keycode in the list determines what modifiers will be pressed to create it:

1. no modifiers
2. `SHIFT`
3. `level3`
4. `SHIFT` + `level3`
5. `level5`
6. `SHIFT` + `level5`
7. `level3` + `level5`
8. `SHIFT` + `level3` + `level5`

As an example, the line
```
   h: "h ʜ ɥ ħ ɦ ɧ ʰ H"
```
will cause the `h` key to type:

* `h` when no modifiers are pressed
* `ʜ` when `SHIFT` is pressed
* `ɥ` when `level3` is pressed
* `ħ` when `SHIFT` + `level3`
* `ɦ` when `level5` is pressed
* `ɧ` when `SHIFT` + `level5` is pressed
* `ʰ` when `level3` + `level5` is pressed
* `H` when `SHIFT` + `level3` + `level5` is pressed

## Examples

The `examples` directory contains example YAML files and their generated keyboard layouts, demonstrating all of the functionality described here.

