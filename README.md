# YolkBot
A collaborative all-in-one bot for the Yolked discord server, written in Python.  It provides numerous utilities and other tools to help keep the server running like a well-oiled machine. If you're interested in helping out, please adhere to the contribution guidelines.

## Contributing
If you want to contribute to YolkBot you can just submit a pull request. Extremely CPU/memory intensive code may be rejected, and your code must be functional in the latest stable release of discord.py.
### Code styling / IDE Settings
- Define variables cleanly, with indicative and descriptive names.
- Use tabs for indentation.
- Lines should not have trailing whitespace.
- Classes and functions should have comments describing their purpose at the beginning of the declaration.
- Use inline comments sparingly.
- When refering to the YolkBot instance, use `bot` instead of `client`.

If you're using a linter or autoformatter, please use `autopep8`. If you're using VSCode, you can find an example config below:
```json
"[python]": {
    "editor.rulers": [
        99
    ],
    "editor.tabSize": 4,
},
"files.insertFinalNewline": true,
"files.trimTrailingWhitespace": true,
"editor.trimAutoWhitespace": true,
"python.formatting.provider": "autopep8",
"python.formatting.autopep8Args": ["--max-line-length", "99"],
```

## Quick Start Guide
This set of instructions should have the project up and running on any machine. You'll need **Python 3.8 or higher**.

[TODO]
