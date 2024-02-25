"""wine-nvml builder and copy to Wine output directory"""
import subprocess
from ethanol.utils.logger import debug, info, warn, error
from pathlib import Path

BASE_PATH = Path("./src/wine-nvml")


def update_source():
    """Update wine-nvml source"""
    if BASE_PATH.exists():
        info("Updating wine-nvml repo...")
        retcode = subprocess.call(["git", "pull", "--rebase"], cwd=BASE_PATH)
        if retcode != 0:
            warn("Updating repo failed, resetting...")
            subprocess.call(["git", "reset", "--hard"], cwd=BASE_PATH)
            info("Updating wine-nvml repo again...")
            subprocess.call(["git", "pull"], cwd=BASE_PATH)
    else:
        info("Cloning wine-nvml repo...")
        subprocess.call(
            [
                "git",
                "clone",
                "https://github.com/Saancreed/wine-nvml",
                str(BASE_PATH),
            ]
        )
    info("Updated sources.")


def build():
    """Build wine-nvml"""
    info("Building wine-nvml...")
    subprocess.call(["bash", "./build.sh"], cwd=BASE_PATH)
    info("Built wine-nvml.")
    return True
