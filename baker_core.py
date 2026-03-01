import os
import subprocess

# ======================================================================
# CONFIGURATION
# ======================================================================
BAKER_EXE = r"D:\Program Files\Adobe Substance 3D Designer\substance3d_baker.exe"
RENDER_EXE = r"D:\Program Files\Adobe Substance 3D Designer\sbsrender.exe"


def check_executables():
    missing = []
    if not os.path.exists(BAKER_EXE):
        missing.append("substance3d_baker.exe")
    if not os.path.exists(RENDER_EXE):
        missing.append("sbsrender.exe")
    return missing
