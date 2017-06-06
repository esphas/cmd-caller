
# Cmd Caller

A [Sublime Text 3](http://www.sublimetext.com) plugin to execute predefined commands conveniently.

[![license](https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square)](https://github.com/esphas/cmd-caller/blob/master/License)
[![Package Control](https://img.shields.io/packagecontrol/dt/cmd-caller.svg?style=flat-square)](https://packagecontrol.io/packages/cmd-caller)

## Usage

Cmd Caller can execute a command instantly by pressing a hotkey(`Default Action`, or open a list of avaliable commands to execute via another hotkey(`App List`).
These commands should be predefined in the settings. Also, there are a few predefined commands in the default settings.

Thus, you are two steps away from the convenience of the plugin
* Define commands: consult [Settings](#settings) below
* Press hotkey: consult [Key Bindings](#key-bindings) below

  Also, `Default Action`, `App List`, `Settings` and `Key Bindings` are also available via Command Palette.

## Key Bindings
By default, Cmd Caller binds `Ctrl+Shift+X` to `Default Action`, and `Ctrl+Shift+,` to `App List`.


Key Bindings are accessed via the `Preferences` > `Package settings` > `Cmd Caller` menu.

## Settings
Settings are accessed via the `Preferences` > `Package settings` > `Cmd Caller` menu.

### default
`"default": "KEY_TO_APP"`

`"KEY_TO_APP"` should be set to the key of app that `Default Action` will call.

### apps

Apps are predefined commands.

```json
{
  "apps": {
    "KEY": {
      "name": "DISPLAY_NAME",
      "cmd": "COMMAND_TO_EXECUTE"
    },
    "KEY2": {
      "name": "DISPLAY_NAME2",
      "cmd": "COMMAND2"
    },
  }
}
```

Following variables in `"cmd"` will be expanded.

   variable            | example                                   | note
-----------------------|-------------------------------------------|----------------------------------
`${file}`              | `/home/esphas/cmd-caller/src/commands.py` | current edited file, full path
`${file_name}`         | `commands.py`                             | current file name: basename.extname
`${file_base_name}`    | `commands`                                | current file basename
`${file_extension}`    | `py`                                      | current file extension name
`${file_path}`         | `/home/esphas/cmd-caller/src/`            | current working directory, full path
`${folder}`            | `/home/esphas/cmd-caller`*                | current added folder in project, full path
`${project_base_name}` | `cc`**                                    | current project name

\* about projects, consult [Projects](http://docs.sublimetext.info/en/latest/file_management/projects.html)

\*\* granted that the project file is `/some/directory/cc.sublime-project`

## Installation

### Package Control
* Start Sublime Text
* [Install Package Control](https://packagecontrol.io/installation#st3)
* Open the Command Palette and choose `Package Control: Install Package`
* Search for [`cmd-caller`](https://packagecontrol.io/packages/cmd-caller) and select to install

### Manual Installation
* Start Sublime Text
* Open package folder via the `Preferences`>`Browse Packages...` menu
* Execute git clone: `git clone https://github.com/esphas/cmd-caller.git`

## Compatibility

This plugin is tested campatible with windows(`Windows 10 1703 Build 15063`) and linux(`Ubuntu 16.04.2 LTS`).

No commands(apps) are predefined for osx, although the plugin should not face compatibility problems with osx.
