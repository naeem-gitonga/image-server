import gc
import os
import subprocess
import torch
env = os.getenv("ENV")

def cleanup_memory():
    print("[CLEANUP] Releasing model + RAM...")
    try:
        from app.image_generator import _pipeline
        _pipeline = None
    except:
        pass

    gc.collect()

    try:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
    except:
        pass
    
    print("[CLEANUP] Done!")


def clear_buffer_cache(): # ? This function is helpful for dev because after shutting down the app I often want my buffer cleared... 
    if env != "prod":
        try:
            subprocess.run(
                ['sh', '-c', 'echo 3 > /proc/sys/vm/drop_caches'],
                check=True,
                capture_output=True,
                text=True
            )
            print('Buffer cleared')
        except subprocess.CalledProcessError as e:
            print(f"Failed to drop caches: {e.stderr}")