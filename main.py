import subprocess
import os
import sys
import shlex
from syntaxp import cvert
import time
import random

print(cvert("[syntaxp-bold][syntaxp-light-green]MiniCube 2.5.2 alpha 3[syntaxp-reset]"))

# Setup virtual home
username = os.getenv("USER") or os.getenv("USERNAME") or "user"
real_home = os.path.realpath(f"/tmp/minicube/home/{username}")
virtual_home = f"/home/{username}"
os.makedirs(real_home, exist_ok=True)
os.chdir(real_home)
# ~/.micurc autoload
micurc_path = os.path.join(real_home, ".micurc")
if os.path.isfile(micurc_path):
    with open(micurc_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                # print(f"~/.micurc > {line}")
                os.system(line)

import readline
import atexit

HISTORY_FILE = os.path.join(real_home, ".minicube_history")
os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

# Load history if exists
if os.path.exists(HISTORY_FILE):
    readline.read_history_file(HISTORY_FILE)

# Save history on exit
atexit.register(readline.write_history_file, HISTORY_FILE)

# Install path
minicube_root = os.path.dirname(os.path.abspath(__file__))
print(cvert(f"[syntaxp-light-purple]Last login: {time.asctime()[:-5]} on ttys0{random.randint(10,45)}[syntaxp-reset]"))

while True:
    try:
        cwd_virtual = os.getcwd().replace(real_home, virtual_home, 1)
        cmd_input = input(cvert(f"[syntaxp-cyan]{cwd_virtual.split('/')[-1]} > [syntaxp-blue]", True)).strip()
        if not cmd_input:
            continue

        cmd_parts = shlex.split(cmd_input)
        command, *args = cmd_parts

        # Handle built-in curd
        if command == "curd":
            print(os.getcwd().replace(real_home, virtual_home, 1))
            continue
        
        if command == "list":
            try:
                subprocess.run(["ls"] + args)
            except Exception as e:
                print(cvert(f"[syntaxp-red]ls error:[syntaxp-reset] {e}"))
            continue
        
        if command == "clr":
            os.system("clear")
            continue

        
        # Pass-through to system nano
        if command == "nano":
            if not args:
                print("Usage: nano <filename>")
                continue
            try:
                subprocess.run(["nano"] + args)
            except FileNotFoundError:
                print("Nano is not installed.")
            continue

        # Handle built-in ccd
        if command == "ccd":
            if not args:
                print("ccd requires a path")
                continue
            try:
                os.chdir(args[0])
            except Exception as e:
                print(f"Failed to change directory: {e}")
            continue

        # Command path logic
        script_dir = os.path.join("commands", command)
        script_path = ""
        script_args = []

        if args:
            subcommand_script = os.path.join(script_dir, f"{args[0]}.sh")
            fallback_script = os.path.join(script_dir, f"{command}.sh")
            if os.path.isfile(os.path.join(minicube_root, subcommand_script)):
                script_path = subcommand_script
                script_args = args[1:]
            elif os.path.isfile(os.path.join(minicube_root, fallback_script)):
                script_path = fallback_script
                script_args = args
            else:
                print(cvert(f"[syntaxp-red]Command '{command}' not found or no matching script.[syntaxp-reset]"))
                continue
        else:
            fallback_script = os.path.join(script_dir, f"{command}.sh")
            if not os.path.isfile(os.path.join(minicube_root, fallback_script)):
                print(cvert(f"[syntaxp-red]Command '{command}' not found or '{command}.sh' missing.[syntaxp-reset]"))
                continue
            script_path = fallback_script
            script_args = []

        # print("MiniCube Developer mode command debug:", f"[\"{command}\"]", args)

        # Run command from root, then return
        os.chdir(minicube_root)
        result = subprocess.run(["sh", script_path] + script_args, capture_output=True, text=True)
        os.chdir(real_home)

        print(cvert(f"[syntaxp-green]{result.stdout}[syntaxp-reset]"))
        if result.stderr:
            print(result.stderr, file=sys.stderr)

    except KeyboardInterrupt:
        print(cvert("\n[syntaxp-red]MiniCube exiting.[syntaxp-reset]"))
        break
    except Exception as e:
        print(f"Error: {e}")
