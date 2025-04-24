import subprocess
import os
import sys
import shlex

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
                print(f"~/.micurc > {line}")
                os.system(line)

# Install path
minicube_root = os.path.dirname(os.path.abspath(__file__))

while True:
    try:
        cwd_virtual = os.getcwd().replace(real_home, virtual_home, 1)
        cmd_input = input(f"{cwd_virtual.split("/")[-1]} > ").strip()
        if not cmd_input:
            continue

        cmd_parts = shlex.split(cmd_input)
        command, *args = cmd_parts

        # Handle built-in curd
        if command == "curd":
            print(os.getcwd().replace(real_home, virtual_home, 1))
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
                print(f"Command '{command}' not found or no matching script.")
                continue
        else:
            fallback_script = os.path.join(script_dir, f"{command}.sh")
            if not os.path.isfile(os.path.join(minicube_root, fallback_script)):
                print(f"Command '{command}' not found or '{command}.sh' missing.")
                continue
            script_path = fallback_script
            script_args = []

        print("MiniCube Developer mode command debug:", f"[\"{command}\"]", args)

        # Run command from root, then return
        os.chdir(minicube_root)
        result = subprocess.run(["sh", script_path] + script_args, capture_output=True, text=True)
        os.chdir(real_home)

        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

    except KeyboardInterrupt:
        print("\nMiniCube exiting.")
        break
    except Exception as e:
        print(f"Error: {e}")
