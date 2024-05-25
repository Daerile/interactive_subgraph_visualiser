import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine-tuning.
build_exe_options = {
    "packages": ["os", "pygame", "networkx", "scipy", "pandas", "numpy", "pygame_gui", "tk", "chardet"],
    "excludes": [],
    "include_files": [
        ("data/allc_model_tulertkek_grafmegjeleníteshez.csv", "allc_model_tulertkek_grafmegjeleníteshez.csv"),
        ("data/test.csv", "test.csv"),
        ("src/view/assets", "view/assets")
    ],
    "build_exe": "interactive_subgraph_visualiser"
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use "Win32GUI" for a Windows GUI app, or None for a console app

setup(
    name="interactive_subgraph_visualiser",
    version="1.0.0",
    description="An interactive subgraph visualiser",
    options={"build_exe": build_exe_options},
    executables=[Executable("src/main.py", base=base)]
)
