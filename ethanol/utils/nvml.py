"""wine-nvml builder and copy to Wine output directory"""
import subprocess
from ethanol.utils.logger import logger as base_logger
from pathlib import Path

BASE_PATH = Path("./src/wine-nvml")
logger = base_logger.getChild("nvml")


def update_source():
    """Update wine-nvml source"""
    if BASE_PATH.exists():
        logger.info("Updating wine-nvml repo...")
        retcode = subprocess.call(["git", "pull", "--rebase"], cwd=BASE_PATH)
        if retcode != 0:
            logger.warn("Updating repo failed, resetting...")
            subprocess.call(["git", "reset", "--hard"], cwd=BASE_PATH)
            logger.info("Updating wine-nvml repo again...")
            subprocess.call(["git", "pull"], cwd=BASE_PATH)
    else:
        logger.info("Cloning wine-nvml repo...")
        subprocess.call(
            [
                "git",
                "clone",
                "https://github.com/Saancreed/wine-nvml",
                str(BASE_PATH),
            ]
        )
    logger.info("Updated sources.")


def build():
    """Build wine-nvml"""
    logger.info("Resetting repo state (to fix building issue)...")
    subprocess.call(["git", "reset", "--hard"], cwd=BASE_PATH)
    logger.info("Building wine-nvml...")
    retcode = subprocess.call(["bash", "./build.sh"], cwd=BASE_PATH)
    if retcode == 0:
        logger.info("Built wine-nvml.")
        return True
    else:
        logger.error("Failed to build wine-nvml.")
        return False
