import sys

from cx_Freeze import setup, Executable

PROJECT_NAME = "VKJointProcurementAssistant"
BASE = None

if sys.platform == "win32":
    BASE = "Win32GUI"

MODULES = [
    "__main__",
]

PYQT4_MODULES = [
    "sip",
    "PyQt4.QtCore",
    "PyQt4.uic",
    "PyQt4.QtGui",
    "PyQt4.QtWebkit",
]

build_exe = {
    "includes": ["atexit", "re"] + PYQT4_MODULES + MODULES,
}

setup(
    name=PROJECT_NAME,
    version="0.0.0.0",
    description=PROJECT_NAME,

    options={
        "build_exe": build_exe
    },

    executables=[
        Executable("__main__.py", base=BASE, targetName=PROJECT_NAME + ".exe")
    ]
)
