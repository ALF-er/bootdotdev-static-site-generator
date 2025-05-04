import os
import shutil

def copy_dir_content(src, dst):
    if not os.path.exists(src):
        raise Exception("source directory doesn't exist")

    if os.path.exists(dst):
        shutil.rmtree(dst)

    os.mkdir(dst)

    dir_items = os.listdir(src)

    for item in dir_items:
        item_path = os.path.join(src, item)

        if os.path.isfile(item_path):
            shutil.copy(item_path, dst)
        else:
            copy_dir_content(item_path + "/", os.path.join(dst, item + "/"))
