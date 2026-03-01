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
    "bakers": [
        {
            "baker": "Curvature.Raytraced",
            "identifier": "curvature",
            "parameters": {
                "auto_minmax": True,
                "base.uv_set": "Value from Common/base.uv_set",
                "cage_scene_path": "Value from CommonProjection/cage_scene_path",
                "high_scene_paths": "Value from CommonProjection/high_scene_paths",
                "is_selected": True,
                "normal_map_orientation": "directx",
                "normal_map_path": "",
                "normal_map_space": "tangent_space",
                "output_format": "Value from Common/output_format",
                "output_name": "Value from Common/output_name",
                "output_size": "Value from Common/output_size",
                "projection.cull_backfaces": "Value from CommonProjection/cull_backfaces",
                "projection.hit_strategy": "Value from CommonProjection/hit_strategy",
                "projection.max_depth": "Value from CommonProjection/max_depth",
                "projection.max_height": "Value from CommonProjection/max_height",
                "projection.mesh_match_mode": "Value from CommonProjection/mesh_match_mode",
                "projection.normalized_distance": "Value from CommonProjection/normalized_distance",
                "projection.offset_map_path": "Value from CommonProjection/offset_map_path",
                "projection.sampling_rate": "Value from CommonProjection/sampling_rate",
                "projection.skew_map_invert": "Value from CommonProjection/skew_map_invert",
                "projection.skew_map_path": "Value from CommonProjection/skew_map_path",
                "projection.smooth_normals": "Value from CommonProjection/smooth_normals",
                "secondary.mesh_match_mode": "match_all",
                "secondary.normalized_distance": False,
                "secondary.sample_count": 256,
                "secondary.sampling_radius": 0.001,
                "selected_meshes": "Value from Common/selected_meshes",
                "skew_correction": "Value from CommonProjection/skew_correction",
                "use_cage": "Value from CommonProjection/use_cage",
                "use_lowdef_as_highdef": "Value from CommonProjection/use_lowdef_as_highdef",
                "value_bounds": [-1, 1],
            },
        },
        {
            "baker": "AmbientOcclusion.Raytraced",
            "identifier": "ambient_occlusion",
            "parameters": {
                "attenuation": "linear",
                "base.uv_set": "Value from Common/base.uv_set",
                "cage_scene_path": "Value from CommonProjection/cage_scene_path",
                "culling_mode": "never",
                "enable_ground_plane": False,
                "ground_offset": 0,
                "high_scene_paths": "Value from CommonProjection/high_scene_paths",
                "is_selected": True,
                "normal_map_orientation": "directx",
                "normal_map_path": "",
                "normal_map_space": "tangent_space",
                "output_format": "Value from Common/output_format",
                "output_name": "Value from Common/output_name",
                "output_size": "Value from Common/output_size",
                "projection.cull_backfaces": "Value from CommonProjection/cull_backfaces",
                "projection.hit_strategy": "Value from CommonProjection/hit_strategy",
                "projection.max_depth": "Value from CommonProjection/max_depth",
                "projection.max_height": "Value from CommonProjection/max_height",
                "projection.mesh_match_mode": "Value from CommonProjection/mesh_match_mode",
                "projection.normalized_distance": "Value from CommonProjection/normalized_distance",
                "projection.offset_map_path": "Value from CommonProjection/offset_map_path",
                "projection.sampling_rate": "Value from CommonProjection/sampling_rate",
                "projection.skew_map_invert": "Value from CommonProjection/skew_map_invert",
                "projection.skew_map_path": "Value from CommonProjection/skew_map_path",
                "projection.smooth_normals": "Value from CommonProjection/smooth_normals",
                "secondary.max_distance": 1,
                "secondary.mesh_match_mode": "match_all",
                "secondary.min_distance": 0.00001,
                "secondary.normalized_distance": False,
                "secondary.sample_count": 256,
                "secondary.sample_distribution": "cosine",
                "secondary.spread_angle": 180,
                "selected_meshes": "Value from Common/selected_meshes",
                "skew_correction": "Value from CommonProjection/skew_correction",
                "use_cage": "Value from CommonProjection/use_cage",
                "use_lowdef_as_highdef": "Value from CommonProjection/use_lowdef_as_highdef",
            },
        },
    ],
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
