from setuptools import setup

APP = ["src/app.py"]
DATA_FILES = ["icon.png"]
OPTIONS = {
    "argv_emulation": True,
    "iconfile": "icon.png",
    "plist": {"CFBundleShortVersionString": "1.0.0", "LSUIElement": True},
    "packages": ["rumps"],
}

setup(
    app=APP,
    name="PostureWatcher",
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
    install_requires=[
        "rumps",
        "keyboard",
        "mediapipe",
        "opencv-python",
        "beepy",
        "termcolor",
    ],
)
