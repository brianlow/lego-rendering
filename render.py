import bpy
import os
import math
import sys
import random
from math import radians
from mathutils import Vector, Matrix

# This script runs under Blender's python environment. Add the current
# directly to the path so we can import our own modules
dir_path = os.path.dirname(os.path.realpath(__file__))
print(f"Prepending {dir_path} to Python path...")
sys.path.insert(0, dir_path)
from utils import rotate_object_randomly, place_object_on_ground, rotate_object_around_scene_origin, get_2d_bounding_box, draw_bounding_box, bounding_box_to_dataset_format, move_camera_back, reset_scene, change_object_color, move_object_away_from_origin, default_lighting, soft_lighting, hard_lighting, file_exists
from colors import Color, random_color_for_blender, random_color_for_pil
from background import save_background_image

# Yolo Detection
# - write out in Yolo format with bounding boxes
# - render multiple images, multiple parts
# - transparent colors
# - ability to specify color (can use hue augmentation)
# - list of parts + color combinations

# Part to render
# partnames = ["3001"]
# partnames = ["3001", "3004", "4274"]
# partnames = ["4073","3004","3022","3003","11211","3665","3713","60592","60483","6536"]
# 1000 most common parts 2018-2022 (except "15400", "60169", "61903", "76537" b/c of error 'Object does not have geometry data')
partnames = ["4073", "3023", "98138", "3024", "2780", "54200", "3069b", "3710", "25269", "3070b", "3004", "3005", "3020", "3022", "15573", "6558", "3623", "3021", "3666", "85984", "85861", "3010", "2431", "2412", "11477", "2420", "15068", "24866", "3001", "3003", "3062b", "3068b", "87079", "3795", "4274", "4032", "6636", "43093", "3622", "87580", "63864", "3040", "3460", "15712", "87087", "35480", "99780", "32062", "99207", "3941", "4070", "22885", "3009", "11211", "32028", "4589", "6091", "20482", "33909", "4162", "2357", "98283", "4085", "99206", "3034", "2877", "99563", "44728", "32952", "30136", "3660", "41740", "32123", "92280", "3665", "18654", "3700", "27925", "3039", "32054", "2654", "4519", "92946", "24246", "26603", "99781", "59443", "26601", "93273", "60478", "32607", "63868", "4477", "3245c", "11214", "48336", "61252", "3713", "3031", "87994", "49307", "50950", "24201", "18674", "28192", "30414", "3002", "26047", "32064", "34103", "61409", "32828", "6541", "3032", "3673", "3008", "48729", "32523", "36840", "62462", "11476", "32803", "30374", "60483", "60592", "15100", "32316", "14769", "2540", "3832", "32140", "23443", "11090", "29120", "32000", "60479", "14719", "32524", "6536", "11212", "2456", "4286", "61678", "27263", "29119", "4865", "60470", "18677", "41677", "2429c01", "4740", "60601", "32526", "36841", "18651", "42003", "30241", "87552", "53451", "85080", "60474", "32013", "26604", "11458", "3937", "35787", "60481", "3705", "2450", "37762", "32073", "14716", "15535", "2454", "3035", "3701", "64644", "37352", "2436", "2445", "64567", "6005", "22388", "14704", "3749", "11203", "43722", "63965", "40490", "3065", "43723", "24309", "22385", "4282", "3958", "30357", "49668", "87083", "4599b", "14696", "6134", "32278", "6632", "41770", "3037", "30413", "41769", "69729", "2432", "32525", "3659", "41682", "47457", "93274", "27507", "24316", "3036", "24299", "15070", "32184", "6628", "87620", "88323", "93606", "4460", "24307", "14417", "88072", "30565", "18653", "44865", "3007", "3176", "4081", "2423", "22961", "30153", "10247", "3298", "32556", "54657", "20310", "3747b", "33183", "51739", "298c02", "26287", "73825", "60596", "32034", "3957", "2465", "32039", "14418", "15470", "35464", "2453", "32016", "13547", "13965", "92947", "11478", "32002", "88646", "6112", "3033", "41239", "23969", "6111", "4733", "3678", "87544", "63869", "60484", "6231", "15392", "4490", "48092", "18980", "60477", "32606", "6014b", "3030", "21459", "30503", "44294", "55981", "3706", "4287", "88292", "11215", "73562", "60581", "3029", "32124", "87747", "15571", "25214", "36752a", "2417", "4624", "11253", "13548", "96874", "30237", "3709", "3045", "78258", "44301", "553", "32449", "2449", "15379", "88930", "4079b", "54383", "58176", "6589", "14395", "91988", "15533", "92950", "22888", "73230", "32270", "6179", "3894", "15462", "3684c", "60593", "6003", "54384", "4510", "52107", "37775", "59349", "3702", "4697b", "87697", "70681", "47905", "43888", "15208", "43898", "43857", "64647", "18649", "2476", "3703", "65509", "3829c01", "24855", "11609", "6232", "4216", "87082", "98100", "30350b", "11213", "60602", "27261", "4871", "17485", "15706", "41539", "3028", "11833", "60594", "92438", "4185", "32192", "87081", "3633", "3899", "30236", "2460", "32474", "23950", "3938", "3839b", "47456", "48989", "37695", "3895", "32291", "35044", "18646", "6587", "15254", "28974", "2653", "6126b", "50340", "65578", "79389", "32063", "42610", "2921", "22890", "25893", "47455", "78329", "2736", "27940", "89522", "30137", "30363", "15458", "4600", "59426", "64179", "11610", "89678", "3680", "10197", "3679", "34816", "32009", "6180", "15395", "67329", "39739", "13731", "75937", "86996", "2730", "57360", "6081", "2817", "69819", "30166", "33320", "3942c", "6553", "3297", "92013", "93095", "66792", "30383", "15403", "87609", "32056", "92582", "30165", "3707", "3830", "3831", "15303", "60476", "94925", "87414", "22886", "57895", "44567", "6106", "14419", "24122", "35459", "56145", "2419", "55013", "11947", "33078", "11946", "59895", "32015", "60849", "64799", "32530", "32014", "90195", "10202", "99021", "22667", "15456", "14718", "2723", "2496", "92402", "50745", "38320", "15332", "47458", "32001", "32018", "30099", "3038", "99008", "4488", "61184", "2343", "61485", "85943", "30602", "66956", "18575", "6215", "39789", "79756", "64225", "60616", "11208", "60485", "68013", "50951", "13564", "32348", "3708", "3738", "22484", "2639", "78256", "30000", "90194", "50254", "78666", "30031", "22889", "30162", "33243", "30176", "6191", "40345", "90258", "6629", "6060", "10928", "18853", "3006", "47397", "64782", "85975", "30028", "47398", "6182", "68568", "46212", "11209", "92690", "48171", "2599", "30145", "92410", "95344", "53923", "45590", "19119", "14720", "6157", "39793", "10884", "98282", "16577", "28326", "40344", "50304", "3960", "99773", "2462", "98834", "18041", "42022", "15461", "61482", "74967", "28870", "4345", "30157", "91501", "24375", "4346", "42023", "53585", "57909", "91405", "43719", "26599", "4590", "92907", "21445", "52031", "13971", "50305", "42918", "93160", "92338", "53119", "3737", "15209", "6254", "18977", "30044", "98585", "90540", "32271", "25375", "62113", "76766", "19220", "73109", "40379", "30504", "3743", "x346", "16770", "19807a", "4006", "30562", "49311", "2447", "32802", "88293", "27448", "43045", "52501", "43892", "23948", "38014", "92099", "24482", "38585", "11618", "60603", "2569", "55982", "33299", "15279", "30663", "60032", "85941", "18946", "2489", "4536", "41948", "33172", "66909", "95347", "60219", "50861", "32126", "64648", "48169", "61780", "65803", "93555", "58090", "4445", "2853", "32072", "2655", "68888", "65617", "3675", "50862", "30150", "48208", "27965", "45677", "30046", "92738", "3648", "71752", "44568", "55236", "61254", "4218", "4349", "32555", "2851", "48205", "87989", "4175", "87618", "24119", "64570", "32059", "15397", "4863", "3940b", "2850", "43710", "3027", "67810", "60212", "2852", "15391", "92409", "58247", "44375", "71708", "98397", "32932", "3044", "66789", "3049", "2825", "6187", "40378", "37776", "33085", "95228", "3676", "4528", "4595", "3185", "3046", "93604", "24116", "32324", "64847", "24946", "6020", "32249", "49731", "43713", "30089", "72454", "87617", "43056", "63082", "30586", "60607", "11291", "73507", "6192", "27393", "4533", "69910", "65249", "64727", "14413", "18759", "38583", "60583", "95188", "24593", "61072", "67095", "92692", "18976", "55615", "57585", "47755", "41748", "98139", "62361", "2739", "36451a", "6259", "33492", "56890", "51239", "41747", "36017", "43711", "79987", "6233", "3685", "49283", "99784", "53540", "4738a", "6183", "4735", "41854", "4739", "19121", "3956", "24093", "47753", "3228", "93594", "50943", "61408", "6190", "47847", "3837", "35442", "33051", "30505", "30151b", "6222", "40066", "21229", "88704", "15092", "60623", "51270", "60608", "35789", "30355", "48170", "35654", "3852b", "42862", "48165", "2926", "30340", "18920", "25061", "6575", "30356", "32017", "89201", "85543", "60208", "90370", "57697", "10187", "66727", "65426", "65098", "32557", "77765", "44674", "71709", "69858", "31990", "3043", "18948", "3823", "39794", "27256", "98721", "55976", "13349", "4176", "24599", "56904", "53400", "35470", "64448", "95343", "32198", "71682", "4522", "30987", "24869", "6564", "95199", "69755", "65473", "98137", "6154", "65429", "3821", "15745", "32250", "60808", "44126", "4727", "23405", "50337", "87408", "87080", "20309", "34173", "6239", "3822", "3456", "18854", "4151", "87407", "38340", "18838", "62531", "32065", "35700", "6583", "47759", "87086", "78444", "12885", "93593", "18910", "54671", "11010", "41669", "93595", "65138", "18944", "24324", "30526", "49577", "78443", "6565", "54672", "18945", "76797", "2815", "64951", "18974", "92851", "39613", "29111", "87421", "71710", "15413", "14181", "86876", "6124", "32235", "51266", "4083", "15540", "54661", "65092", "4161", "44224", "30093", "44809", "15362", "30361", "24947", "2340", "35186", "6249", "25386", "64867", "30385", "30395", "64683", "14226c11", "43712", "11954", "64391", "30134", "15469", "54662", "2415", "32125", "3299", "35443", "80015", "61800", "92107", "6148", "3464", "41531", "22391", "42876", "72869", "92585", "87693", "62360", "11455", "93789", "41767", "53401", "77808", "18034", "32529", "66857", "50956", "33322", "92220", "2486", "3943", "74698", "78594", "79757", "24314", "6256", "57520", "30043", "92842", "50955", "44709", "4489", "2854", "15445", "93571", "4515", "42446", "65635", "28588", "90202", "72206", "71771", "23986", "87585", "35485", "44225", "66955", "15460", "3836", "50949", "3300", "60599", "74261", "33121", "29109", "32739", "13608", "42205", "48933", "41768", "88393", "1748", "27262", "78257"]



# Set the number of images to generate
num_images_per_part = 2

# 10% of generated images will be used for validation, remaining for training
# Setting this to 0 when experimenting makes it easier to review the results
percent_val = 0.2

# True for quick draft renders (1s per image on M1 Mac), False for high quality renders (10s per image on M1 Mac)
draft = False

# Randomize object color, orientation and lighting
randomize = True

# Percentage of images to render as backgrounds with no parts
percent_background = 0.0



# Input output paths
ldraw_path = "./ldraw"
ldraw_parts_path = "./ldraw/parts"
renders_path = "./renders"
dataset_yaml_path = "./renders/dataset.yaml"
dataset_path = "./renders/dataset"
train_path = "./renders/dataset/train"
val_path = "./renders/dataset/val"

os.makedirs(train_path, exist_ok=True)
os.makedirs(os.path.join(train_path, "images"), exist_ok=True)
os.makedirs(os.path.join(train_path, "labels"), exist_ok=True)
os.makedirs(val_path, exist_ok=True)
os.makedirs(os.path.join(val_path, "images"), exist_ok=True)
os.makedirs(os.path.join(val_path, "labels"), exist_ok=True)

# Render at the resolution needed by YOLO (i.e. standard Imagenet size)
render_width = 224
render_height = 224

# Render parts
for partname in partnames:
    if file_exists(f"{partname}_*", dataset_path):
        print(f"Skipping {partname} as it already exists in the dataset")
        continue

    bpy.ops.object.select_all(action='DESELECT')

    # Select all objects in the current scene
    for obj in bpy.context.scene.objects:
        if obj.type not in {'LIGHT', 'CAMERA'}:
            obj.select_set(True)

    # Delete selected objects
    bpy.ops.object.delete()


    # Import the part into Blender
    # Options for importing the part
    # https://github.com/TobyLobster/ImportLDraw/blob/09dd286d294672c816d33e70ac10146beb69693c/importldraw.py
    part_filename = os.path.abspath(os.path.join(ldraw_parts_path, f"{partname}.dat"))
    print(f"Importing {part_filename}")
    options = {
        "ldrawPath": os.path.abspath(ldraw_path),
        "addEnvironment": True,                       # add a white ground plane
        "resPrims": "Standard" if draft else "High",  # high resolution primitives
        "useLogoStuds": False if draft else True,     # LEGO logo on studs
    }
    if not os.path.exists(part_filename):
        print(f"Part file not found: {part_filename}")
        continue
    bpy.ops.import_scene.importldraw(filepath=part_filename, **options)
    bpy.ops.object.select_all(action='DESELECT')

    part = bpy.data.objects[0]
    light = bpy.data.objects['Light']
    camera = bpy.data.objects['Camera']

    # Do this after import b/c the importer overwrites some of these settings
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 16 if draft else 256 # increase for higher quality
    bpy.context.scene.cycles.max_bounces = 2
    bpy.context.scene.render.resolution_x = render_width
    bpy.context.scene.render.resolution_y = render_height

    # There is a problem getting a bounding box for some parts
    # Trigger this failure early so we don't leave an orphaned image
    get_2d_bounding_box(part, camera)

    for i in range(num_images_per_part):
        output_path = val_path if random.random() <= percent_val else train_path
        image_filename = os.path.join(output_path, "images", partname + "_{}.png".format(i))
        label_filename = os.path.join(output_path, "labels", partname + "_{}.txt".format(i))

        # Randomly rotate the part
        if randomize:
            rotate_object_randomly(part)
            place_object_on_ground(part)
            change_object_color(part, random_color_for_blender())

        # Move the light so each image has a random shadow
        # The importer creates a light for us at roughly 45 angle above the part so
        # we rotate it around the part (at the origin)
        if randomize:
            rotate_object_around_scene_origin(light, random.uniform(0, 360))
            lighting = [default_lighting, soft_lighting, hard_lighting]
            random.choice(lighting)(light)
        else:
            rotate_object_around_scene_origin(light, 20)
            default_lighting(light)

        # Aim and position the camera so the part is centered in the frame.
        # The importer can do this for us but we rotate and move the part
        # after importing so would need to do it again anyways.
        part.select_set(True)
        bpy.ops.view3d.camera_to_view_selected()
        move_camera_back(camera, .4)

        # Render
        bpy.context.scene.render.filepath = image_filename
        bpy.ops.render.render(write_still=True)

        # Save label and bounding box
        bounding_box = get_2d_bounding_box(part, camera)
        # draw_bounding_box(bounding_box, image_filename)
        bounding_box = bounding_box_to_dataset_format(bounding_box, render_width, render_height)
        with open(label_filename, 'w') as f:
            f.write(f"0 {bounding_box[0]:.3f} {bounding_box[1]:.3f} {bounding_box[2]:.3f} {bounding_box[3]:.3f}\n")

# Save a Blender file so we can debug this script
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(os.path.join(renders_path, "render.blend")))

# Render backgrounds
num_images = len(partnames) * num_images_per_part
num_background_images = int(num_images * percent_background)
for i in range(num_background_images):
    # pick random color but prefer white to match converyor belt
    color = random_color_for_pil() if random.random() < 0.5 else (255, 255, 255)
    # pick random number of shapes to draw but prefer no shapes
    num_shapes = 0 if random.random() < 0.5 else random.randint(0, 20)
    image_filename = os.path.join(train_path, "images", "background_{}.png".format(i))
    label_filename = os.path.join(train_path, "labels", "background_{}.txt".format(i))
    filename = os.path.join(train_path, "images", )
    save_background_image(color, (render_width, render_height), num_shapes, image_filename)
    with open(label_filename, 'w') as f:
        pass

# Output a dataset yaml file
with open(dataset_yaml_path, 'w') as f:
  f.write(f"# Path must be an absolute path unless it is Ultralytics standard location\n")
  f.write(f"path: {os.path.abspath(dataset_path)}\n")
  f.write(f"train: train/images\n")
  f.write(f"val: val/images\n")
  f.write(f"\n")
  f.write(f"names:\n")
  f.write(f"  0: lego\n")
