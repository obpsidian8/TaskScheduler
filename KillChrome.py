import subprocess
import os
import platform


def run_shell_cmd(cmd, startDirectory=None):
    fullCmd = f"{cmd}"
    if not startDirectory:
        startDirectory = os.path.dirname(os.path.abspath(__file__))
        print(f"LOG INFO: DIR: {startDirectory}")

    try:
        subprocess.Popen(fullCmd, cwd=startDirectory, shell=True)
    except Exception as exc:
        print(f"LOG ERROR: Shell command was aborted: {exc}")


def get_os_root_dir():
    opr_sys = platform.system()
    if 'windows' in opr_sys.lower():
        shell_cmd = "Taskkill /F /IM Chrome.exe"
    elif 'linux' in opr_sys.lower():
        shell_cmd = "killall chrome"
    else:
        shell_cmd = "Taskkill /F /IM Chrome.exe"
    return shell_cmd


if __name__ == "__main__":
    shell_cmd = get_os_root_dir()
    run_shell_cmd(shell_cmd)
