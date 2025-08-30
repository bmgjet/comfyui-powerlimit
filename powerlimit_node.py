import subprocess
import sys
import os
from typing import Any

class SetPowerLimitNode:
    """
    ComfyUI custom node to set NVIDIA GPU power limit using nvidia-smi.
    Passes through any input unchanged.
    Warns if admin/root privileges are missing.
    """

    default_power_limit = 600

    # Try to read the current power limit on load
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=power.limit", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, check=True
        )
        limits = result.stdout.strip().split("\n")
        if limits and limits[0].replace(".", "", 1).isdigit():
            default_power_limit = int(float(limits[0]))
            print(f"[SetPowerLimitNode] Default GPU power limit detected: {default_power_limit}W")
    except Exception as e:
        print(f"[SetPowerLimitNode] Could not read default power limit, using {default_power_limit}W. Error: {e}")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "gpu_index": ("INT", {"default": 0, "min": 0, "max": 8, "step": 1}),
                "power_limit": ("INT", {"default": cls.default_power_limit, "min": 50, "max": 600, "step": 1}),
            },
            "optional": {
                "audio": ("AUDIO",),
                "image": ("IMAGE",),
                "latent": ("LATENT",),
                "clip": ("CLIP",),
                "conditioning": ("CONDITIONING",),
                "vae": ("VAE",),
                "model": ("MODEL",),
                "text": ("STRING",),
                "integer": ("INT",),
                "number": ("FLOAT",),
                "mask": ("MASK",),
            }
        }

    RETURN_TYPES = (
        "AUDIO", "IMAGE", "LATENT", "CLIP", "CONDITIONING",
        "VAE", "MODEL", "STRING", "INT", "FLOAT", "MASK"
    )
    RETURN_NAMES = RETURN_TYPES
    FUNCTION = "set_power_limit"
    CATEGORY = "System"
    OUTPUT_IS_LIST = tuple(False for _ in RETURN_TYPES)

    def is_admin(self):
        if os.name == "nt":
            try:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except Exception:
                return False
        else:
            return os.geteuid() == 0

    def run_nvidia_smi(self, gpu_index: int, power_limit: int):
        if not self.is_admin():
            print(f"[SetPowerLimitNode] WARNING: Missing admin/root privileges. Cannot set GPU {gpu_index} power limit.")
            return

        try:
            if os.name == "nt":
                args = f'-i {gpu_index} -pl {power_limit}'
                subprocess.run([
                    "powershell",
                    "Start-Process",
                    "nvidia-smi",
                    "-ArgumentList",
                    f'"{args}"',
                    "-Verb",
                    "runAs"
                ], check=True)
            else:
                subprocess.run(
                    ["nvidia-smi", "-i", str(gpu_index), "-pl", str(power_limit)],
                    check=True
                )
            print(f"[SetPowerLimitNode] GPU {gpu_index} power limit set to {power_limit}W")
        except subprocess.CalledProcessError as e:
            print(f"[SetPowerLimitNode] Failed to set power limit: {e}")
        except FileNotFoundError:
            print("[SetPowerLimitNode] nvidia-smi not found.")

    def set_power_limit(
        self,
        gpu_index: int, power_limit: int,
        audio: Any=None, image: Any=None, latent: Any=None,
        clip: Any=None, conditioning: Any=None, vae: Any=None,
        model: Any=None, text: Any=None, integer: Any=None,
        number: Any=None, mask: Any=None,
    ):
        self.run_nvidia_smi(gpu_index, power_limit)
        return (
            audio, image, latent, clip, conditioning,
            vae, model, text, integer, number, mask
        )


NODE_CLASS_MAPPINGS = {
    "SetPowerLimitNode": SetPowerLimitNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SetPowerLimitNode": "Set GPU Power Limit"
}
