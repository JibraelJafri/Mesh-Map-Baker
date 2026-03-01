import os
import subprocess
import math
import json

# ======================================================================
# CONFIGURATION
# ======================================================================
BAKER_EXE = r"D:\Program Files\Adobe Substance 3D Designer\substance3d_baker.exe"
RENDER_EXE = r"D:\Program Files\Adobe Substance 3D Designer\sbsrender.exe"

BASE_JSON = {
    "Common": {
        "base.uv_set": 0,
        "output_format": "png",
        "output_name": "$(scenename)_$(bakername)",
        "output_size": [2048, 2048],
        "selected_meshes": [],
    },
    "CommonProjection": {
        "cage_scene_path": "",
        "cull_backfaces": True,
        "high_scene_paths": [],
        "hit_strategy": "inward",
        "max_depth": 0.01,
        "max_height": 0.01,
        "mesh_match_mode": "match_all",
        "normalized_distance": False,
        "offset_map_path": "",
        "sampling_rate": "2x2",
        "skew_correction": False,
        "skew_map_invert": False,
        "skew_map_path": "",
        "smooth_normals": True,
        "use_cage": False,
        "use_lowdef_as_highdef": True,
    },
    "bakers": [],
    "enable_mip_diffusion": True,
    "low_scene_path": "",
    "output_path": "",
    "padding_radius": 2,
    "per_fragment_binormal": True,
    "recompute_tangents": False,
    "sbsoutput_place_into_specific_folder": False,
    "sbsoutput_resource_method": "linked",
    "settingsInfo": {"version": 2},
    "uv_tiles": [[0, 0]],
}


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
