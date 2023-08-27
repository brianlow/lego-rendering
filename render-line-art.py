import bpy
import sys
import os

# This script runs under Blender's python environment. Add the current
# directly to the path so we can import our own modules
dir_path = os.path.dirname(os.path.realpath(__file__))
print(f"Prepending {dir_path} to Python path...")
sys.path.insert(0, dir_path)

from lib.renderer.renderer import Renderer
from lib.renderer.render_options import RenderOptions, Quality, LightingStyle, Look, Format
from lib.colors import RebrickableColors

# This is a list of LDraw parts for parts in the 447 dataset
# I am using to train a classifier. It includes every mold variation
# and LDraw model for each Rebrickable canonical part num. Run
# query on the bricks.db from `lego-inventory`
#
# select distinct e.external_id
# from datasets d
# left join canonical_parts c on d.part_num = c.canonical_part_num
# left join external_ids e on e.part_num = c.part_num
# where d.id = '447'
# and e."type" = 'LDraw'

ldraw_ids = [
"10197",
"10288",
"10314",
"11090",
"11211",
"11212",
"11213",
"11214",
"11215",
"11272",
"11458",
"11476",
"11477",
"11478",
"12939",
"15254",
"3307",
"13547",
"13548",
"14417",
"14419",
"14704",
"14707",
"18838",
"6108",
"14716",
"14720",
"14769",
"15068",
"15070",
"15092",
"15100",
"65487",
"15332",
"15395",
"15397",
"15460",
"15461",
"46189",
"15470",
"15535",
"15672",
"15706",
"17485",
"18649",
"18651",
"18653",
"18674",
"18677",
"28809",
"18969",
"20482",
"21229",
"22385",
"22388",
"22390",
"22391",
"22484",
"22885",
"22888",
"22889",
"22890",
"22961",
"14395",
"2339",
"2357",
"2362a",
"2362b",
"87544",
"23969",
"24014",
"24122",
"2412a",
"2412b",
"30244",
"2419",
"43127",
"2420",
"63325",
"24246",
"24299",
"2431",
"24316",
"2436b",
"2436a",
"28802",
"24375",
"2441",
"2445",
"2450",
"2453a",
"2453b",
"2454",
"2454a",
"2454b",
"46212a",
"2456",
"44237",
"2458",
"44865",
"2460",
"2476a",
"2476b",
"2486",
"24866",
"25269",
"2529",
"60607",
"2540",
"12825",
"15712",
"2555",
"93794",
"25893a",
"79194",
"26047",
"2639",
"2654a",
"26601",
"26604",
"27255",
"27262",
"27266",
"2730",
"2736",
"27940",
"2853",
"2854",
"2877",
"2904",
"2921",
"2926",
"30000",
"3001",
"3001",
"u8004a",
"3002",
"3002",
"3003",
"3003",
"u8002a",
"3004",
"93792",
"30044",
"30046",
"3005",
"30071",
"3007",
"3008",
"63322",
"3008",
"3009",
"30099",
"3010",
"30136",
"30157",
"30157a",
"30157b",
"40687",
"30165",
"30179",
"60596",
"3020",
"u8200",
"3021",
"3022",
"94148",
"28653",
"3023",
"3023a",
"30237",
"95820",
"3024",
"3028",
"3031",
"3032",
"3033",
"3034",
"u8201",
"3035",
"u8202",
"30357",
"30361a",
"30361d",
"30363",
"30367b",
"30367c",
"3262",
"3037",
"3038",
"3039",
"3040a",
"3040b",
"30414",
"3045",
"30503",
"30553",
"482",
"57360",
"30565",
"30068",
"3062b",
"3063b",
"85080",
"3068a",
"3068b",
"3069a",
"3069b",
"3070a",
"3070b",
"3185",
"32000",
"32002",
"32013",
"32014",
"32015",
"32016",
"32017",
"32028",
"32034",
"32039",
"42135",
"32054",
"65304",
"32056",
"32059",
"32064a",
"32064c",
"32064b",
"32064d",
"32064a",
"32064c",
"32073",
"32123a",
"32123b",
"32124",
"32126",
"32140",
"32184",
"32187",
"32192",
"924",
"32198",
"32209",
"59426",
"32250",
"32278",
"64871",
"32291",
"32316",
"32348",
"32449",
"3245a",
"3245b",
"3245c",
"772",
"32523",
"32524",
"32526",
"32529",
"32530",
"32557",
"32828",
"32932",
"3298",
"3298",
"16577",
"3308a",
"33291",
"33299a",
"33299b",
"33299",
"33299b",
"33909",
"3403",
"3455",
"92950",
"3460",
"35044",
"3622",
"45505",
"3623",
"3633",
"3639",
"3640",
"10928",
"3647",
"24505",
"3648b",
"3648a",
"3648",
"3648b",
"3659",
"3660b",
"76959",
"3665a",
"3665b",
"3666",
"3673",
"3676",
"3679",
"3680",
"3684a",
"3684a",
"3684c",
"36840",
"36841",
"3700",
"389",
"3701",
"32062",
"3704",
"3705",
"3706",
"3707",
"3710",
"3713",
"6590",
"3747a",
"3747b",
"3749",
"15573",
"3794a",
"3794b",
"3795",
"3823",
"3832",
"3854",
"60608",
"3873",
"3895",
"3941",
"6143",
"3942a",
"3942b",
"3942c",
"3957a",
"3957b",
"3958",
"35394",
"3960",
"39739",
"4032a",
"4032b",
"40490",
"64289",
"30069",
"4070",
"4070",
"4081b",
"4083",
"4085a",
"4085b",
"4085c",
"60897",
"40902",
"53029",
"4132",
"60598",
"41530",
"41532",
"57697",
"4162",
"41677",
"41678",
"41682",
"41740",
"41747",
"41748",
"4176",
"41768",
"41769",
"41770",
"4185",
"4185a",
"4185b",
"42003",
"41762",
"42022",
"42023",
"4215a",
"30007",
"4215b",
"60581",
"4216",
"4218b",
"28974a",
"42446",
"4274",
"4282",
"4286",
"4287",
"4287a",
"4287b",
"4287c",
"15207",
"30413",
"43708",
"43712",
"43713",
"43719",
"43898",
"44126",
"44568",
"4460b",
"44728",
"4477",
"44809",
"44874",
"87082",
"4488",
"4490",
"4510",
"4519",
"45590",
"45677",
"4589",
"59900",
"4600",
"4727",
"4733",
"47397",
"47398",
"4740",
"4742",
"47456",
"47753",
"47755",
"47905",
"19159",
"47994",
"48092",
"48169",
"48171",
"48336",
"13349",
"4855",
"4864a",
"4864b",
"87552",
"4865a",
"4865b",
"4871",
"48723",
"48729a",
"48729b",
"48933",
"48989",
"65489",
"49668",
"49673",
"50304",
"50305",
"50373",
"50950",
"51739",
"52031",
"52501",
"30552",
"481",
"53923",
"54200",
"54383",
"54384",
"30387",
"54661",
"55013",
"55981",
"57518",
"88323",
"57519",
"57520",
"57585",
"57895",
"60803",
"17114",
"57908",
"57909",
"57910",
"62712",
"92013",
"58090",
"6578",
"58176",
"59443",
"60032",
"6005",
"92903",
"6014",
"6014",
"6014",
"6015",
"87697",
"6020",
"60470a",
"60470b",
"50340",
"60471",
"60474",
"60475a",
"60475b",
"60476",
"60477",
"60478",
"60479",
"60481",
"60481a",
"60483",
"60484",
"60592",
"60593",
"60594",
"60599",
"6060",
"60616a",
"60616b",
"60621",
"60623",
"6081",
"6091",
"61070",
"61071",
"6111",
"6019",
"61252",
"61409",
"4073",
"6141",
"11002",
"6157",
"61678",
"61678",
"6182",
"6215",
"6222",
"6231",
"6232",
"6233",
"62462",
"63864",
"63868",
"63869",
"64225",
"64391",
"64393",
"64681",
"64683",
"64712",
"6536",
"6541",
"6553",
"42924",
"6558",
"6587",
"6628",
"6628",
"6632",
"6636",
"72454",
"74261",
"84954",
"85861",
"85943",
"13731",
"85970",
"85970",
"85984",
"87079",
"87081",
"87083",
"87087",
"87580",
"87609",
"87620",
"88292",
"88646",
"61068",
"88930",
"90195",
"15646",
"90202",
"90609",
"90611",
"90630",
"52526",
"92092",
"92280",
"92579",
"92582",
"92583",
"92589",
"92907",
"92947",
"93273",
"93274",
"93606",
"94161",
"98100",
"98138",
"98262",
"98283",
"99008",
"99021",
"99206",
"99207",
"99773",
"99780",
"99781",
]


RENDER_DIR ="./renders/line-art"

os.makedirs(RENDER_DIR, exist_ok=True)

renderer = Renderer(ldraw_path="./ldraw")

for ldraw_id in ldraw_ids:
  filename = f"{RENDER_DIR}/{ldraw_id}.png"
  if os.path.exists(filename):
    print(f"------ Skipping {ldraw_id}, already exists")
    continue

  print(f"------ Rendering {ldraw_id}...")
  options = RenderOptions(
      image_filename = filename,
      format = Format.PNG,
      blender_filename = None,
      quality = Quality.DRAFT,
      lighting_style = LightingStyle.BRIGHT,
      part_color = RebrickableColors.White.value.best_hex,
      part_rotation=(0, 0, 0),
      zoom=0.8,
      look=Look.INSTRUCTIONS,
      width=150,
      height=150,
  )
  renderer.render_part(ldraw_id, options)
