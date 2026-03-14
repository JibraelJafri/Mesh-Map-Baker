# Substance 3D Auto-Baker & Channel Packer

A batch automation pipeline and graphical desktop utility for **Adobe Substance 3D Designer / Automation Toolkit CLI**. It automates the generation of raytraced mesh utility maps (Ambient Occlusion, Curvature, Thickness, and Color ID) and packs them into a single channel-packed texture (OCT) via a compiled Substance Archive (`.sbsar`).

---

## Features

- **Automated Substance CLI Baking**: Headless execution of `substance3d_baker.exe` using custom JSON bake plans.
- **Raytraced Baking Pipeline**:
  - **Ambient Occlusion** (Raytraced, DirectX tangent space)
  - **Curvature** (Raytraced, auto min-max normalization)
  - **Thickness** (Raytraced, spread angle sampling)
  - **Color ID** (Raytraced, mesh-index grayscale ID mask)
- **SBSAR Channel Packing**: Packed into a single RGBA texture via `sbsrender.exe`:
  - **R Channel**: Ambient Occlusion
  - **G Channel**: Curvature
  - **B Channel**: Thickness
  - **A Channel**: Color / Mesh ID
- **Smart Mesh Parser**: Multi-select 3D meshes (`.fbx`, `.obj`, `.usd`, `.usda`, `.usdc`, `.glb`, `.gltf`) or drag/paste directories.
- **Configurable Quality Settings**: Resolution (512 to 8192), Super-sampling Antialiasing (1x1 to 8x8), Ray Counts (16 to 256), and file format export (`png`, `tiff`, `exr`, `jpeg`, `tga`).
- **Housekeeping & Cleanup**: Automatically cleans up intermediate single-channel maps and temporary bake plan manifests.
- **Asynchronous Desktop GUI**: Built with Tkinter and dark theme integration (`sv_ttk`), running operations on background worker threads with real-time log output and progress tracking.

---

## Prerequisites

- Python 3.10+
- Adobe Substance 3D Designer (installed with CLI tools: `substance3d_baker.exe` and `sbsrender.exe`).
- *(Optional)* `sv_ttk` for modern dark theme support:
  ```bash
  pip install sv_ttk
  ```

---

## Configuration

Update executable paths in `baker_core.py` if Substance 3D Designer is installed in a custom location:

```python
BAKER_EXE = r"D:\Program Files\Adobe Substance 3D Designer\substance3d_baker.exe"
RENDER_EXE = r"D:\Program Files\Adobe Substance 3D Designer\sbsrender.exe"
```

---

## Usage

### GUI Application
Launch the desktop interface:
```bash
python baker_gui.py
```

1. Click **Browse** under **Selected Meshes** and pick one or more 3D model files.
2. The output directory is automatically configured to `{ModelDirectory}/Mesh_Maps`.
3. Choose your desired output resolution (e.g. `2048`), format (`png`), AA (`2x2`), and ray count (`256`).
4. Click **START PIPELINE**.

### Headless CLI / Python API
Import and run directly from scripts:
```python
import baker_core

baker_core.run_pipeline(
    input_files=["path/to/mesh_a.fbx", "path/to/mesh_b.obj"],
    output_dir="path/to/output_maps",
    sbsar_path="Mesh_Maps_Packer.sbsar",
    resolution=2048,
    out_format="png",
    sampling_rate="2x2",
    ray_count=256,
    cleanup_temps=True,
    log_callback=print,
    progress_callback=lambda current, total: print(f"{current}/{total}")
)
```

---

## License

MIT License.
