[
    {
        "path": [
            "wine-tkg-git/wine-tkg-patches/hotfixes/earlyhotfixer",
            "wine-tkg-git/wine-tkg-patches/hotfixes/valve/hotfixes",
            "wine-tkg-git/wine-tkg-patches/hotfixes/NosTale/hotfixes",
            "wine-tkg-git/wine-tkg-scripts/build-32.sh"
        ],
        "replace": [
            {"""$_plain_version" = *_8.0""": """$_plain_version" = *bleeding-edge"""},
            {"""$_plain_version" != *_8.0""": """$_plain_version" != *bleeding-edge"""}
        ]
    }
]