# Ethanol

Wine-tkg quick patcher written in Python

## Installation

```bash
git clone https://github.com/teppyboy/ethanol
cd ethanol
poetry install
poetry run python -m ethanol <variant>
# Where variant is listed in "wine-tkg-profiles" directory 
```

## Usage

Put the changes you want to make in `./patches`, for instance to change a setting in `customization.cfg`:
```
File: config/wine-tkg-git/customization.cfg
---
_community_patches="0002-proton_QPC.mypatch"
```

`.patch` file is also supported, you can do that by putting it in anywhere inside `./patches` and it'll patch the file 
with the same relative name. 

E.g. `wine-tkg-git/wine-tkg-scripts/prepare.sh.patch` will patch `wine-tkg-git/wine-tkg-git/wine-tkg-scripts/prepare.sh`

Also there's `replace.py` where you can define which files to replace the content.

The default preset (nightmare-staging) is tweaked for wine-staging with some patches and branding.

## License

[MIT](./LIECNSE)
