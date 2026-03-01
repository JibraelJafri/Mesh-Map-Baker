import os
import subprocess
import math

# ======================================================================
# CONFIGURATION
# ======================================================================
BAKER_EXE = r"D:\Program Files\Adobe Substance 3D Designer\substance3d_baker.exe"
RENDER_EXE = r"D:\Program Files\Adobe Substance 3D Designer\sbsrender.exe"


def clean_path(path_str):
    if not path_str:
        return ""
    return os.path.abspath(path_str.strip()).replace("\\", "/")


def get_log2_res(pixel_res):
    return int(math.log2(pixel_res))


def check_executables():
    missing = []
    if not os.path.exists(BAKER_EXE):
        missing.append("substance3d_baker.exe")
    if not os.path.exists(RENDER_EXE):
        missing.append("sbsrender.exe")
    return missing
