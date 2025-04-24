
# MiniCube

[![Install MiniCube](https://img.shields.io/badge/🧊%20Install-MiniCube-blue)](https://zimoshi.github.io/minicube/setup.sh)

MiniCube is a lightweight command-line virtual machine simulation written in Python. It mimics a shell environment with a virtual home directory (`/home/<user>`), built-in commands (`curd`, `ccd`, etc.), and support for shell script modules.

## Features

- Virtual home (`/home/<user>`) mapped to `/tmp`
- Built-in commands: `curd`, `ccd`, etc.
- Command scripts in `commands/` folder (e.g. `commands/install/install.sh`)
- Subcommand support: `install install cubeos`
- Startup file support (`~/.micurc`)
- Developer-friendly debug output

## Install
```bash
curl -LO https://zimoshi.github.io/minicube/setup.sh
chmod +x setup.sh
./setup.sh
```

## Structure

```
minicube/
├── main.py       # Core MiniCube interpreter (aka vm.pyd)
├── commands/
│   └── example/
│       └── example.sh
```

## Example

```bash
/home/zimo > curd
/home/zimo

/home/zimo > ccd projects
/home/zimo/projects >

/home/zimo > cubeos directory
Welcome to CubeOS!
```

## License

MiniCube Personal License (MCPL).

This project is licensed for personal use only.

📌 **Please do not fork or redistribute this repository** without permission from the author: [zimoshi](https://github.com/zimoshi).
