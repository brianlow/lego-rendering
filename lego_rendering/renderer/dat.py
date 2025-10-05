import os

def ldraw_dat_exists(ldraw_id):
    # Check if the file exists in the parts directories
    part_filename = os.path.abspath(os.path.join("./ldraw/parts", f"{ldraw_id}.dat"))
    if os.path.exists(part_filename):
        return True

    # Check if the file exists in the unofficial parts directories
    part_filename = os.path.abspath(os.path.join("./ldraw/unofficial/parts", f"{ldraw_id}.dat"))
    if os.path.exists(part_filename):
        return True

    return False
