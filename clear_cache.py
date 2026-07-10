import os
import shutil

for root, dirs, files in os.walk("."):
    if "__pycache__" in dirs:
        cache_path = os.path.join(root, "__pycache__")
        shutil.rmtree(cache_path)
        print(f"Deleted: {cache_path}")

print("\n✅ All __pycache__ folders removed.")