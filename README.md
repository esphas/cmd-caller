
# Cmd Caller

A [Sublime Text 3](http://www.sublimetext.com) plugin to execute predefined commands conveniently.

#### Key Bindings
By default, Cmd Caller binds `Ctrl+Shift+X` for quickly executing default command, and `Ctrl+Shift+,` for opening a panel to select a command to execute.

Key Bindings are accessed via the `Preferences` > `Package settings` > `Cmd Caller` menu.

#### Settings
Settings are accessed via the `Preferences` > `Package settings` > `Cmd Caller` menu.

##### default command
`"default": "KEY_TO_APP"`

Default command should be set to the key of disired command.

##### apps

Apps are predefined commands.

```json
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
```

Following variables in `"cmd"` will be expanded.

   variable            | note
-----------------------|--------------------------------------------
`${file}`              | current edited file, full path
`${file_name}`         | basename.extname
`${file_base_name}`    |
`${file_extension}`    |
`${file_path}`         | current working directory, full path
`${folder}`            | current added folder in project, full path
`${project_base_name}` | name of current project

#### Installation

##### Manual Installation
Just clone this repository to your Sublime Text packages directory.

```
git clone git@github.com:esphas/cmd-caller.git
```

#### Compatibility

This plugin is made on Windows, and should work on Linux and OSX, though not yet tested.
