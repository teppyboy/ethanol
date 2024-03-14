#!/usr/bin/env python3

import inicfp
import subprocess
from datetime import datetime
from ethanol.utils.logger import debug, info, warn, error
from ethanol.utils import nvml
from pathlib import Path
from shutil import copy2, move

BASE_PATH = Path("./src/")
BASE_PATH.mkdir(exist_ok=True)
DIST_PATH = Path("./dist/")
wine_tkg_path = BASE_PATH.joinpath("wine-tkg-git")
wine_tkg_out_name: str = None


def patch_config(patch_file: Path, target: Path):
    patch_content = inicfp.loads(patch_file.read_text())
    if target.is_file():
        # Preserve everything in the config
        base_content = inicfp.loads(target.read_text(), comments=True, whitespace=True)
    else:
        base_content = {}
    for k, v in patch_content.items():
        base_content[k] = v
    # Replace to fix ini spacing
    target.write_text(inicfp.dumps(base_content).replace(" = ", "="))


def update_sources():
    # Wine-tkg-git
    if wine_tkg_path.exists():
        info("Updating wine-tkg repo...")
        retcode = subprocess.call(["git", "pull", "--rebase"], cwd=wine_tkg_path)
        if retcode != 0:
            warn("Updating repo failed, resetting...")
            subprocess.call(["git", "reset", "--hard"], cwd=wine_tkg_path)
            info("Updating wine-tkg repo again...")
            if subprocess.call(["git", "pull"], cwd=wine_tkg_path) != 0:
                error("Failed to update wine-tkg repo.")
                return False
    else:
        info("Cloning wine-tkg repo...")
        if (
            subprocess.call(
                [
                    "git",
                    "clone",
                    "https://github.com/Frogging-Family/wine-tkg-git",
                    str(wine_tkg_path),
                ]
            )
            != 0
        ):
            error("Failed to clone wine-tkg repo.")
            return False
    # Wine-nvml
    nvml.update_source()
    info("Updated sources.")
    return True


def patch_tkg(patches: Path = Path("./patches")):
    """Patch Wine-tkg files"""
    config = patches.joinpath("config")
    for file in patches.rglob("*.*"):
        if file.suffix == ".patch":
            info(f"Applying patch '{file}'...")
            if (
                subprocess.call(
                    [
                        "patch",
                        "-Np1",
                        file.with_suffix("").relative_to(patches),
                        file.resolve(),
                    ],
                    cwd=wine_tkg_path,
                )
                != 0
            ):
                error("Failed to apply patch.")
                return False
    for file in config.rglob("*.*"):
        if file.suffix == ".cfg":
            info(f"Applying config patch to '{file}'...")
            patch_config(file, target=wine_tkg_path.joinpath(file.relative_to(config)))
    replace_path = patches.joinpath("replace.py")
    if replace_path.exists():
        replace_list: list[dict] = eval(replace_path.read_text())
        for replace_file in replace_list:
            for replace in replace_file["replace"]:
                for maybe_path in replace_file['path']:
                    if "*" in maybe_path:
                        paths = wine_tkg_path.glob(maybe_path)
                    else:
                        paths = [wine_tkg_path.joinpath(maybe_path)]
                    for file in paths:
                        file_content = file.read_text()
                        for from_text, to in replace.items():
                            info(f"Replacing '{from_text}' with '{to}' in '{file}'...")
                            file_content = file_content.replace(from_text, to)
                        file.write_text(file_content)
    info("Patched wine-tkg successfully.")
    return True


def build_wine():
    """
    Run wine-tkg prepare script
    """
    info("Building wine-tkg-git...")
    info("Executing actual build script...")
    retcode = subprocess.call(
        ["bash", "./non-makepkg-build.sh"], cwd=wine_tkg_path.joinpath("wine-tkg-git")
    )
    if retcode != 0:
        error("Failed to build wine.")
        return False
    info("Wine built successfully, moving output to 'dist' directory...")
    partial_name: str = None
    for line in wine_tkg_path.joinpath("wine-tkg-git/last_build_config.log").read_text().splitlines():
        if "Wine (plain) version:" in line:
            partial_name = line.split(":")[1].strip()
            break
    if not partial_name:
        error("Failed to find wine output name.")
        return False
    for file in wine_tkg_path.joinpath("wine-tkg-git/non-makepkg-builds/").iterdir():
        if not file.is_dir():
            continue
        if partial_name in file.name:
            info(f"Moving '{file}' to 'dist' directory...")
            move(file, DIST_PATH.joinpath(file.name))
            global wine_tkg_out_name
            wine_tkg_out_name = file.name
            break
    return True


def bundle_nvml():
    info("Bundling NVML to wine...")
    wine_path = DIST_PATH.joinpath(wine_tkg_out_name)
    info("Copying NVML to wine output directory...")
    nvml_path = nvml.BASE_PATH
    copy2(nvml_path.joinpath("build-wine64/src/nvml.so"), wine_path.joinpath("lib/wine/x86_64-unix/nvml.so"))
    copy2(nvml_path.joinpath("build-mingw64/src/nvml.dll"), wine_path.joinpath("lib/wine/x86_64-windows/nvml.dll"))
    info("NVML bundled successfully.")
    return True


def main():
    info("Ethanol - Wine-tkg-git quick patcher")
    for job in [(update_sources, True), (patch_tkg, True), (build_wine, True), (nvml.build, False), (bundle_nvml, True)]:
        if not job():
            error("Job failed, aborting.")
            return


if __name__ == "__main__":
    main()
