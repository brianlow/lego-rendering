# Lego Rendering Pipeline

These scripts render individual parts on a white background from various angles.
Used for training an image classifier for lego sorting where the background
and lighting can be controlled.


# Setup
- [Blender](https://blender.org)
- [ImportLDraw Plugin](https://github.com/TobyLobster/ImportLDraw)
- [LDraw parts library](https://library.ldraw.org/updates?latest)
  - extract into ./ldraw, e.g. ./ldraw/parts/30010.dat
- Python

```
./setup.sh

 cd /Applications/Blender.app/Contents/Resources/3.5/python/bin
 ./python3-10 -m pip install pillow
```


# Run

./render.sh


# Get the dataset onto Paperspace

# zip
zip -r myzip.zip renders/dataset renders/dataset.yaml

# upload
aws s3 cp myzip.zip s3://brian-lego-public/myzip.zip

# download
wget https://brian-lego-public.s3.us-west-1.amazonaws.com/myzip.zip -o myzip.zip


unzip lego-2k-images-10classes.zip
mv renders lego-2k-images-10classes
edit the path in dataset.yaml
cd /notebooks
pip install -r requirements.txt
export COMET_API_KEY=...
python train.py

# Output format
my_dataset.yml
my_dataset/
  train/
    images/
      3001_1.png
      3001_2.png
    labels/
      3001_1.txt
      3001_2.txt
  val/
    images/
      3001_1.png
      3001_2.png
    labels/
      3001_1.txt
      3001_2.txt
