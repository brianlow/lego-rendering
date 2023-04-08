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
