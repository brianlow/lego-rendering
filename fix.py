import os


random_views_dir = "./renders/random-views"

# for each subfolder in random_view_dir
#   for each image file (.jpg | .jpeg | .png)
#      pritn a warning if the image file doesn't have a .txt file with the same name


for root, dirs, files in os.walk(random_views_dir):
    for file in files:
        if file.endswith(('.jpg', '.jpeg', '.png')):
            image_file_path = os.path.join(root, file)
            label_file_path = os.path.splitext(image_file_path)[0] + ".txt"
            if not os.path.exists(label_file_path):
                # delete the image file
                os.remove(image_file_path)
                print(f"WARNING: {image_file_path} does not have a corresponding label file.")
