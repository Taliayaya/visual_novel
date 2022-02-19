import os


def getAbsolutePath(script_dir, rel_path):
    return os.path.join(script_dir, rel_path)
