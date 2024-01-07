import socket
import logging
import subprocess


def get_logger(name: str) ->  logging.Logger:
    return logging.getLogger(f"[{socket.gethostname()} {name}")


def run_shell_command(cmd: str) -> str:
    try:
        return subprocess.run(cmd, text=True, shell=True, check=True, capture_output=True).stdout
    except:
        try:
            subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))

                