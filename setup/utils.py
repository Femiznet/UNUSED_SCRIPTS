import subprocess
import platform

def verify_installation(commands:list[str], use_path:str):
    # Modified line: injects target directory based on the boolean path flag

    for command in commands:
        cmd = command.split()

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True,
            cwd=use_path,
        )

        if result.returncode == 0:
            print("Output:", result.stdout)
            return True

    return False

def get_os():
    return platform.system()
