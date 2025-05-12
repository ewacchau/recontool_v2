import subprocess, shlex, logging, shutil

def run_cmd(cmd, timeout=600):
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    if not shutil.which(cmd[0]):
        logging.warning("Command %s not found", cmd[0])
        return ""
    try:
        comp = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        comp.check_returncode()
        return comp.stdout
    except subprocess.TimeoutExpired:
        logging.warning("Command %s timed out", cmd)
        return ""
    except subprocess.CalledProcessError as exc:
        logging.error("Command failed: %s", exc)
        return exc.stdout + exc.stderr
