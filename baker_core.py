import os
import json
import subprocess
import time
import math
import shutil

# ======================================================================
# CONFIGURATION
# ======================================================================
BAKER_EXE = r"D:\Program Files\Adobe Substance 3D Designer\substance3d_baker.exe"
RENDER_EXE = r"D:\Program Files\Adobe Substance 3D Designer\sbsrender.exe"

# Updated with the new Color.Raytraced baker
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
        "normalized_distance": True,
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
            "baker": "Thickness.Raytraced",
            "identifier": "thickness",
            "parameters": {
                "base.uv_set": "Value from Common/base.uv_set",
                "cage_scene_path": "Value from CommonProjection/cage_scene_path",
                "high_scene_paths": "Value from CommonProjection/high_scene_paths",
                "is_selected": True,
                "maximize_range": "min_max",
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
                "secondary.max_distance": 0.1,
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
    return os.path.abspath(path_str.strip(" \"'")).replace("\\", "/")


def get_log2_res(pixel_res):
    return int(math.log2(pixel_res))


def check_executables():
    missing = []
    if not os.path.exists(BAKER_EXE):
        missing.append("substance3d_baker.exe")
    if not os.path.exists(RENDER_EXE):
        missing.append("sbsrender.exe")
    return missing


def run_pipeline(
    input_files, output_dir, sbsar_path, resolution, out_format, sampling_rate, ray_count, cleanup_temps, log_callback, progress_callback
):
    """
    Main logic loop. Now accepts a specific list of file paths.
    """
    output_dir = clean_path(output_dir)
    sbsar_path = clean_path(sbsar_path)
    log2_res = get_log2_res(resolution)

    if not input_files:
        log_callback(f"[!] No valid 3D files provided.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    json_dir = clean_path(os.path.join(output_dir, "_bake_plans"))
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)

    success_count = 0
    start_time = time.time()

    log_callback(f"Queued {len(input_files)} meshes. Starting pipeline...\n")

    for i, mesh_path in enumerate(input_files, 1):
        mesh_path = clean_path(mesh_path)
        mesh_name = os.path.basename(mesh_path)
        mesh_base = os.path.splitext(mesh_name)[0]

        log_callback(f"[{i}/{len(input_files)}] Processing: {mesh_name}")
        progress_callback(i - 1, len(input_files))

        # --- BAKING ---
        log_callback(f"  -> [Phase 1] Baking Textures ({sampling_rate} AA, {ray_count} Rays)...")

        current_json = BASE_JSON.copy()

        # Inject standard options
        current_json["low_scene_path"] = mesh_path
        current_json["output_path"] = output_dir
        current_json["Common"]["output_size"] = [resolution, resolution]
        current_json["Common"]["output_format"] = out_format

        # Inject Power User options (AA and Rays)
        current_json["CommonProjection"]["sampling_rate"] = sampling_rate
        for baker in current_json["bakers"]:
            if "secondary.sample_count" in baker["parameters"]:
                baker["parameters"]["secondary.sample_count"] = int(ray_count)

        json_path = os.path.join(json_dir, f"{mesh_base}_bake.json")
        with open(json_path, "w") as f:
            json.dump(current_json, f, indent=2)

        bake_cmd = [BAKER_EXE, "run", "--json", json_path]

        try:
            subprocess.run(bake_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.decode("utf-8").strip() if e.stderr else "Unknown error"
            log_callback(f"  [!] Bake failed. Code: {e.returncode}. {err_msg}")
            continue

        # --- PACKING ---
        log_callback("  -> [Phase 2] Packing via SBSAR...")

        ao_file = os.path.join(output_dir, f"{mesh_base}_ambient_occlusion.{out_format}")
        curv_file = os.path.join(output_dir, f"{mesh_base}_curvature.{out_format}")
        thick_file = os.path.join(output_dir, f"{mesh_base}_thickness.{out_format}")
        if not all(os.path.exists(f) for f in [ao_file, curv_file, thick_file]):
            log_callback(f"  [!] Missing baked textures! Skipping packing for {mesh_base}.")
            continue

        render_cmd = [
            RENDER_EXE,
            "render",
            "--input",
            sbsar_path,
            "--no-report",
            "--output-name",
            f"OCT_{mesh_base}",
            "--output-path",
            output_dir,
            "--output-format",
            out_format,
            "--set-value",
            f"$outputsize@{log2_res},{log2_res}",
            "--set-entry",
            f"occlusion@{ao_file}",
            "--set-entry",
            f"curvature@{curv_file}",
            "--set-entry",
            f"thickness@{thick_file}",
        ]

        try:
            subprocess.run(render_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            log_callback(f"  -> [SUCCESS] Created: OCT_{mesh_base}.{out_format}")
            success_count += 1

            # --- HOUSEKEEPING ---
            if cleanup_temps:
                log_callback("  -> [Phase 3] Cleaning up temp maps...")
                for temp_file in [ao_file, curv_file, thick_file]:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)

        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.decode("utf-8").strip() if e.stderr else "Unknown error"
            log_callback(f"  [!] Packing failed. Code: {e.returncode}. {err_msg}")

        log_callback("-" * 40)

    # Final Folder Housekeeping
    if cleanup_temps and os.path.exists(json_dir):
        shutil.rmtree(json_dir)

    # End summary
    elapsed = round(time.time() - start_time, 2)
    progress_callback(len(input_files), len(input_files))  # Fill progress bar
    log_callback(f"\nPIPELINE COMPLETE! ({success_count}/{len(input_files)} successful)")
    log_callback(f"Time elapsed: {elapsed} seconds")
    log_callback(f"Final output: {output_dir}")
