# ComfyUI GPU Power Limit Node

A custom **ComfyUI node** to change NVIDIA GPU power limits dynamically while passing through any input.

This node **warns** if ComfyUI is not running as administrator/root — it does not attempt to elevate the process.

---

## Features

* Set NVIDIA GPU power limit on the fly.
* Supports multiple GPU indexes.
* Passes through all inputs without modification.
* Compatible with common ComfyUI types:

  * `AUDIO`, `IMAGE`, `LATENT`, `CLIP`, `CONDITIONING`
  * `VAE`, `MODEL`, `STRING`, `INT`, `FLOAT`, `MASK`
* Windows and Linux compatible.
* Warns if admin/root privileges are missing.

---

## Installation

1. Copy the folder `comfyui-powerlimit` into your ComfyUI custom nodes directory:

```
F:\NewAI\ComfyUI_windows_portable\ComfyUI\custom_nodes\comfyui-powerlimit
```

2. Folder structure should be:

```
comfyui-powerlimit/
├── __init__.py
└── powerlimit_node.py
```

3. Start ComfyUI. The node will appear under the **System** category as **Set GPU Power Limit**.

---

## Usage

1. Add the **Set GPU Power Limit** node to your ComfyUI graph.
2. Set:

   * `gpu_index`: GPU to apply the power limit to.
   * `power_limit`: Desired power limit in watts.
3. Connect any input(s) — all input types will pass through automatically.
4. The node will **warn** if ComfyUI is not running as admin/root.

---

## Example: Running ComfyUI as Administrator (Windows)

To allow the node to set GPU power limits, run ComfyUI with admin privileges. You can modify your startup batch file like this:

```
@echo off
:: Get the directory of the batch file
cd /d "%~dp0"

:: Check for admin rights
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

:: Run ComfyUI
python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --listen --disable-smart-memory

pause
```

* This will **restart the batch file with admin privileges** if needed.
* On Linux/macOS, you can launch ComfyUI with `sudo`:

```
sudo python3 ComfyUI/main.py
```

---

## Example Node Source

```python
from comfyui_powerlimit.powerlimit_node import SetPowerLimitNode
```

The node supports passthrough for all common types:

```
audio, image, latent, clip, conditioning,
vae, model, text, integer, number, mask
```

---

## Notes

* You **must run ComfyUI as admin/root** for the node to set GPU power limits.
* The node will **only warn** if privileges are missing; it will not fail the graph.
* The default power limit is read from the GPU at startup.

---
