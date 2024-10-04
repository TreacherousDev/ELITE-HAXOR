from litemapy import Region, BlockState
import ctypes
from ctypes import wintypes
import psutil
import tkinter as tk
from tkinter import ttk, filedialog
import os

# Create a default mapping that the user can update later
cc_to_mc_mapping = {
    0: "air",
    100: "dirt",
    101: "grass_block",
    103: "stone",
    104: "oak_sign",
    105: "mud",
    106: "iron_ore",
    109: "sand",
    111: "cobblestone",
    112: "coal_ore",
    113: "sweet_berry_bush",
    114: "coal_block",
    115: "copper_block",
    116: "azure_bluet",
    117: "red_mushroom",
    119: "light_gray_terracotta",
    120: "white_terracotta",
    121: "red_sandstone",
    122: "tuff",
    124: "jungle_planks",
    # 125: Hidden Gift
    126: "fire_coral_fan",
    127: "dead_brain_coral_fan",
    128: "tuff_bricks",
    129: "stone_bricks",
    130: "chiseled_tuff_bricks",
    131: "chiseled_stone_bricks",
    132: "scaffolding",
    133: "dripstone_block",
    # 134: Boy's Starter Gift
    135: "chiseled_red_sandstone",
    136: "bricks",
    137: "sand",
    138: "water",
    139: "slime_block",
    140: "glass",
    141: "pink_tulip",
    142: "poppy",
    143: "cornflower",
    144: "dandelion",
    145: "snow_block",
    146: "deepslate",
    147: "packed_ice",
    148: "stone_bricks",
    149: "stone_bricks",
    150: "stone_bricks",
    151: "stone_bricks",
    152: "stone_bricks",
    153: "stone_bricks",
    154: "stone_bricks",
    155: "stone_bricks",
    156: "stone_bricks",
    157: "stone_bricks",
    158: "quartz_block",
    159: "mangrove_planks",
    160: "acacia_planks",
    161: "bamboo_planks",
    162: "weathered_cut_copper",
    163: "prismarine_bricks",
    164: "purpur_block",
    165: "cherry_planks",
    166: "blackstone",
    167: "red_stained_glass",
    168: "orange_stained_glass",
    169: "yellow_stained_glass",
    170: "green_stained_glass",
    171: "blue_stained_glass",
    172: "purple_stained_glass",
    173: "pink_stained_glass",
    174: "black_stained_glass",
    175: "jukebox",
    176: "crafting_table",
    177: "chest",
    178: "furnace",
    179: "smoker",
    181: "cauldron",
    182: "stone_stairs",
    184: "stone_slab",
    185: "birch_fence",
    186: "stone_wall",
    # 187: Old Wood Chair
    188: "warped_stairs",
    189: "ladder",
    190: "sand",
    191: "mangrove_stairs",
    192: "stone_bricks",
    193: "stone_bricks",
    194: "stone_bricks",
    195: "stone_bricks",
    196: "stone_bricks",
    197: "stone_bricks",
    198: "stone_bricks",
    199: "stone_bricks",
    200: "stone_bricks",
    201: "stone_bricks",
    202: "spruce_stairs",
    203: "cut_copper_stairs",
    204: "brick_stairs",
    205: "stone_brick_stairs",
    206: "stone_brick_stairs",
    207: "stone_brick_stairs",
    208: "stone_brick_stairs",
    209: "stone_brick_stairs",
    210: "stone_brick_stairs",
    211: "stone_brick_stairs",
    212: "stone_brick_stairs",
    213: "stone_brick_stairs",
    214: "stone_brick_stairs",
    215: "smooth_red_sandstone_stairs",
    216: "red_sandstone_stairs",
    217: "birch_fence",
    218: "azalea_leaves",
    219: "mycelium",
    220: "ancient_debris",
    221: "spruce_fence",
    222: "spruce_leaves",
    223: "dead_brain_coral_block",
    224: "oak_fence",
    225: "oak_leaves",
    226: "crimson_fungus",
    227: "cactus",
    228: "lily_pad",
    229: "dark_oak_fence",
    230: "sculk",
    231: "soul_soil",
    # 232: Girl's Starter Gift
    233: "gold_ore",
    234: "spruce_leaves",
    235: "blue_ice",
    # 236: Slow Geyser
    # 237: Fast Geyser
    238: "sweet_berry_bush",
    239: "sweet_berry_bush",
    240: "lava",
    241: "sweet_berry_bush",
    242: "sweet_berry_bush",
    243: "sweet_berry_bush",
    244: "sweet_berry_bush",
    245: "sweet_berry_bush",
    246: "sweet_berry_bush",
    247: "sweet_berry_bush",
    248: "sweet_berry_bush",
    249: "cherry_fence",
    250: "cherry_leaves",
    251: "cherry_fence",
    252: "sandstone_slab",
    253: "birch_fence",
    254: "spruce_fence",
    255: "flower_pot",
    256: "flower_pot",
    257: "smooth_sandstone_slab",
    258: "smooth_sandstone_slab",
    259: "spruce_slab",
    260: "jungle_slab",
    261: "cut_copper_slab",
    262: "dark_prismarine_slab",
    263: "granite_slab",
    264: "smooth_stone_slab",
    265: "sandstone_slab",
    266: "diorite_slab",
    267: "dark_prismarine_slab",
    268: "quartz_slab",
    269: "mangrove_planks",
    270: "acacia_planks",
    271: "bamboo_planks",
    272: "weathered_cut_copper_slab",
    273: "prismarine_brick_slab",
    274: "purpur_slab",
    275: "cherry_slab",
    276: "blackstone_slab",
    277: "sandstone_wall",
    278: "granite_wall",
    279: "sandstone_slab",
    280: "jungle_stairs",
    281: "quartz_stairs",
    282: "mangrove_stairs",
    283: "acacia_stairs",
    284: "bamboo_stairs",
    285: "weathered_cut_copper_stairs",
    286: "prismarine_brick_stairs",
    287: "purpur_stairs",
    288: "cherry_stairs",
    289: "blackstone_stairs",

    720: "stone",
    723: "dirt",
    724: "grass_block",
    725: "jungle_planks",
    726: "spruce_planks",
    727: "blackstone",
    728: "spruce_wood",
    729: "cut_copper",
    730: "tuff",
    731: "sandstone",
    732: "white_concrete",
    733: "gray_concrete",
    734: "light_gray_concrete",
    735: "blue_concrete",
    736: "green_concrete",
    737: "brown_concrete",
    738: "purple_concrete",
    739: "light_blue_concrete",
    740: "lime_concrete",
    741: "white_terracotta",
    742: "red_concrete",
    743: "cyan_concrete",
    744: "yellow_concrete",
    745: "orange_concrete",
    746: "pink_concrete",
}
block_options = [
    "stone",
    "granite",
    "polished_granite",
    "diorite",
    "polished_diorite",
    "andesite",
    "polished_andesite",
    "deepslate",
    "cobbled_deepslate",
    "polished_deepslate",
    "calcite",
    "tuff",
    "dripstone_block",
    "grass_block",
    "dirt",
    "coarse_dirt",
    "podzol",
    "rooted_dirt",
    "mud",
    "crimson_nylium",
    "warped_nylium",
    "cobblestone",
    "oak_planks",
    "spruce_planks",
    "birch_planks",
    "jungle_planks",
    "acacia_planks",
    "dark_oak_planks",
    "mangrove_planks",
    "crimson_planks",
    "warped_planks",
    "oak_sapling",
    "spruce_sapling",
    "birch_sapling",
    "jungle_sapling",
    "acacia_sapling",
    "dark_oak_sapling",
    "mangrove_propagule",
    "sand",
    "red_sand",
    "gravel",
    "coal_ore",
    "deepslate_coal_ore",
    "iron_ore",
    "deepslate_iron_ore",
    "copper_ore",
    "deepslate_copper_ore",
    "gold_ore",
    "deepslate_gold_ore",
    "redstone_ore",
    "deepslate_redstone_ore",
    "emerald_ore",
    "deepslate_emerald_ore",
    "lapis_ore",
    "deepslate_lapis_ore",
    "diamond_ore",
    "deepslate_diamond_ore",
    "nether_gold_ore",
    "nether_quartz_ore",
    "ancient_debris",
    "coal_block",
    "raw_iron_block",
    "raw_copper_block",
    "raw_gold_block",
    "amethyst_block",
    "iron_block",
    "copper_block",
    "gold_block",
    "diamond_block",
    "netherite_block",
    "exposed_copper",
    "weathered_copper",
    "oxidized_copper",
    "cut_copper",
    "exposed_cut_copper",
    "weathered_cut_copper",
    "oxidized_cut_copper",
    "cut_copper_stairs",
    "exposed_cut_copper_stairs",
    "weathered_cut_copper_stairs",
    "oxidized_cut_copper_stairs",
    "cut_copper_slab",
    "exposed_cut_copper_slab",
    "weathered_cut_copper_slab",
    "oxidized_cut_copper_slab",
    "waxed_copper_block",
    "waxed_exposed_copper",
    "waxed_weathered_copper",
    "waxed_oxidized_copper",
    "waxed_cut_copper",
    "waxed_exposed_cut_copper",
    "waxed_weathered_cut_copper",
    "waxed_oxidized_cut_copper",
    "waxed_cut_copper_stairs",
    "waxed_exposed_cut_copper_stairs",
    "waxed_weathered_cut_copper_stairs",
    "waxed_oxidized_cut_copper_stairs",
    "waxed_cut_copper_slab",
    "waxed_exposed_cut_copper_slab",
    "waxed_weathered_cut_copper_slab",
    "waxed_oxidized_cut_copper_slab",
    "oak_log",
    "spruce_log",
    "birch_log",
    "jungle_log",
    "acacia_log",
    "dark_oak_log",
    "mangrove_log",
    "mangrove_roots",
    "muddy_mangrove_roots",
    "crimson_stem",
    "warped_stem",
    "stripped_oak_log",
    "stripped_spruce_log",
    "stripped_birch_log",
    "stripped_jungle_log",
    "stripped_acacia_log",
    "stripped_dark_oak_log",
    "stripped_mangrove_log",
    "stripped_crimson_stem",
    "stripped_warped_stem",
    "stripped_oak_wood",
    "stripped_spruce_wood",
    "stripped_birch_wood",
    "stripped_jungle_wood",
    "stripped_acacia_wood",
    "stripped_dark_oak_wood",
    "stripped_mangrove_wood",
    "stripped_crimson_hyphae",
    "stripped_warped_hyphae",
    "oak_wood",
    "spruce_wood",
    "birch_wood",
    "jungle_wood",
    "acacia_wood",
    "dark_oak_wood",
    "mangrove_wood",
    "crimson_hyphae",
    "warped_hyphae",
    "oak_leaves",
    "spruce_leaves",
    "birch_leaves",
    "jungle_leaves",
    "acacia_leaves",
    "dark_oak_leaves",
    "mangrove_leaves",
    "azalea_leaves",
    "flowering_azalea_leaves",
    "sponge",
    "wet_sponge",
    "glass",
    "tinted_glass",
    "lapis_block",
    "sandstone",
    "chiseled_sandstone",
    "cut_sandstone",
    "cobweb",
    "grass",
    "fern",
    "azalea",
    "flowering_azalea",
    "dead_bush",
    "seagrass",
    "sea_pickle",
    "white_wool",
    "orange_wool",
    "magenta_wool",
    "light_blue_wool",
    "yellow_wool",
    "lime_wool",
    "pink_wool",
    "gray_wool",
    "light_gray_wool",
    "cyan_wool",
    "purple_wool",
    "blue_wool",
    "brown_wool",
    "green_wool",
    "red_wool",
    "black_wool",
    "dandelion",
    "poppy",
    "blue_orchid",
    "allium",
    "azure_bluet",
    "red_tulip",
    "orange_tulip",
    "white_tulip",
    "pink_tulip",
    "oxeye_daisy",
    "cornflower",
    "lily_of_the_valley",
    "wither_rose",
    "spore_blossom",
    "brown_mushroom",
    "red_mushroom",
    "crimson_fungus",
    "warped_fungus",
    "crimson_roots",
    "warped_roots",
    "nether_sprouts",
    "weeping_vines",
    "twisting_vines",
    "sugar_cane",
    "kelp",
    "moss_carpet",
    "moss_block",
    "hanging_roots",
    "big_dripleaf",
    "small_dripleaf",
    "bamboo",
    "oak_slab",
    "spruce_slab",
    "birch_slab",
    "jungle_slab",
    "acacia_slab",
    "dark_oak_slab",
    "mangrove_slab",
    "crimson_slab",
    "warped_slab",
    "stone_slab",
    "smooth_stone_slab",
    "sandstone_slab",
    "cut_sandstone_slab",
    "cobblestone_slab",
    "brick_slab",
    "stone_brick_slab",
    "mud_brick_slab",
    "nether_brick_slab",
    "quartz_slab",
    "red_sandstone_slab",
    "cut_red_sandstone_slab",
    "purpur_slab",
    "prismarine_slab",
    "prismarine_brick_slab",
    "dark_prismarine_slab",
    "smooth_quartz",
    "smooth_red_sandstone",
    "smooth_sandstone",
    "smooth_stone",
    "bricks",
    "bookshelf",
    "mossy_cobblestone",
    "obsidian",
    "torch",
    "end_rod",
    "chorus_flower",
    "purpur_block",
    "purpur_pillar",
    "purpur_stairs",
    "chest",
    "crafting_table",
    "furnace",
    "ladder",
    "cobblestone_stairs",
    "snow",
    "ice",
    "snow_block",
    "cactus",
    "clay",
    "jukebox",
    "oak_fence",
    "spruce_fence",
    "birch_fence",
    "jungle_fence",
    "acacia_fence",
    "dark_oak_fence",
    "mangrove_fence",
    "crimson_fence",
    "warped_fence",
    "pumpkin",
    "carved_pumpkin",
    "jack_o_lantern",
    "netherrack",
    "soul_sand",
    "soul_soil",
    "basalt",
    "polished_basalt",
    "smooth_basalt",
    "soul_torch",
    "glowstone",
    "stone_bricks",
    "mossy_stone_bricks",
    "cracked_stone_bricks",
    "chiseled_stone_bricks",
    "packed_mud",
    "mud_bricks",
    "deepslate_bricks",
    "cracked_deepslate_bricks",
    "deepslate_tiles",
    "cracked_deepslate_tiles",
    "chiseled_deepslate",
    "brown_mushroom_block",
    "red_mushroom_block",
    "mushroom_stem",
    "iron_bars",
    "chain",
    "glass_pane",
    "melon",
    "vine",
    "glow_lichen",
    "brick_stairs",
    "stone_brick_stairs",
    "mud_brick_stairs",
    "mycelium",
    "lily_pad",
    "nether_bricks",
    "cracked_nether_bricks",
    "chiseled_nether_bricks",
    "nether_brick_fence",
    "nether_brick_stairs",
    "sculk",
    "sculk_vein",
    "sculk_catalyst",
    "sculk_shrieker",
    "enchanting_table",
    "end_stone",
    "end_stone_bricks",
    "dragon_egg",
    "sandstone_stairs",
    "ender_chest",
    "emerald_block",
    "oak_stairs",
    "spruce_stairs",
    "birch_stairs",
    "jungle_stairs",
    "acacia_stairs",
    "dark_oak_stairs",
    "mangrove_stairs",
    "crimson_stairs",
    "warped_stairs",
    "beacon",
    "cobblestone_wall",
    "mossy_cobblestone_wall",
    "brick_wall",
    "prismarine_wall",
    "red_sandstone_wall",
    "mossy_stone_brick_wall",
    "granite_wall",
    "stone_brick_wall",
    "mud_brick_wall",
    "nether_brick_wall",
    "andesite_wall",
    "red_nether_brick_wall",
    "sandstone_wall",
    "end_stone_brick_wall",
    "diorite_wall",
    "blackstone_wall",
    "polished_blackstone_wall",
    "polished_blackstone_brick_wall",
    "cobbled_deepslate_wall",
    "polished_deepslate_wall",
    "deepslate_brick_wall",
    "deepslate_tile_wall",
    "anvil",
    "chipped_anvil",
    "damaged_anvil",
    "chiseled_quartz_block",
    "quartz_block",
    "quartz_bricks",
    "quartz_pillar",
    "quartz_stairs",
    "white_terracotta",
    "orange_terracotta",
    "magenta_terracotta",
    "light_blue_terracotta",
    "yellow_terracotta",
    "lime_terracotta",
    "pink_terracotta",
    "gray_terracotta",
    "light_gray_terracotta",
    "cyan_terracotta",
    "purple_terracotta",
    "blue_terracotta",
    "brown_terracotta",
    "green_terracotta",
    "red_terracotta",
    "black_terracotta",
    "hay_block",
    "white_carpet",
    "orange_carpet",
    "magenta_carpet",
    "light_blue_carpet",
    "yellow_carpet",
    "lime_carpet",
    "pink_carpet",
    "gray_carpet",
    "light_gray_carpet",
    "cyan_carpet",
    "purple_carpet",
    "blue_carpet",
    "brown_carpet",
    "green_carpet",
    "red_carpet",
    "black_carpet",
    "terracotta",
    "packed_ice",
    "sunflower",
    "lilac",
    "rose_bush",
    "peony",
    "tall_grass",
    "large_fern",
    "white_stained_glass",
    "orange_stained_glass",
    "magenta_stained_glass",
    "light_blue_stained_glass",
    "yellow_stained_glass",
    "lime_stained_glass",
    "pink_stained_glass",
    "gray_stained_glass",
    "light_gray_stained_glass",
    "cyan_stained_glass",
    "purple_stained_glass",
    "blue_stained_glass",
    "brown_stained_glass",
    "green_stained_glass",
    "red_stained_glass",
    "black_stained_glass",
    "white_stained_glass_pane",
    "orange_stained_glass_pane",
    "magenta_stained_glass_pane",
    "light_blue_stained_glass_pane",
    "yellow_stained_glass_pane",
    "lime_stained_glass_pane",
    "pink_stained_glass_pane",
    "gray_stained_glass_pane",
    "light_gray_stained_glass_pane",
    "cyan_stained_glass_pane",
    "purple_stained_glass_pane",
    "blue_stained_glass_pane",
    "brown_stained_glass_pane",
    "green_stained_glass_pane",
    "red_stained_glass_pane",
    "black_stained_glass_pane",
    "prismarine",
    "prismarine_bricks",
    "dark_prismarine",
    "prismarine_stairs",
    "prismarine_brick_stairs",
    "dark_prismarine_stairs",
    "sea_lantern",
    "red_sandstone",
    "chiseled_red_sandstone",
    "cut_red_sandstone",
    "red_sandstone_stairs",
    "magma_block",
    "nether_wart_block",
    "warped_wart_block",
    "red_nether_bricks",
    "bone_block",
    "shulker_box",
    "white_shulker_box",
    "orange_shulker_box",
    "magenta_shulker_box",
    "light_blue_shulker_box",
    "yellow_shulker_box",
    "lime_shulker_box",
    "pink_shulker_box",
    "gray_shulker_box",
    "light_gray_shulker_box",
    "cyan_shulker_box",
    "purple_shulker_box",
    "blue_shulker_box",
    "brown_shulker_box",
    "green_shulker_box",
    "red_shulker_box",
    "black_shulker_box",
    "white_glazed_terracotta",
    "orange_glazed_terracotta",
    "magenta_glazed_terracotta",
    "light_blue_glazed_terracotta",
    "yellow_glazed_terracotta",
    "lime_glazed_terracotta",
    "pink_glazed_terracotta",
    "gray_glazed_terracotta",
    "light_gray_glazed_terracotta",
    "cyan_glazed_terracotta",
    "purple_glazed_terracotta",
    "blue_glazed_terracotta",
    "brown_glazed_terracotta",
    "green_glazed_terracotta",
    "red_glazed_terracotta",
    "black_glazed_terracotta",
    "white_concrete",
    "orange_concrete",
    "magenta_concrete",
    "light_blue_concrete",
    "yellow_concrete",
    "lime_concrete",
    "pink_concrete",
    "gray_concrete",
    "light_gray_concrete",
    "cyan_concrete",
    "purple_concrete",
    "blue_concrete",
    "brown_concrete",
    "green_concrete",
    "red_concrete",
    "black_concrete",
    "white_concrete_powder",
    "orange_concrete_powder",
    "magenta_concrete_powder",
    "light_blue_concrete_powder",
    "yellow_concrete_powder",
    "lime_concrete_powder",
    "pink_concrete_powder",
    "gray_concrete_powder",
    "light_gray_concrete_powder",
    "cyan_concrete_powder",
    "purple_concrete_powder",
    "blue_concrete_powder",
    "brown_concrete_powder",
    "green_concrete_powder",
    "red_concrete_powder",
    "black_concrete_powder",
    "turtle_egg",
    "dead_tube_coral_block",
    "dead_brain_coral_block",
    "dead_bubble_coral_block",
    "dead_fire_coral_block",
    "dead_horn_coral_block",
    "tube_coral_block",
    "brain_coral_block",
    "bubble_coral_block",
    "fire_coral_block",
    "horn_coral_block",
    "tube_coral",
    "brain_coral",
    "bubble_coral",
    "fire_coral",
    "horn_coral",
    "dead_brain_coral",
    "dead_bubble_coral",
    "dead_fire_coral",
    "dead_horn_coral",
    "dead_tube_coral",
    "tube_coral_fan",
    "brain_coral_fan",
    "bubble_coral_fan",
    "fire_coral_fan",
    "horn_coral_fan",
    "dead_tube_coral_fan",
    "dead_brain_coral_fan",
    "dead_bubble_coral_fan",
    "dead_fire_coral_fan",
    "dead_horn_coral_fan",
    "blue_ice",
    "conduit",
    "polished_granite_stairs",
    "smooth_red_sandstone_stairs",
    "mossy_stone_brick_stairs",
    "polished_diorite_stairs",
    "mossy_cobblestone_stairs",
    "end_stone_brick_stairs",
    "stone_stairs",
    "smooth_sandstone_stairs",
    "smooth_quartz_stairs",
    "granite_stairs",
    "andesite_stairs",
    "red_nether_brick_stairs",
    "polished_andesite_stairs",
    "diorite_stairs",
    "cobbled_deepslate_stairs",
    "polished_deepslate_stairs",
    "deepslate_brick_stairs",
    "deepslate_tile_stairs",
    "polished_granite_slab",
    "smooth_red_sandstone_slab",
    "mossy_stone_brick_slab",
    "polished_diorite_slab",
    "mossy_cobblestone_slab",
    "end_stone_brick_slab",
    "smooth_sandstone_slab",
    "smooth_quartz_slab",
    "granite_slab",
    "andesite_slab",
    "red_nether_brick_slab",
    "polished_andesite_slab",
    "diorite_slab",
    "cobbled_deepslate_slab",
    "polished_deepslate_slab",
    "deepslate_brick_slab",
    "deepslate_tile_slab",
    "scaffolding",
    "redstone",
    "redstone_torch",
    "redstone_block",
    "repeater",
    "comparator",
    "piston",
    "sticky_piston",
    "slime_block",
    "honey_block",
    "observer",
    "hopper",
    "dispenser",
    "dropper",
    "lectern",
    "target",
    "lever",
    "lightning_rod",
    "daylight_detector",
    "sculk_sensor",
    "tripwire_hook",
    "trapped_chest",
    "tnt",
    "redstone_lamp",
    "note_block",
    "stone_button",
    "polished_blackstone_button",
    "oak_button",
    "spruce_button",
    "birch_button",
    "jungle_button",
    "acacia_button",
    "dark_oak_button",
    "mangrove_button",
    "crimson_button",
    "warped_button",
    "stone_pressure_plate",
    "polished_blackstone_pressure_plate",
    "light_weighted_pressure_plate",
    "heavy_weighted_pressure_plate",
    "oak_pressure_plate",
    "spruce_pressure_plate",
    "birch_pressure_plate",
    "jungle_pressure_plate",
    "acacia_pressure_plate",
    "dark_oak_pressure_plate",
    "mangrove_pressure_plate",
    "crimson_pressure_plate",
    "warped_pressure_plate",
    "iron_door",
    "oak_door",
    "spruce_door",
    "birch_door",
    "jungle_door",
    "acacia_door",
    "dark_oak_door",
    "mangrove_door",
    "crimson_door",
    "warped_door",
    "iron_trapdoor",
    "oak_trapdoor",
    "spruce_trapdoor",
    "birch_trapdoor",
    "jungle_trapdoor",
    "acacia_trapdoor",
    "dark_oak_trapdoor",
    "mangrove_trapdoor",
    "crimson_trapdoor",
    "warped_trapdoor",
    "oak_fence_gate",
    "spruce_fence_gate",
    "birch_fence_gate",
    "jungle_fence_gate",
    "acacia_fence_gate",
    "dark_oak_fence_gate",
    "mangrove_fence_gate",
    "crimson_fence_gate",
    "warped_fence_gate",
    "powered_rail",
    "detector_rail",
    "rail",
    "activator_rail",
    "saddle",
    "minecart",
    "chest_minecart",
    "furnace_minecart",
    "tnt_minecart",
    "hopper_minecart",
    "carrot_on_a_stick",
    "warped_fungus_on_a_stick",
    "elytra",
    "oak_boat",
    "oak_chest_boat",
    "spruce_boat",
    "spruce_chest_boat",
    "birch_boat",
    "birch_chest_boat",
    "jungle_boat",
    "jungle_chest_boat",
    "acacia_boat",
    "acacia_chest_boat",
    "dark_oak_boat",
    "dark_oak_chest_boat",
    "mangrove_boat",
    "mangrove_chest_boat",
    "turtle_helmet",
    "scute",
    "flint_and_steel",
    "apple",
    "bow",
    "arrow",
    "coal",
    "charcoal",
    "diamond",
    "emerald",
    "lapis_lazuli",
    "quartz",
    "amethyst_shard",
    "raw_iron",
    "iron_ingot",
    "raw_copper",
    "copper_ingot",
    "raw_gold",
    "gold_ingot",
    "netherite_ingot",
    "netherite_scrap",
    "wooden_sword",
    "wooden_shovel",
    "wooden_pickaxe",
    "wooden_axe",
    "wooden_hoe",
    "stone_sword",
    "stone_shovel",
    "stone_pickaxe",
    "stone_axe",
    "stone_hoe",
    "golden_sword",
    "golden_shovel",
    "golden_pickaxe",
    "golden_axe",
    "golden_hoe",
    "iron_sword",
    "iron_shovel",
    "iron_pickaxe",
    "iron_axe",
    "iron_hoe",
    "diamond_sword",
    "diamond_shovel",
    "diamond_pickaxe",
    "diamond_axe",
    "diamond_hoe",
    "netherite_sword",
    "netherite_shovel",
    "netherite_pickaxe",
    "netherite_axe",
    "netherite_hoe",
    "stick",
    "bowl",
    "mushroom_stew",
    "string",
    "feather",
    "gunpowder",
    "wheat_seeds",
    "wheat",
    "bread",
    "leather_helmet",
    "leather_chestplate",
    "leather_leggings",
    "leather_boots",
    "chainmail_helmet",
    "chainmail_chestplate",
    "chainmail_leggings",
    "chainmail_boots",
    "iron_helmet",
    "iron_chestplate",
    "iron_leggings",
    "iron_boots",
    "diamond_helmet",
    "diamond_chestplate",
    "diamond_leggings",
    "diamond_boots",
    "golden_helmet",
    "golden_chestplate",
    "golden_leggings",
    "golden_boots",
    "netherite_helmet",
    "netherite_chestplate",
    "netherite_leggings",
    "netherite_boots",
    "flint",
    "porkchop",
    "cooked_porkchop",
    "painting",
    "golden_apple",
    "enchanted_golden_apple",
    "oak_sign",
    "spruce_sign",
    "birch_sign",
    "jungle_sign",
    "acacia_sign",
    "dark_oak_sign",
    "mangrove_sign",
    "crimson_sign",
    "warped_sign",
    "bucket",
    "water_bucket",
    "lava_bucket",
    "powder_snow_bucket",
    "snowball",
    "leather",
    "milk_bucket",
    "pufferfish_bucket",
    "salmon_bucket",
    "cod_bucket",
    "tropical_fish_bucket",
    "axolotl_bucket",
    "tadpole_bucket",
    "brick",
    "clay_ball",
    "dried_kelp_block",
    "paper",
    "book",
    "slime_ball",
    "egg",
    "compass",
    "recovery_compass",
    "fishing_rod",
    "clock",
    "spyglass",
    "glowstone_dust",
    "cod",
    "salmon",
    "tropical_fish",
    "pufferfish",
    "cooked_cod",
    "cooked_salmon",
    "ink_sac",
    "glow_ink_sac",
    "cocoa_beans",
    "white_dye",
    "orange_dye",
    "magenta_dye",
    "light_blue_dye",
    "yellow_dye",
    "lime_dye",
    "pink_dye",
    "gray_dye",
    "light_gray_dye",
    "cyan_dye",
    "purple_dye",
    "blue_dye",
    "brown_dye",
    "green_dye",
    "red_dye",
    "black_dye",
    "bone_meal",
    "bone",
    "sugar",
    "cake",
    "white_bed",
    "orange_bed",
    "magenta_bed",
    "light_blue_bed",
    "yellow_bed",
    "lime_bed",
    "pink_bed",
    "gray_bed",
    "light_gray_bed",
    "cyan_bed",
    "purple_bed",
    "blue_bed",
    "brown_bed",
    "green_bed",
    "red_bed",
    "black_bed",
    "cookie",
    "filled_map",
    "shears",
    "melon_slice",
    "dried_kelp",
    "pumpkin_seeds",
    "melon_seeds",
    "beef",
    "cooked_beef",
    "chicken",
    "cooked_chicken",
    "rotten_flesh",
    "ender_pearl",
    "blaze_rod",
    "ghast_tear",
    "gold_nugget",
    "nether_wart",
    "potion",
    "glass_bottle",
    "spider_eye",
    "fermented_spider_eye",
    "blaze_powder",
    "magma_cream",
    "brewing_stand",
    "cauldron",
    "ender_eye",
    "glistering_melon_slice",
    "experience_bottle",
    "fire_charge",
    "writable_book",
    "written_book",
    "item_frame",
    "glow_item_frame",
    "flower_pot",
    "carrot",
    "potato",
    "baked_potato",
    "poisonous_potato",
    "map",
    "golden_carrot",
    "skeleton_skull",
    "wither_skeleton_skull",
    "zombie_head",
    "creeper_head",
    "dragon_head",
    "nether_star",
    "pumpkin_pie",
    "firework_rocket",
    "firework_star",
    "enchanted_book",
    "nether_brick",
    "prismarine_shard",
    "prismarine_crystals",
    "rabbit",
    "cooked_rabbit",
    "rabbit_stew",
    "rabbit_foot",
    "rabbit_hide",
    "armor_stand",
    "iron_horse_armor",
    "golden_horse_armor",
    "diamond_horse_armor",
    "leather_horse_armor",
    "lead",
    "name_tag",
    "mutton",
    "cooked_mutton",
    "white_banner",
    "orange_banner",
    "magenta_banner",
    "light_blue_banner",
    "yellow_banner",
    "lime_banner",
    "pink_banner",
    "gray_banner",
    "light_gray_banner",
    "cyan_banner",
    "purple_banner",
    "blue_banner",
    "brown_banner",
    "green_banner",
    "red_banner",
    "black_banner",
    "end_crystal",
    "chorus_fruit",
    "popped_chorus_fruit",
    "beetroot",
    "beetroot_seeds",
    "beetroot_soup",
    "dragon_breath",
    "splash_potion",
    "spectral_arrow",
    "tipped_arrow",
    "lingering_potion",
    "shield",
    "totem_of_undying",
    "shulker_shell",
    "iron_nugget",
    "music_disc_13",
    "music_disc_cat",
    "music_disc_blocks",
    "music_disc_chirp",
    "music_disc_far",
    "music_disc_mall",
    "music_disc_mellohi",
    "music_disc_stal",
    "music_disc_strad",
    "music_disc_ward",
    "music_disc_11",
    "music_disc_wait",
    "music_disc_otherside",
    "music_disc_5",
    "music_disc_pigstep",
    "disc_fragment_5",
    "trident",
    "phantom_membrane",
    "nautilus_shell",
    "heart_of_the_sea",
    "crossbow",
    "suspicious_stew",
    "loom",
    "flower_banner_pattern",
    "creeper_banner_pattern",
    "skull_banner_pattern",
    "mojang_banner_pattern",
    "globe_banner_pattern",
    "piglin_banner_pattern",
    "goat_horn",
    "composter",
    "barrel",
    "smoker",
    "blast_furnace",
    "cartography_table",
    "fletching_table",
    "grindstone",
    "smithing_table",
    "stonecutter",
    "bell",
    "lantern",
    "soul_lantern",
    "sweet_berries",
    "glow_berries",
    "campfire",
    "soul_campfire",
    "shroomlight",
    "honeycomb",
    "bee_nest",
    "beehive",
    "honey_bottle",
    "honeycomb_block",
    "lodestone",
    "crying_obsidian",
    "blackstone",
    "blackstone_slab",
    "blackstone_stairs",
    "gilded_blackstone",
    "polished_blackstone",
    "polished_blackstone_slab",
    "polished_blackstone_stairs",
    "chiseled_polished_blackstone",
    "polished_blackstone_bricks",
    "polished_blackstone_brick_slab",
    "polished_blackstone_brick_stairs",
    "cracked_polished_blackstone_bricks",
    "respawn_anchor",
    "candle",
    "white_candle",
    "orange_candle",
    "magenta_candle",
    "light_blue_candle",
    "yellow_candle",
    "lime_candle",
    "pink_candle",
    "gray_candle",
    "light_gray_candle",
    "cyan_candle",
    "purple_candle",
    "blue_candle",
    "brown_candle",
    "green_candle",
    "red_candle",
    "black_candle",
    "small_amethyst_bud",
    "medium_amethyst_bud",
    "large_amethyst_bud",
    "amethyst_cluster",
    "pointed_dripstone",
    "ochre_froglight",
    "verdant_froglight",
    "pearlescent_froglight",
    "echo_shard",
    "bedrock",
    "budding_amethyst",
    "petrified_oak_slab",
    "chorus_plant",
    "spawner",
    "farmland",
    "infested_stone",
    "infested_cobblestone",
    "infested_stone_bricks",
    "infested_mossy_stone_bricks",
    "infested_cracked_stone_bricks",
    "infested_chiseled_stone_bricks",
    "infested_deepslate",
    "reinforced_deepslate",
    "end_portal_frame",
    "command_block",
    "barrier",
    "light",
    "dirt_path",
    "repeating_command_block",
    "chain_command_block",
    "structure_void",
    "structure_block",
    "jigsaw"
]
block_options = sorted(block_options)

def storagelmao():
    pass
    # 290. Gold Block
    # 291. Gold Plate
    # 292. Golden Stairs
    # 293. Old Cabinet
    # 294. Sink
    # 295. Persian Rug
    # 296. Fridge
    # 297. Stove
    # 298. Raw Silver
    # 299. Silver Block
    # 300. Silver Plate
    # 301. Silver Stairs
    # 302. Tropical Grass
    # 303. Soil
    # 304. Fancy Road
    # 305. Nuke
    # 306. Cloud
    # 307. Finial Stone
    # 308. Finial Sandstone
    # 309. Horizontal AcceloRing
    # 310. Vertical AcceloRing
    # 311. Trash Can
    # 312. Mecho-Spikes Blue
    # 313. Mecho-Spikes Yellow
    # 314. The Almighty Cube
    # 315. Warning Sign
    # 316. Stop Sign
    # 317. Left Sign
    # 318. Right Sign
    # 319. Up Sign
    # 320. Down Sign
    # 321. Steel Block
    # 322. Steel Plate
    # 323. Steel Stairs
    # 324. Stainless Steel Block
    # 325. Stainless Steel Plate
    # 326. Stainless Steel Stairs
    # 327. Steel Gear
    # 328. Stone Cross
    # 329. Mattress
    # 330. Double Mattress
    # 331. New Wood Table
    # 332. New Wood Chair
    # 333. Fancy Table
    # 334. Bomb
    # 335. C Note
    # 336. C# Note
    # 337. D Note
    # 338. D# Note
    # 339. E Note
    # 340. F Note
    # 341. F# Note
    # 342. G Note
    # 343. G# Note
    # 344. A Note
    # 345. A# Note
    # 346. B Note
    # 347. Cannon
    # 348. Rope Ladder
    # 349. Candle
    # 350. Checkpoint
    # 351. Healing Block
    # 352. Fast Cannon
    # 353. Distiller
    # 354. Extractor
    # 355. Steel Cauldron
    # 356. Fancy Chair
    # 357. Throne
    # 358. New Cabinet
    # 359. Fancy Cabinet
    # 360. Prison Bars
    # 361. Computer
    # 362. Torch
    # 363. Warp Anchor
    # 364. Street Light
    # 365. Iron Pole
    # 366. Purple Paper Lantern
    # 367. Red Paper Lantern
    # 368. Blue Paper Lantern
    # 369. Green Paper Lantern
    # 370. Farm Hive
    # 371. Fairy Mushroom
    # 372. Bones
    # 373. Fern
    # 374. Fairy Fern
    # 375. Cobblestone
    # 376. Cash Register
    # 377. Cave Art VI
    # 378. Cave Art X
    # 379. Cave Art VIII
    # 380. Cave Art IV
    # 381. Cave Art V
    # 382. Cave Art I
    # 383. Cave Art VII
    # 384. Cave Art III
    # 385. Cave Art IX
    # 386. Cave Art II
    # 387. Cave Art XII
    # 388. Cave Art XI
    # 389. Rating Block
    # 390. Wild Hive
    # 391. Mosaic Floor
    # 392. Bubbling Cauldron
    # 393. Jack O' Lantern I
    # 394. Jack O' Lantern II
    # 395. Jack O' Lantern III
    # 396. Headstone I
    # 397. Headstone II
    # 398. Terracotta Tiles
    # 399. White Lattice
    # 400. Wood Lattice
    # 401. Scaffold
    # 402. QBee Bomb
    # 403. Pulse Bomb
    # 404. Pulse Block
    # 405. Fossil II
    # 406. Fossil XII
    # 407. Fossil VII
    # 408. Fossil V
    # 409. Fossil III
    # 410. Fossil I
    # 411. Fossil XI
    # 412. Fossil IX
    # 413. Fossil VIII
    # 414. Fossil IV
    # 415. Fossil VI
    # 416. Fossil X
    # 417. Silver Christmas Tree
    # 418. Gold Christmas Tree
    # 419. Yule Log
    # 420. Candy Cane
    # 421. Star
    # 422. Wreath
    # 423. Red Present
    # 424. Blue Present
    # 425. Pink Present
    # 426. Purple Present
    # 427. Stocking
    # 428. Chocolate Chip Cookies
    # 429. Christmas Cookies
    # 430. Cocoa
    # 431. Roast Beast
    # 432. Clan Stone
    # 433. Clan Stone Level 2
    # 434. Clan Stone Level 3
    # 435. Clan Stone Level 4
    # 436. Clan Stone Level 5
    # 437. Donation Table
    # 438. Mannequin
    # 439. Dice Bumper - Number 1
    # 440. Dice Bumper - Number 2
    # 441. Dice Bumper - Number 3
    # 442. Dice Bumper - Number 4
    # 443. Dice Bumper - Number 5
    # 444. Dice Bumper - Number 6
    # 445. Trick Dice - Number 1
    # 446. Trick Dice - Number 2
    # 447. Dice Bumper
    # 448. Hidey Bumper
    # 449. Heal Bumper
    # 450. Checkpoint Bumper
    # 451. Basic Bumper
    # 452. Special Notice Block
    # 453. Green Goop
    # 454. Snot
    # 455. Crate
    # 456. Barrel
    # 457. Bone Throne
    # 458. Stalagmite
    # 459. Stalagmite Bunch
    # 460. Skull Pile
    # 461. Qbee Skull
    # 462. Slyme Egg
    # 463. Purple Crystal
    # 464. Monster Grave
    # 465. Glow Shroom
    # 466. Cave Wall
    # 467. Jagged Rocks
    # 468. Gargoyle
    # 469. Bookshelf
    # 470. Iron Fire Trap
    # 471. Steel Fire Trap
    # 472. Gate Bumper
    # 473. Shackles
    # 474. Iron Fire Wall
    # 475. Steel Fire Wall
    # 476. Cave Lava Cracks
    # 477. Stone Lava Cracks
    # 478. Mega Stalagmite
    # 479. Dog Kennel
    # 480. Recube Bin
    # 481. Scrub
    # 482. Giant Pansy
    # 483. Giant Corn Flower
    # 484. Giant Aster
    # 485. Giant Violet
    # 486. Giant Pansy
    # 487. Giant Cornflower Clump
    # 488. Giant Aster Clump
    # 489. Giant Violet Clump
    # 490. Giant Daisy
    # 491. Giant Daisy Clump
    # 492. Polka Tree Trunk
    # 493. Polka Tree Base
    # 494. Meemew House
    # 495. Hopper House
    # 496. Ramm House
    # 497. Dragon Lair
    # 498. White Stripe Road
    # 499. White Divider Road 1
    # 500. White Divider Road 2
    # 501. White Curve Road 1
    # 502. White Curve Road 2
    # 503. White Curve Road 3
    # 504. White Curve Road 4
    # 505. Yellow Stripe Road
    # 506. Yellow Divider Road 1
    # 507. Yellow Divider Road 2
    # 508. Yellow Curve Road 1
    # 509. Yellow Curve Road 2
    # 510. Yellow Curve Road 3
    # 511. Yellow Curve Road 4
    # 512. Mute Bumper
    # 513. NPC
    # 514. Mailbox
    # 515. Trigger
    # 516. Warp Crunch Bumper
    # 517. Search Bumper
    # 518. Shrink Bumper
    # 519. Power Stone
    # 520. Telepizza Bumper
    # 521. Crude Signpost
    # 522. Teletaco Bumper
    # 523. Beam Burger Bumper
    # 524. Wind Machine
    # 525. Black Meemew House
    # 526. Awful Cobwebs
    # 527. Haunted Chest
    # 528. Candelabra
    # 529. Leaf Pile
    # 530. Autumn Leaves
    # 531. Pumpkin House
    # 532. Invisible Sign
    # 533. Omni Wind Machine
    # 534. Slyme Splat
    # 535. Walk-In Trigger
    # 536. Slyme Inna Box
    # 537. Spudbug Inna Box
    # 538. Red Official Sign
    # 539. Green Official Sign
    # 540. Black Official Sign
    # 541. House Lamp
    # 542. Office Lamp
    # 543. Drop Scaffold
    # 544. Cracked Ice
    # 545. Cracked Stone
    # 546. Dropper Block
    # 547. Frostberry Pie
    # 548. Plate
    # 549. Cutlery
    # 550. Yumberry Juice
    # 551. Sunberry Juice
    # 552. Yumberry Pitcher
    # 553. Sunberry Pitcher
    # 554. Yumberry Cake
    # 555. Baleful Box
    # 556. Chiliberry Cake
    # 557. Cheese Plate
    # 558. Mashed Potatoes
    # 559. Salad
    # 560. Silver Chest
    # 561. Gold Chest
    # 562. Pharoah Chest
    # 563. Quantum Chest
    # 564. Bi-Spectrum Variable Modulator
    # 565. Convex Coil Resonating Turbine
    # 566. Quasi-Magnetic Parallax Quantum Receiver
    # 567. Book
    # 568. Footprint
    # 569. Super Pow Xmas Gift
    # 570. Santa Sack
    # 571. Reindeer Kennel
    # 572. North Pole Sign
    # 573. Snowman Kennel
    # 574. Poinsettia
    # 575. Santa's Workbench
    # 576. Elf Hut
    # 577. Firecracker
    # 578. Bottle Rocket
    # 579. Black Marble
    # 580. Spook-Inna-Box
    # 581. Metal Ladder
    # 582. System Block
    # 583. Open Sign
    # 584. Closed Sign
    # 585. White Marble
    # 586. Blue Marble
    # 587. Black Marble Half Block
    # 588. White Marble Half Block
    # 589. Blue Marble Half Block
    # 590. Bonus Star Block
    # 591. Black Marble Stairs
    # 592. White Marble Stairs
    # 593. Blue Marble Stairs
    # 594. Black Marble Column
    # 595. White Marble Column
    # 596. Blue Marble Column
    # 597. Dark Brick
    # 598. Blue Brick
    # 599. Gold Brick
    # 600. Half Snow Block
    # 601. Half Topic Grass
    # 602. Half Mountain Block
    # 603. Old Wood Column
    # 604. New Wood Column
    # 605. Stone Fence
    # 606. Dry Cement
    # 607. Wet Cement
    # 608. Dry Paste
    # 609. Wet Paste
    # 610. Old Wood Shelves
    # 611. New Wood Shelves
    # 612. Mosaic Half Block
    # 613. Mosaic Stairs
    # 614. Persian Rug Half Block
    # 615. Persian Rug Stairs
    # 616. Terracotta Half Block
    # 617. Terracotta Stairs
    # 618. Trilobyte I
    # 619. Trilobyte II
    # 620. Trilobyte III
    # 621. Trilobyte IV
    # 622. Trilobyte V
    # 623. Trilobyte VI
    # 624. Trilobyte VII
    # 625. Trilobyte VIII
    # 626. Trilobyte IX
    # 627. Trilobyte XI
    # 628. Trilobyte X
    # 629. Trilobyte XII
    # 630. Dark Raw Stone
    # 631. System Sand
    # 632. Glyph I
    # 633. Glyph II
    # 634. Glyph III
    # 635. Glyph IV
    # 636. Glyph V
    # 637. Glyph VI
    # 638. Glyph VII
    # 639. Glyph VIII
    # 640. Glyph IX
    # 641. Glyph XI
    # 642. Glyph X
    # 643. Glyph XII
    # 644. Book of Bic
    # 645. Book of Cas
    # 646. Book of Tles
    # 647. Wuvva Pig Kennel
    # 648. Wuvva Wallpaper
    # 649. Wuvva Wallpaper
    # 650. Wuvva Wallpaper
    # 651. Diamond
    # 652. Ruby
    # 653. Emerald
    # 654. Half Diamond
    # 655. Half Ruby
    # 656. Half Emerald
    # 657. Diamond Stairs
    # 658. Ruby Stairs
    # 659. Emerald Stairs
    # 660. Park Bench
    # 661. Lit Checkpoint
    # 662. Finish Line
    # 663. Start Timer
    # 664. Water Current
    # 665. Chick Coop
    # 666. Blooming Cherry Leaves
    # 667. Cherry Blossom Pile
    # 668. Bedrock
    # 669. Pink Pastel Stripes
    # 670. Purple Pastel Stripes
    # 671. Blue Pastel Stripes
    # 672. Green Pastel Stripes
    # 673. Yellow Pastel Stripes
    # 674. Red Rainbow
    # 675. Orange Rainbow
    # 676. Yellow Rainbow
    # 677. Green Rainbow
    # 678. Blue Rainbow
    # 679. Purple Rainbow
    # 680. Life Block
    # 681. Guestbook Bumper
    # 682. Easter Basket
    # 683. Easter Chest
    # 684. Fancy Wood
    # 685. Green Polka Trunk
    # 686. Green Polka Base
    # 687. Giant Mushroom Stalk
    # 688. Giant Mushroom Base
    # 689. Giant Mushroom Cap
    # 690. Spring Grass
    # 691. Mossy Tree Trunk
    # 692. Water Lily
    # 693. Raffle Box
    # 694. WarpaCola Bumper
    # 695. Telefrank Bumper
    # 696. Transpickle Bumper
    # 697. QuantumFries Bumper
    # 698. Rehydrator
    # 699. (Active) - Rehydrator
    # 700. Gather Bumper
    # 701. Realm Info Bumper
    # 702. Realm Flash Bumper
    # 703. Claim Bumper
    # 704. Timed Claim Bumper
    # 705. Cubit Claim Bumper
    # 706. Foundation
    # 707. (Active) - Foundation 1
    # 708. (Active) - Foundation 2
    # 709. Ecto Containment
    # 710. Ghost Gate
    # 711. Foundation 5 Height
    # 712. Foundation 10 Height
    # 713. Foundation 20 Height
    # 714. Paranormal Index
    # 715. Rent 1 Hour Bumper
    # 716. Rent 1 Day Bumper
    # 717. Rent 1 Week Bumper
    # 718. Ghost Trap
    # 719. Monster Print
    # 720. Sculpty Stone
    # 721. Cardboard Box
    # 722. Bark Block
    # 723. Sculpty Dirt
    # 724. Sculpty Grass
    # 725. Sculpty New Wood
    # 726. Sculpty Old Wood
    # 727. Sculpty Coal
    # 728. Sculpty Bark
    # 729. Sculpty Iron
    # 730. Sculpty Clay
    # 731. Sculpty Sand
    # 732. White Pixel
    # 733. Grey Pixel
    # 734. Light Grey Pixel
    # 735. Indigo Pixel
    # 736. Deep Green Pixel
    # 737. Burnt Umber Pixel
    # 738. Dark Purple Pixel
    # 739. Light Blue Pixel
    # 740. Light Green Pixel
    # 741. Tan Pixel
    # 742. Red Pixel
    # 743. Cyan Pixel
    # 744. Yellow Pixel
    # 745. Orange Pixel
    # 746. Pink Pixel
    # 747. Roast Ham
    # 748. Bread Basket
    # 749. Pumpkin Pie
    # 750. TV
    # 751. Coffee
    # 752. Rustic Chest
    # 753. Fall Wreath
    # 754. Hay Bale
    # 755. Turkey Kennel
    # 756. Gingerbread
    # 757. Gingerbread White Wave
    # 758. Gingerbread Red Wave
    # 759. Gingerbread Green Wave
    # 760. Gingerbread White Diamond
    # 761. Gingerbread Red Diamond
    # 762. Gingerbread Green Diamond
    # 763. Gummy Road
    # 764. Big Snowflake
    # 765. Gingerbread Candy Sprinkles
    # 766. Big Bow
    # 767. Mr. Snowman Head
    # 768. Mr. Snowman Body
    # 769. Vending Machine
    # 770. Rocky Farm Soil
    # 771. Decent Farm Soil
    # 772. Quality Farm Soil
    # 773. Watered Rocky Farm Soil
    # 774. Watered Decent Farm Soil
    # 775. Watered Quality Farm Soil
    # 776. Planted Seed
    # 777. Eggplant 1
    # 778. Eggplant 2
    # 779. Eggplant 3
    # 780. Eggplant 4
    # 781. Eggplant 5
    # 782. Withered Plant
    # 783. Old Barn
    # 784. Rusty Aluminium
    # 785. Barn Door 1
    # 786. Barn Red
    # 787. Barn Door 2
    # 788. Trough
    # 789. Starter Scaffold
    # 790. Starting Line
    # 791. Finishing Line
    # 792. Traffic Cone
    # 793. Racing Curb
    # 794. Starter Pistol Bumper
    # 795. Traffic Light Green
    # 796. Traffic Light Yellow
    # 797. Traffic Light Red
    # 798. Race Marker Horizontal
    # 799. Race Marker Vertical
    # 800. Pedestrians Only
    # 801. White Tire Stack
    # 802. Red Tire Stack
    # 803. Blue Tire Stack
    # 804. Red Bleacher Bench
    # 805. Blue Bleacher Bench
    # 806. Giant Rose Petals
    # 807. Big Fancy Vase
    # 808. Big Classic Vase
    # 809. Big Teddy
    # 810. Rose Bouquet
    # 811. Fancy Vase
    # 812. Classic Vase
    # 813. Teddy Bear
    # 814. Daisy Bouquet
    # 815. Corn 1
    # 816. Corn 2
    # 817. Corn 3
    # 818. Corn 4
    # 819. Corn 5
    # 820. Eggplant Seeds
    # 821. Corn Seeds
    # 822. Small Sprinkler
    # 823. Big Sprinkler
    # 824. Painting (Sun Break)
    # 825. Painting (The Pond)
    # 826. Painting (Fragrant Flowers)
    # 827. Pink Flowering Leaves
    # 828. White Flowering Leaves
    # 829. Rabbit Hole
    # 830. Seeker Egg
    # 831. Seeker Skull
    # 832. Seeker Key
    # 833. Seeker Coin
    # 834. Seeker Bumper
    # 835. Hog-Inna-Crate
    # 836. Cow-Inna-Crate
    # 837. Chick-Inna-Crate
    # 838. Potato 1
    # 839. Potato 2
    # 840. Potato 3
    # 841. Potato 4
    # 842. Potato 5
    # 843. Tomato 1
    # 844. Tomato 2
    # 845. Tomato 3
    # 846. Tomato 4
    # 847. Tomato 5
    # 848. Wheat 1
    # 849. Wheat 2
    # 850. Wheat 3
    # 851. Wheat 4
    # 852. Wheat 5
    # 853. Tomato Seeds
    # 854. Potato Seeds
    # 855. Wheat Seeds
    # 856. Sugarcane
    # 857. Mud Cake
    # 858. Corn Bread
    # 859. Sunny Side Up Eggs
    # 860. Veggie Omelette
    # 861. Scrambled Eggs
    # 862. Fries
    # 863. 3 Legged Stool
    # 864. Night Table
    # 865. Pig Sign
    # 866. Cow Sign
    # 867. Chicken Sign
    # 868. Wheat Sign
    # 869. Eggplant Sign
    # 870. Potato Sign
    # 871. Tomato Sign
    # 872. Corn Sign
    # 873. (Active) - Stove
    # 874. Red Beach Umbrella
    # 875. Blue Beach Umbrella
    # 876. Green Beach Umbrella
    # 877. Purple Beach Umbrella
    # 878. Rainbow Beach Umbrella
    # 879. Sandcastle Tower
    # 880. Sandcastle Block
    # 881. Sandcastle Turret
    # 882. Sand Dune
    # 883. Clammy Clam
    # 884. (Active) - Clammy Clam
    # 885. No Balls!
    # 886. Block Popper!
    # 887. Cubic Town Speaker
    # 888. QBee Quest Speaker
    # 889. The Cubening Speaker
    # 890. QBee Fields Speaker
    # 891. Cut-O-Matik 5000!
    # 893. Rustic Coffin
    # 893. Fancy Coffin
    # 894. Deluxe Coffin
    # 895. Orb Web
    # 896. Friendly Orb Web
    # 897. Spider Den
    # 898. Big Jack I
    # 899. Big Jack II
    # 900. Pumpkin 1
    # 901. Pumpkin 2
    # 902. Pumpkin 3
    # 903. Pumpkin 4
    # 904. Pumpkin 5
    # 905. Pumpkin Seeds
    # 906. Spirit Lamp I
    # 907. Spirit Lamp II
    # 908. Spirit Lamp III
    # 909. Haunted Lamp I
    # 910. Haunted Lamp II
    # 911. Haunted Lamp III
    # 912. Spirit Stone
    # 913. Cubiosaur VI
    # 914. Cubiosaur XI
    # 915. Cubiosaur V
    # 916. Cubiosaur VIII
    # 917. Cubiosaur III
    # 918. Cubiosaur I
    # 919. Cubiosaur VII
    # 920. Cubiosaur IV
    # 921. Cubiosaur IX
    # 922. Cubiosaur X
    # 923. Cubiosaur II
    # 924. Cubiosaur XII
    # 925. Cubiosaur XIV
    # 926. Cubiosaur XIII
    # 927. Cubiosaur XV
    # 928. Ancient Tech V
    # 929. Ancient Tech III
    # 930. Ancient Tech II
    # 931. Ancient Tech XIV
    # 932. Ancient Tech I
    # 933. Ancient Tech XIII
    # 934. Ancient Tech VII
    # 935. Ancient Tech XI
    # 936. Ancient Tech IX
    # 937. Ancient Tech X
    # 938. Ancient Tech VIII
    # 939. Ancient Tech XII
    # 940. Ancient Tech VI
    # 941. Ancient Tech IV
    # 942. Ancient Tech XV
    # 943. Lil' Bed
    # 944. Cornucopia
    # 945. Desk Pot
    # 946. Small Desk
    # 947. Mirror
    # 948. Miso Soup
    # 949. Phone
    # 950. Radio
    # 951. Scarecrow I
    # 952. Scarecrow II
    # 953. Scarecrow III
    # 954. Scarecrow IV
    # 955. Shop Display
    # 956. Spaghetti
    # 957. Sushi Rolls
    # 958. Shop Sign
    # 959. Drinks Sign
    # 960. Chest Sign
    # 961. Wood Post
    # 962. Fairy Stone I
    # 963. Fairy Stone II
    # 964. Fairy Stone III
    # 965. Fairy Stone IV
    # 966. Fairy Seeds
    # 967. No Littering!
    # 968. Gift Sign
    # 969. Candy Cane Sign
    # 970. Fairy Plant 1
    # 971. Fairy Plant 2
    # 972. Fairy Plant 3
    # 973. Fairy Plant 4
    # 974. Mystic Mushroom
    # 975. Fairy Orchid
    # 976. Fairy Grass
    # 977. Fairy Flytrap
    # 978. Home Sign
    # 979. Fairy Soil
    # 980. Watered Fairy Soil
    # 981. Jingle Bells Speaker
    # 982. QBee Bells Speaker
    # 983. Box O' Blocks
    # 984. Christmas Chest
    # 985. Log Pile
    # 986. Snowy Log Pile
    # 987. Penguin Pad
    # 988. Sitting Stump
    # 989. Sitting Log
    # 990. Fancy Pink Cake
    # 991. Fancy Lavender Cake
    # 992. Luvbug-Inna-Box
    # 993. Wall Plant
    # 994. Blue Egg Flower
    # 995. Pink Egg Flower
    # 996. Easter Pow Gift!
    # 997. Carrot 1
    # 998. Carrot 2
    # 999. Carrot 3
    # 1000. Carrot 4
    # 1001. Carrot 5
    # 1002. Carrot Seeds
    # 1003. Carrot Cake
    # 1004. Carrot Soup
    # 1005. Cartoon Tree
    # 1006. Fruity Cartoon Tree
    # 1007. Bunnyzilla Mannequin
    # 1008. Pressure Plate
    # 1009. Heavy Pressure Plate
    # 1010. Switch
    # 1011. Timed Switch
    # 1012. Red Receiver
    # 1013. Green Receiver
    # 1014. Blue Receiver
    # 1015. Poison Spikes
    # 1016. Outline Block
    # 1017. Receiver Negator
    # 1018. Receiver Extender
    # 1019. Event Bumper
    # 1020. Modern Extractor
    # 1021. Modern Distiller
    # 1022. Modern Stove
    # 1023. Cooler
    # 1024. Outdoor Grill
    # 1025. Fiberglass
    # 1026. Slyme Ball
    # 1027. Master Book
    # 1028. Mineral Deposit
    # 1029. Shell
    # 1030. Sulfur
    # 1031. Summoning Circle
    # 1032. Thorny Vines
    # 1033. Sleeping Bag
    # 1034. Campfire
    # 1035. Camping Tent
    # 1036. Striped Camping Tent
    # 1037. Wild Grass
    # 1038. Forest Grass
    # 1039. Half Forest Grass
    # 1040. Forest Leaves
    # 1041. Wild Blue Flower
    # 1042. Wild Red Flower
    # 1043. Wild White Flower
    # 1044. First Aid Kit
    # 1045. Fish Trophy
    # 1046. Bear Trap
    # 1047. Canned Goods
    # 1048. Blender
    # 1049. White Coffee Machine
    # 1050. Black Coffee Machine
    # 1051. Kitchen Counter
    # 1052. Kitchen Cupboard
    # 1053. Kitchen Sink
    # 1054. Expresso Machine
    # 1055. Food Processor
    # 1056. Modern Fridge
    # 1057. Mini Fridge
    # 1058. Ice Container
    # 1059. Knife Holder
    # 1060. Microwave
    # 1061. Range Hood
    # 1062. Rice Cooker
    # 1063. Toaster Over
    # 1064. Toaster
    # 1065. Waffle Maker
    # 1066. Jumbled Kitchen Tile
    # 1067. Big Kitchen Tile
    # 1068. Angled Kitchen Tile
    # 1069. Bread Box
    # 1070. Dishwasher
    # 1071. Night Shroom
    # 1072. Old Crossroad Sign
    # 1073. Old Grandfather's Painting
    # 1074. Death Potion
    # 1075. Mana Potion
    # 1076. Poison Potion
    # 1077. Multiple Night Shroom
    # 1078. Halloween Door
    # 1079. Bronze Gift Piggy
    # 1080. Silver Gift Piggy
    # 1081. Gold Gift Piggy
    # 1082. Tech Workbench
    # 1083. Expert Workbench
    # 1084. Chicken Nuggets
    # 1085. French Fries
    # 1086. Hamburger
    # 1087. Hotdog
    # 1088. Softdrink
    # 1089. Fiesta Decoration
    # 1090. Food Cart 1
    # 1091. Food Cart 2
    # 1092. Food Cart 3
    # 1093. Wheelbarrow
    # 1094. Pumpkin Food Stall
    # 1095. Apple Food Stall
    # 1096. Blue Balloon
    # 1097. Orange Balloon
    # 1098. Yellow Balloon
    # 1099. Multi Balloon
    # 1100. Fall Leaves
    # 1101. Wizard's Workbench
    # 1102. Kangaroo Kennel
    # 1103. Ostrich Pit
    # 1104. Overworld Grass
    # 1105. Overworld Scrub
    # 1106. Overworld Ocean
    # 1107. Overworld Sand
    # 1108. Overworld Mountain
    # 1109. Overworld Realm Spot
    # 1110. (Active) - Overworld Realm Spot
    # 1111. Overworld Wild Realm
    # 1112. Overworld Start
    # 1113. ABC Blocks
    # 1114. Toy Soldier
    # 1115. Train Toy
    # 1116. Train Toy with Yule Tree
    # 1117. Star Carol
    # 1118. Christmas Lights
    # 1119. Yule Bells
    # 1120. Yule Wallpaper
    # 1121. Wood Sled
    # 1122. Igloo
    # 1123. Christmas Card
    # 1124. Angel Topper
    # 1125. Microphone
    # 1126. Heart Bush
    # 1127. Heart Blower
    # 1128. Kissing Booth
    # 1129. Overworld Official Icon
    # 1130. Overworld Map Icon
    # 1131. Overworld Blocks Icon
    # 1132. Overworld Planet Icon
    # 1133. Overworld QBee Icon
    # 1134. Overworld Star Icon
    # 1135. Useless Box
    # 1136. Overworld Snowy Scrub
    # 1137. Overworld Cracked Earth
    # 1138. Acorn Streetlight
    # 1139. Carrot House
    # 1140. White Lotus Flower Clump
    # 1141. Purple Flower
    # 1142. Rose Flower
    # 1143. Purple Flower Clump
    # 1144. Egg House
    # 1145. Black Rabbit Villager
    # 1146. Pink Rabbit Villager
    # 1147. Blue Rabbit Villager
    # 1148. Orange Rabbit Villager
    # 1149. Green Rabbit Villager
    # 1150. Cuberge Egg 1
    # 1151. Cuberge Egg 2
    # 1152. Moss Patch
    # 1153. Bunny Hole
    # 1154. Moonar Surface
    # 1155. Moonar Rocks
    # 1156. Moonar Crater 1
    # 1157. Moonar Crater 2
    # 1158. Moonar Crater 3
    # 1159. Alien Monument
    # 1160. Moon Dome
    # 1161. Space Radar
    # 1162. Slow Conveyor
    # 1163. Fast Conveyor
    # 1164. Model C Station
    # 1165. Model N Station
    # 1166. Model F Station
    # 1167. Red Laser Wall
    # 1168. Access Control Panel
    # 1169. Sci Fi Cabinet
    # 1170. Sci Fi Chest
    # 1171. Single Computer Station
    # 1172. Double Computer Station
    # 1173. Hibernation Pod
    # 1174. Hologram Device
    # 1175. Meeting Table
    # 1176. Railings
    # 1177. Sci Fi Table
    # 1178. Servers
    # 1179. Wall Monitor
    # 1180. Chart Wall Monitor
    # 1181. Stats Wall Monitor
    # 1182. Alien Plant
    # 1183. Alien Rock
    # 1184. Alien Stalagmite
    # 1185. Sci Fi Blue Chair
    # 1186. Alien Surface
    # 1187. Sci Fi Floor
    # 1188. Sci Fi Wall
    # 1189. Sci Fi Red Chair
    # 1190. Destination Wall Monitor
    # 1191. Charts 2 Wall Monitor
    # 1192. Warning Wall Monitor
    # 1193. Space Drone
    # 1194. Green Laser Wall
    # 1195. Halloween Ghost
    # 1196. Haunted Candelabra
    # 1197. Picture Frame 1
    # 1198. Picture Frame 2
    # 1199. Haunted Picture Frame 1
    # 1200. Haunted Picture Frame 2
    # 1201. Dead Grass
    # 1202. Zombie Hand
    # 1203. Crimson Block
    # 1204. Dead Grass 2
    # 1205. Hieroglyph
    # 1206. Mummy Coffin
    # 1207. Web Block
    # 1208. Mini Pyramid
    # 1209. Monster Mash
    # 1210. Kewberno's Battery
    # 1211. Kewberno's Mash Receptor
    # 1212. Kewberno's Coupler
    # 1213. Kewberno's Komputer
    # 1214. Kewberno's Memory
    # 1215. Mutant Doog Kennel
    # 1216. Mutant Meemew Kennel
    # 1217. Mutant Hopper House
    # 1218. Apple Pie
    # 1219. Beef Steak
    # 1220. Chair 2019
    # 1221. Cordon Bleu
    # 1222. Fancy ClothTable
    # 1223. Fried Rice w Toppings
    # 1224. Fried Rice
    # 1225. Meatballs
    # 1226. Fancy Low Cabinet
    # 1227. Pudding
    # 1228. Pumpkin Soup
    # 1229. Stew
    # 1230. Wall Clock
    # 1231. Grass Block
    # 1232. High State Floor
    # 1233. Big BlueBerry Pie
    # 1234. Butternut Squash Soup
    # 1235. Candied Yams
    # 1236. Gravy
    # 1237. Green Bean Casserole
    # 1238. Stuffing
    # 1239. Turkey Chair
    # 1240. Turkey Table
    # 1241. Column Christmas Lights
    # 1242. Christmas Sock
    # 1243. Christmas Sock 2
    # 1244. Ice Brick
    # 1245. Ice Chair
    # 1246. Ice Floor
    # 1247. Ice Ladder
    # 1248. Ice Sofa
    # 1249. Ice Stalagmites
    # 1250. Ice Table
    # 1251. Ice Throne
    # 1252. Snowflakes Block
    # 1253. Gauge
    # 1254. Lever
    # 1255. Lever 2
    # 1256. Pipe Chair
    # 1257. Pipe Sofa
    # 1258. Pipe With Valve
    # 1259. Vertical Pipe
    # 1260. Horizontal Pipe
    # 1261. Vertical Curve Pipe
    # 1262. Vertical Cross Pipe
    # 1263. T-Shape Pipe
    # 1264. Inverted T Pipe
    # 1265. Inverted Curve Pipe
    # 1266. Horizontal Curve Pipe
    # 1267. Horizontal Cross Pipe
    # 1268. Pressure Tank
    # 1269. Pressure Tank 2
    # 1270. Valve
    # 1271. SteamPunk Floor
    # 1272. SteamPunk Metal Floor
    # 1273. SteamPunk Fancy Flooring
    # 1274. Horizontal Broken Steam Pipe
    # 1275. Steamy Floor
    # 1276. Barrels
    # 1277. Old Bucket
    # 1278. SteamPunk Chest
    # 1279. SteamPunk Computer
    # 1280. SteamPunk Floor
    # 1281. SteamPunk Wall
    # 1282. Ventillation
    # 1283. Vertical Broken Steam Pipe
    # 1284. Love Bench
    # 1285. Orange Butterfly Sticker
    # 1286. Green Butterfly Sticker
    # 1287. Rainbow Butterfly Sticker
    # 1288. Heart Chair
    # 1289. Heart Table
    # 1290. Heart Topiary
    # 1291. Vertical T-Shape Pipe
    # 1292. Wooden Chair
    # 1293. Log Fence
    # 1294. Wooden Bridge
    # 1295. BlueGreen Checkered Wallpaper
    # 1296. YellowOrange Checkered Wallpaper
    # 1297. Striped Wallpaper
    # 1298. Cattail Plant
    # 1299. Red Tulip Flower
    # 1300. White Tulip Flower
    # 1301. Blue Tulip Flower
    # 1302. Log Fence Corner
    # 1303. Mossy Rock
    # 1304. Wild Plant
    # 1305. Red Easter Chair
    # 1306. Blue Easter Chair
    # 1307. Red Easter Table
    # 1308. Blue Easter Table
    # 1309. Giant Egg
    # 1310. Gold Gear
    # 1311. Bronze Gear
    # 1312. Horizontal Pipe's Endcap
    # 1313. Vertical Pipe's Endcap Up
    # 1314. Vertical Pipe's Endcap Down
    # 1315. SteamPunk Capsule
    # 1316. SteamPunk Telescope
    # 1317. Silver Gear
    # 1318. SteamPunk Wall Capsule
    # 1319. SteamPunk Wall Lamp
    # 1320. Big Clam
    # 1321. Big Starfish
    # 1322. Clams
    # 1323. Corals 1
    # 1324. Corals 2
    # 1325. Corals 3
    # 1326. Corals 4
    # 1327. Corals 5
    # 1328. Kelp
    # 1329. Red Algae
    # 1330. Starfish
    # 1331. Yellow Algae
    # 1332. Sea Sand
    # 1333. Sea Urchin
    # 1334. Sunken Treasure Closed
    # 1335. Sunken Treasure Opened
    # 1336. CuttleFish-Inna-Box
    # 1337. JellyFish-Inna-Box
    # 1338. PufferFish-Inna-Box
    # 1339. Illuminated Coral
    # 1340. Pearlite
    # 1341. Bubbly Coral
    # 1342. Bubbly Vent
    # 1343. Colorful Coral
    # 1344. Brown Coral
    # 1345. Red Coral
    # 1346. Green Coral
    # 1347. Dry Cracked Land
    # 1348. Old Bricks
    # 1349. Old Pavement Floor
    # 1350. Old Wall
    # 1351. Old Wood Floor
    # 1352. Lightning Rod
    # 1353. Old LabMachine 1
    # 1354. Old LabMachine 2
    # 1355. Test Tube 01
    # 1356. Test Tube 02
    # 1357. Black Widow
    # 1358. Tarantula
    # 1359. Monster Grave 2020
    # 1360. Haunted Monster Grave 2020
    # 1361. Relic of Bad I
    # 1362. Relic of Bad II
    # 1363. Relic of Bad III
    # 1364. Relic of Bad IV
    # 1365. Relic of Bad V
    # 1366. Relic of Bad VI
    # 1367. Relic of Bad VII
    # 1368. Relic of Bad VIII
    # 1369. Relic of Bad IX
    # 1370. (Inactive) - Relic of Bad I
    # 1371. (Inactive) - Relic of Bad II
    # 1372. (Inactive) - Relic of Bad III
    # 1373. (Inactive) - Relic of Bad IV
    # 1374. (Inactive) - Relic of Bad V
    # 1375. (Inactive) - Relic of Bad VI
    # 1376. (Inactive) - Relic of Bad VII
    # 1377. (Inactive) - Relic of Bad VIII
    # 1378. (Inactive) - Relic of Bad IX
    # 1379. Relic of Good I
    # 1380. Relic of Good II
    # 1381. Relic of Good III
    # 1382. Relic of Good IV
    # 1383. Relic of Good V
    # 1384. Relic of Good VI
    # 1385. Relic of Good VII
    # 1386. Relic of Good VIII
    # 1387. Relic of Good IX
    # 1388. (Inactive) - Relic of Good I
    # 1389. (Inactive) - Relic of Good II
    # 1390. (Inactive) - Relic of Good III
    # 1391. (Inactive) - Relic of Good IV
    # 1392. (Inactive) - Relic of Good V
    # 1393. (Inactive) - Relic of Good VI
    # 1394. (Inactive) - Relic of Good VII
    # 1395. (Inactive) - Relic of Good VIII
    # 1396. (Inactive) - Relic of Good IX
    # 1397. Haunted Landscape 1
    # 1398. Haunted Landscape 2
    # 1399. Monster Footprint
    # 1400. Landscape 1
    # 1401. Landscape 2
    # 1402. BBQ Drumstick
    # 1403. BBQ Sauce
    # 1404. BBQ Wing
    # 1405. Breadtray
    # 1406. Pumpkin Puree
    # 1407. Roast Pumpkin
    # 1408. Sourdough
    # 1409. Hunting Bush
    # 1410. Twigs
    # 1411. Fall Bush
    # 1412. Fall Grass
    # 1413. Fall Fern
    # 1414. Fall Leaves
    # 1415. Acorn Plushie
    # 1416. Fall Scrub
    # 1417. (Active) - Hunting Bush
    # 1418. Gentlefish Trophy
    # 1419. Beakfish Trophy
    # 1420. Parrotfish Trophy
    # 1421. Qbeefish Trophy
    # 1422. Toothfish Trophy
    # 1423. Spudfish Trophy
    # 1424. Bigeye Trophy
    # 1425. Wailfish Trophy
    # 1426. Christmas Chest
    # 1427. Candy Cane Chair
    # 1428. Christmas Lantern
    # 1429. Christmas Garland
    # 1430. Gingerbread Chair
    # 1431. Gingerbread Table
    # 1432. Peppermint Candy Table
    # 1433. Bear Toy
    # 1434. Christmas Balls
    # 1435. Doll
    # 1436. Doll House
    # 1437. Toy Figurines
    # 1438. Chocolate Bar Floor
    # 1439. Dark Chocolate Bar Floor
    # 1440. White Chocolate Bar Floor
    # 1441. Cookie Stair
    # 1442. Cookie Table
    # 1443. Blue Icing Cake
    # 1444. Pink Icing Cake
    # 1445. Marshmallow End Table
    # 1446. Pretzel Post
    # 1447. Red Chocolate Cabinet
    # 1448. Elffish Trophy
    # 1449. Santafish Trophy
    # 1450. Puzzlemat Block
    # 1451. Firework Stand
    # 1452. Horizontal Wooden Post
    # 1453. New Year Red Lantern
    # 1454. New Year Blue Lantern
    # 1455. New Year Yellow Lantern
    # 1456. New Year Purple Lantern
    # 1457. 2021 NY Premium Chest 1
    # 1458. 2021 NY Premium Chest 2
    # 1459. Recycled Plastic
    # 1460. Recycled Aluminum
    # 1461. Crushed Cans
    # 1462. Seaweed
    # 1463. Leather
    # 1464. Fabulous Slug
    # 1465. Angelfish Trophy
    # 1466. Circlefish Trophy
    # 1467. Crystalfish Trophy
    # 1468. Fancyfish Trophy
    # 1469. Firefish Trophy
    # 1470. Flatfish Trophy
    # 1471. Frostfish Trophy
    # 1472. Goldenfish Trophy
    # 1473. Lazyfish Trophy
    # 1474. Magmafish Trophy
    # 1475. OneEyedfish Trophy
    # 1476. Robofish Trophy
    # 1477. Seaweedfish Trophy
    # 1478. Silverfish Trophy
    # 1479. Slimefish Trophy
    # 1480. Spikyfish Trophy
    # 1481. Squarefish Trophy
    # 1482. ThreeEyedfish Trophy
    # 1483. Trianglefish Trophy
    # 1484. Unicornfish Trophy
    # 1485. Yellow Boxfish Trophy
    # 1486. Arcticfish Trophy
    # 1487. Camerafish Trophy
    # 1488. Cowfish Trophy
    # 1489. Fewbeefish Trophy
    # 1490. Guardianfish Trophy
    # 1491. Icefish Trophy
    # 1492. Mewbeefish Trophy
    # 1493. Pigfish Trophy
    # 1494. Piratefish Trophy
    # 1495. Rainbowfish Trophy
    # 1496. Senseifish Trophy
    # 1497. Snowfish Trophy
    # 1498. Stingfish Trophy
    # 1499. Surferfish Trophy
    # 1500. Torpedofish Trophy
    # 1501. Big Whale Trophy
    # 1502. Bird Bath
    # 1503. Cypress Tree
    # 1504. Daffodil Flower
    # 1505. Dandelion Flower
    # 1506. Rose Petals
    # 1507. Sunflower
    # 1508. Valentines Garland
    # 1509. Stone Path 1
    # 1510. Stone Path 2
    # 1511. Cherry Blossom Bonsai
    # 1512. Cherry Blossom Floor
    # 1513. Cherry Blossom Leaves
    # 1514. Cherry Blossom Vase
    # 1515. Cherry Blossom Petals
    # 1516. Easter Egg Chair
    # 1517. Easter Egg Lamp
    # 1518. Easter Egg Table
    # 1519. Easter Egg Wall
    # 1520. Easter Garland
    # 1521. Garden Lantern
    # 1522. Hot Spring Faucet
    # 1523. Hot Spring Rocks
    # 1524. Cherry Blossom Lantern
    # 1525. Picnic Basket
    # 1526. Pink Smooth Wall
    # 1527. Cherry Blossom Bowl
    # 1528. Standing Lamp
    # 1529. Towel Basket
    # 1530. White Smooth Wood Wall
    # 1531. Rabbitfish Trophy
    # 1532. Eggfish Trophy
    # 1533. Player NPC
    # 1534. Fire Hydrant
    # 1535. Mossy Stone
    # 1536. Blue Neon Half Block
    # 1537. Cyan Neon Half Block
    # 1538. Green Neon Half Block
    # 1539. Pink Neon Half Block
    # 1540. Purple Neon Half Block
    # 1541. Yellow Neon Half Block
    # 1542. Ship in a Bottle
    # 1543. Clearway Sign
    # 1544. Do Not Enter Sign
    # 1545. No Parking Sign
    # 1546. No U Turn Sign
    # 1547. U Turn Sign
    # 1548. Yield Sign
    # 1549. Climbing Vines
    # 1550. Cooking Meat
    # 1551. Cooking Pot
    # 1552. Old Helmet
    # 1553. Log Floor
    # 1554. Lying Barrel
    # 1555. Old Log
    # 1556. Pole Arms
    # 1557. Sacks
    # 1558. Spiked Fence
    # 1559. Big Spike Wall Base
    # 1560. Sword in Ground
    # 1561. Tall Grass
    # 1562. Wooden Platform
    # 1563. Totem 1
    # 1564. Custom Block 1
    # 1565. Custom Block 2
    # 1566. Custom Block 3
    # 1567. Custom Block 4
    # 1568. Custom Block 5
    # 1569. Custom Block 6
    # 1570. Custom Block 7
    # 1571. Custom Block 8
    # 1572. Custom Block 9
    # 1573. Custom Block 10
    # 1574. Custom Block 11
    # 1575. Custom Block 12
    # 1576. Custom Block 13
    # 1577. Custom Block 14
    # 1578. Custom Block 15
    # 1579. Custom Block 16
    # 1580. Texture Easle
    # 1581. Texture Projector
    # 1582. Copier
    # 1583. Plastic Baby Corn
    # 1584. Plastic Young Corn
    # 1585. Plastic Medium Corn
    # 1586. Plastic Big Corn
    # 1587. Plastic Corn
    # 1588. Plastic Baby Potato
    # 1589. Plastic Young Potato
    # 1590. Plastic Medium Potato
    # 1591. Plastic Big Potato
    # 1592. Plastic Potato
    # 1593. Plastic Baby Tomato
    # 1594. Plastic Young Tomato
    # 1595. Plastic Medium Tomato
    # 1596. Plastic Big Tomato
    # 1597. Plastic Tomato
    # 1598. Plastic Baby Wheat
    # 1599. Plastic Young Wheat
    # 1600. Plastic Medium Wheat
    # 1601. Plastic Big Wheat
    # 1602. Plastic Wheat
    # 1603. Plastic Baby Eggplant
    # 1604. Plastic Young Eggplant
    # 1605. Plastic Medium Eggplant
    # 1606. Plastic Big Eggplant
    # 1607. Plastic Eggplant
    # 1608. Plastic Withered Plant
    # 1609. Plastic Baby Carrot
    # 1610. Plastic Young Carrot
    # 1611. Plastic Medium Carrot
    # 1612. Plastic Big Carrot
    # 1613. Plastic Carrot
    # 1614. Plastic Baby Pumpkin
    # 1615. Plastic Young Pumpkin
    # 1616. Plastic Medium Pumpkin
    # 1617. Plastic Big Pumpkin
    # 1618. Plastic Pumpkin
    # 1619. Totem 2
    # 1620. Earthen Vase
    # 1621. Earthen Vases
    # 1622. Vine Wall
    # 1623. Ancient Floor
    # 1624. Ancient Wall
    # 1625. Animal Skull
    # 1626. Big Spike Wall Tip
    # 1627. Spike Wall Base
    # 1628. Spike wall Tip
    # 1629. Trophy Stand
    # 1630. 1st Year Trophy
    # 1631. 2nd Year Trophy
    # 1632. 3rd Year Trophy
    # 1633. 4th Year Trophy
    # 1634. 5th Year Trophy
    # 1635. 6th Year Trophy
    # 1636. Script Trigger Block
    # 1637. Black Framed 1
    # 1638. Black Framed 2
    # 1639. Black Framed 3
    # 1640. Black Brick Wall
    # 1641. Halloween Garland
    # 1642. Spider Cabinet
    # 1643. Spider Chair
    # 1644. Spider Chest
    # 1645. Spider Table
    # 1646. Bullyfish Trophy
    # 1647. Ancientfish Trophy
    # 1648. Crazyfish Trophy
    # 1649. Corpsefish Trophy
    # 1650. Bonefish Trophy
    # 1651. Halloweenfish Trophy
    # 1652. Eelk Trophy
    # 1653. Headlessfish Trophy
    # 1654. Squid Trophy
    # 1655. Eyeballfish Trophy
    # 1656. Allium Flowers
    # 1657. Baked Sweet Potato
    # 1658. Cranberyy Pie
    # 1659. Cranberry Sauce
    # 1660. Static Fall Leaves
    # 1661. Pecan Pie
    # 1662. Pumpkin Chair
    # 1663. Pumpkin Table
    # 1664. Redish Bush
    # 1665. Redish Tree Leaves
    # 1666. Christmas Cabinet
    # 1667. Christmas Garland 2
    # 1668. Frosted Chest
    # 1669. Frosted Bench
    # 1670. Frozen Tree
    # 1671. Peppermint Candy 1
    # 1672. Peppermint Candy 2
    # 1673. Peppermint Wreath
    # 1674. Snow Ladder
    # 1675. Snow Stairs
    # 1676. Winter Chair
    # 1677. Winter Table
    # 1678. Magic Xmas
    # 1679. (Inactive) - Magic Xmas
    # 1680. Mini Grouch Kennel
    # 1681. Mini Krampus Kennel
    # 1682. Husky Kennel
    # 1683. Linzer Cookies
    # 1684. Macaron
    # 1685. Piano
    # 1686. Red Velvet Cake
    # 1687. Rose Garland
    # 1688. Valentine Table
    # 1689. Valentine Chest
    # 1690. Valentine Sofa
    # 1691. Love Fence
    # 1692. Heartfish Trophy
    # 1693. Luv Fish Trophy
    # 1694. 7th Year Trophy
    # 1695. 8th Year Trophy
    # 1696. New Wood Picket Fence
    # 1697. Old Wood Picket Fence
    # 1698. White Wood Picket Fence
    # 1699. Bird House
    # 1700. Blue Bonnet  
    # 1701. Carrot Plushie  
    # 1702. Cuckoo Clock  
    # 1703. Easter Wreath  
    # 1704. Green Egg Flower  
    # 1705. Lemon Wooden Chair  
    # 1706. Lemon Wooden Table  
    # 1707. Poppy Flower  
    # 1708. Yellow Egg Flower  
    # 1709. Hazard Block 00  
    # 1710. Hazard Block 01  
    # 1711. Hazard Block 02  
    # 1712. Hazard Block 03  
    # 1713. Hazard Block 04  
    # 1714. Hazard Block 05  
    # 1715. Long Slyme Vat  
    # 1716. Open Slyme Barrel  
    # 1717. Slyme Barrel  
    # 1718. Slyme Block  
    # 1719. Slyme Glass Container  
    # 1720. Slyme Half Block  
    # 1721. Slyme Leaking Wall  
    # 1722. Slyme Machines 01  
    # 1723. Slyme Machines 02  
    # 1724. Slyme Puddle  
    # 1725. Slyme Vat  
    # 1726. Slyme Vial  
    # 1727. Slyme Multiple Vial  
    # 1728. Slymegood Industry Logo  
    # 1729. Orange Reverse Vending Machine  
    # 1730. Green Reverse Vending Machine  
    # 1731. Purple Reverse Vending Machine  
    # 1732. Condemned Telivision  
    # 1733. Dark Dead Grass  
    # 1734. Dark Dead Leaves  
    # 1735. Floating Eye  
    # 1736. Halloween Cookies  
    # 1737. Halloween Sign  
    # 1738. Monster Tree  
    # 1739. Toy Witch  
    # 1740. Toy Zombie  
    # 1741. Broken Frame  
    # 1742. Dust Pile  
    # 1743. White "Help Me"  
    # 1744. White "I See You"  
    # 1745. Red "Help Me"  
    # 1746. Red "I See You"  
    # 1747. Red Scratches  
    # 1748. White Scratches  
    # 1749. Kewberno's Cell  
    # 1750. Kewberno's Tube  
    # 1751. Kewberno's CPU  
    # 1752. Kewberno's DNA  
    # 1753. Kewberno's Monster Creator  
    # 1754. Monster Mash 2  
    # 1755. Good Statue I  
    # 1756. Good Statue II  
    # 1757. Good Statue III  
    # 1758. Good Statue IV  
    # 1759. Good Statue V  
    # 1760. Good Statue VI  
    # 1761. Good Statue VII  
    # 1762. Evil Statue I  
    # 1763. Evil Statue II  
    # 1764. Evil Statue III  
    # 1765. Evil Statue IV  
    # 1766. Evil Statue V  
    # 1767. Evil Statue VI  
    # 1768. Evil Statue VII  
    # 1769. Neutral Statue I  
    # 1770. Neutral Statue II  
    # 1771. Gold Evil Trophy  
    # 1772. Gold Good Trophy  
    # 1773. Bronze Evil Trophy  
    # 1774. Bronze Good Trophy  
    # 1775. Ghost Bomb  
    # 1776. Mutant Wuvva Pig Kennel  
    # 1777. Mutant Ram Kennel  
    # 1778. Bird Poop 01  
    # 1779. Bird Poop 02  
    # 1780. Bird Poop 03  
    # 1781. Acorn Garland  
    # 1782. Golden Pumpkin  
    # 1783. Leafy Chair  
    # 1784. Leafy Table  
    # 1785. Pumpkin Cheesecake  
    # 1786. Pumpkin Muffins  
    # 1787. Stacked Pumpkin  
    # 1788. Thanksgiving Sign  
    # 1789. Turkey Wreath  
    # 1790. Candy Cane Streetlight  
    # 1791. Chicken Bucket  
    # 1792. Christmas Star  
    # 1793. Fruit Cake  
    # 1794. Matryoshka Doll  
    # 1795. Mince Pies  
    # 1796. Poinsettia 2  
    # 1797. Yule Goat  
    # 1798. Patrudge Fish Trophy  
    # 1799. Turtle Dove Trophy  
    # 1800. French Hen Seahorse Trophy  
    # 1801. Calling Bird Fish Trophy  
    # 1802. Five Ring Trophy  
    # 1803. Goose Fish Trophy  
    # 1804. Swan Eel Trophy  
    # 1805. Milk Jelly Fish Trophy  
    # 1806. Dancing Lady Fish Trophy  
    # 1807. Leaping Lord Jellyfish Trophy  
    # 1808. Piper Fish Trophy  
    # 1809. Drum Crab Trophy  
    # 1810. Dasher  
    # 1811. Dancer  
    # 1812. Prancer  
    # 1813. Vixen  
    # 1814. Comet  
    # 1815. Cupid  
    # 1816. Donner  
    # 1817. Blitzen  
    # 1818. Rudolph  
    # 1819. Elf  
    # 1820. Mrs. Claus  
    # 1821. Mr. Santa Claus
    # 1822. Wooden Premium Chest  
    # 1823. Blue Premium Chest  
    # 1824. Green Premium Chest  
    # 1825. Red Premium Chest  
    # 1826. Baguette  
    # 1827. Balloon Heart  
    # 1828. Bubbly Drink  
    # 1829. Bubbly Glass  
    # 1829. Croissant  
    # 1830. Eclair  
    # 1831. Heart Chocolate Box  
    # 1832. Heart Stump  
    # 1833. Heart Tree Leaves  
    # 1834. Easter Egg Balloon 01  
    # 1835. Easter Egg Balloon 02  
    # 1836. Easter Egg Lantern  
    # 1837. Egg Topiary  
    # 1838. Golden Egg Decor  
    # 1839. Blue Plush Bunny  
    # 1840. Green Plush Bunny  
    # 1841. Pink Plush Bunny  
    # 1842. Rabbit Topiary  
    # 1843. Rainbow Bush  
    # 1844. Rainbow Tree Leaves  
    # 1845. Crash Figurine  
    # 1846. Chest Crate  
    # 1847. Eggie Figurine  
    # 1848. Giant Magnet  
    # 1849. Multi Golden Eggs  
    # 1851. Ice king Figurine 
    # 1852. Mutant Plant 
    # 1853. Pablo Figurine  
    # 1854. Radioactive Debris  
    # 1855. Radioactive Sign  
    # 1856. Radioactive Stone  
    # 1857. Z'Chicken-Inna-Box  
    # 1858. Bat Sticker  
    # 1859. Dark Tall Window  
    # 1860. Dark Window  
    # 1861. Pile of Candies  
    # 1862. Skull Candle  
    # 1863. Spiked Fence  
    # 1864. Tall Spiked Fence  
    # 1865. Wall Shackles  
    # 1866. Acorns  
    # 1867. Butter Plate  
    # 1868. Caramel Apple  
    # 1869. French Toast  
    # 1870. Giant Maple Leaf  
    # 1871. Honey Jar  
    # 1872. Maple Syrup  
    # 1873. Pancake  
    # 1874. Pizza  
    # 1875. Giant Bell  
    # 1876. Gingerbread House  
    # 1877. Ice Bench  
    # 1878. Ice Column  
    # 1879. Ice Fence  
    # 1880. Icesharp Pillar  
    # 1881. Ice Spikes  
    # 1882. Snow Angel Mark  
    # 1883. Snowball Pile  
    # 1884. Candy Cane Block  
    # 1885. Green Peppermint Candy  
    # 1886. Golden Peppermint Candy  
    # 1887. High Elf Chest  
    # 1888. Ancient Sea Chest  
    # 1889. Time Chest
    # 1890. Heart Harp
    # 1891. Heart Lock
    # 1892. Love Letters Pile
    # 1893. Love Potion
    # 1894. Mini Eiffel Tower
    # 1895. Pink Swan Display
    # 1896. Ring in a Box
    # 1897. Rose Candle
    # 1898. Swan Display
    # 1899. Aircon 01
    # 1900. White Bed
    # 1901. Blue Bed
    # 1902. Red Bed
    # 1903. Window Blinds 01
    # 1904. Blue Curtains
    # 1905. Red Curtains
    # 1906. Slim Speakers
    # 1907. Speakers
    # 1908. Yellow Standing Lamp
    # 1909. Black Standing Lamp
    # 1910. 28" Flat TV
    # 1911. 64" Flat TV
    # 1912. Vase 01
    # 1913. Vase 02
    # 1914. Bee Hive 02
    # 1915. Chocolate Egg
    # 1916. Egg Rug
    # 1917. Giant Cracked Egg
    # 1918. Golden Anchor
    # 1919. Honeycomb Rug
    # 1920. Leaf Chair
    # 1921. Paper Windmills
    # 1922. Sunflower Table
    # 1923. Aircon 02
    # 1924. Barbell 01
    # 1925. Window Blinds 02
    # 1926. Window Blinds 03
    # 1927. Chess 01
    # 1928. Aqua-Teal Curtains
    # 1929. Orange Curtains
    # 1930. Red-White Curtains
    # 1931. Bunk Bed 01
    # 1932. Bunk Bed 02
    # 1933. Bund Bed 03
    # 1934. Red Drapery
    # 1935. Yellow Drapery
    # 1936. Dumbbells 01
    # 1937. Floor Fan 01
    # 1938. Kettlebell 01
    # 1939. Light Switch 01
    # 1940. Light Switch 02
    # 1941. Mirror 01
    # 1942. Mirror 02
    # 1943. Rug 02
    # 1944. Rug 03
    # 1945. Rug 04
    # 1946. Rug 05
    # 1947. Satellite Dish 01
    # 1948. Stand Fan 01
    # 1949. Vase 03
    # 1950. Pink Curtains
    # 1951. Dino Rabbit Egg
    # 1952. Wood Door
    # 1953. Fancy Wood Door
    # 1954. Red Door
    # 1955. Pink Door
    # 1956. Blue Door
    # 1957. Green Metal Door
    # 1958. Metal Door
    # 1959. Air Hockey Machine
    # 1960. Cactus Plant
    # 1961. Computer Table
    # 1962. Curtain 07
    # 1963. Curtain 08
    # 1964. Desktop Computer
    # 1965. Drapery 03
    # 1966. Game Console
    # 1967. Goldfish Bowl
    # 1968. Guitar Stand
    # 1969. Harp
    # 1970. Laptop
    # 1971. Mirror 03
    # 1972. Mirror 04
    # 1973. Monitor
    # 1974. PC
    # 1975. Peperomia
    # 1976. Pool Table
    # 1977. Pull Up Bar
    # 1978. Record Player
    # 1979. Snake Plant
    # 1980. Storage Box
    # 1981. Treadmill
    # 1982. Ukelele (on wall)
    # 1983. Violin (on wall)
    # 1984. Wall Fan
    # 1985. Abstract Painting
    # 1986. Air Fryer
    # 1987. Alarm Clock
    # 1988. Cello
    # 1989. Coat Rack
    # 1990. Coffee Table 01
    # 1991. Coffee Table 02
    # 1992. Coffee Table 03
    # 1993. Filing Cabinets
    # 1994. Grand Piano
    # 1995. Jukebox
    # 1996. Medicine Cabinet
    # 1997. Office Chair
    # 1998. Printer
    # 1999. Shower
    # 2000. Telephone
    # 2001. Trash Bin
    # 2002. Wall Hooks
    # 2003. Wall Shelf
    # 2004. Washing Machine

# Yes, I had to do this all manually. 
# May you shed a tear for all the lost time, hope and sanity that went into making this switch table.
# The worst part is that it is not even remotely close to being complete. Wonderful :))
def get_mc_block_from_cc_id(cc_id: str, direction: str) -> BlockState:
    mc_id  = "minecraft:" + cc_to_mc_mapping.get(cc_id, "smooth_stone")
    mc_block = BlockState(mc_id, facing=direction, waterlogged="false")
    
    match mc_id:
        case "minecraft:air":
            mc_block = mc_block.with_properties(facing = None)
        case _:
            pass
    return mc_block


def bytes_to_direction(bytes):
    bytes = bytes % 4
    match bytes:
        case 0:
            return "north"
        case 1:
            return "east"
        case 2:
            return "south"
        case 3:
            return "west"
        case _:
            return "north"

# Windows API bullshit
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_ALL_ACCESS = 0x1F0FFF
PROCESS_VM_READ = 0x0010
MAX_MODULE_NAME32 = 255
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
PAGE_READWRITE = 0x04
psapi = ctypes.WinDLL('psapi.dll')
kernel32 = ctypes.windll.kernel32
EnumProcessModules = psapi.EnumProcessModules
EnumProcessModules.restype = wintypes.BOOL
EnumProcessModules.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.HMODULE), wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
GetModuleBaseName = psapi.GetModuleBaseNameW
GetModuleBaseName.restype = wintypes.DWORD
GetModuleBaseName.argtypes = [wintypes.HANDLE, wintypes.HMODULE, wintypes.LPWSTR, wintypes.DWORD]
OpenProcess = kernel32.OpenProcess
OpenProcess.restype = wintypes.HANDLE
OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
CloseHandle = kernel32.CloseHandle
CloseHandle.restype = wintypes.BOOL
CloseHandle.argtypes = [wintypes.HANDLE]
VirtualAllocEx = kernel32.VirtualAllocEx
VirtualAllocEx.argtypes = [wintypes.HANDLE, wintypes.LPVOID, ctypes.c_size_t, wintypes.DWORD, wintypes.DWORD]
VirtualAllocEx.restype = wintypes.LPVOID

# Get location of exe in memory
def get_base_address(pid, exe_name) -> int:
    # Open the process
    process_handle = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
    if not process_handle:
        print(f"Could not open process {pid}")
        return None
    
    # Allocate space for module list
    h_mod = (wintypes.HMODULE * 1024)()
    cb_needed = wintypes.DWORD()
    # Get the list of modules in the process
    if EnumProcessModules(process_handle, h_mod, ctypes.sizeof(h_mod), ctypes.byref(cb_needed)):
        num_modules = cb_needed.value // ctypes.sizeof(wintypes.HMODULE)
        for i in range(num_modules):
            # Get module base name
            mod_name = ctypes.create_unicode_buffer(MAX_MODULE_NAME32)
            GetModuleBaseName(process_handle, h_mod[i], mod_name, MAX_MODULE_NAME32)
            if exe_name.lower() in mod_name.value.lower():
                base_address = h_mod[i]
                CloseHandle(process_handle)
                return base_address
    CloseHandle(process_handle)
    return None

# Find process by name and get its PID
def get_pid() -> int:
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return proc.pid
    raise Exception(f"Process '{process_name}' not found")

# Resets the counter variable in memory to 0
def reset_counter():
    pid = get_pid()
    process_handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not process_handle:
        raise Exception("Failed to open the process")
    
    # Write the bytes to memory region
    zero_in_bytes = ("00 00 00 00")
    write_memory(process_handle, zero_in_bytes, counter_memory_address)
    kernel32.CloseHandle(process_handle)

# Grab the data of all non air blocks in the realm
# x, y, z, direction, sculpty variant, block id
def read_realm_data() -> list:
    pid = get_pid()
    process_handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not process_handle:
        raise Exception("Failed to open the process")
    
    # Get the value of counter varlable
    # This determines the size of the block data array
    counter_buffer = read_memory(process_handle, counter_memory_address, 4)
    data_length = ctypes.cast(counter_buffer, ctypes.POINTER(ctypes.c_uint32)).contents.value

    # Get the block data array of bytes
    blueprint_buffer = read_memory(process_handle, blueprint_memory_address, data_length)
    kernel32.CloseHandle(process_handle)
    return list(blueprint_buffer)

# Inject bytes into targeted memory regions
def inject_game_code():
    pid = get_pid()
    process_handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not process_handle:
        raise Exception("Failed to open the process")
    
    exe_address = get_base_address(pid, process_name)
    # Static addresses for variables
    write_memory(process_handle, variables_content, counter_memory_address)
    # Functions
    write_memory(process_handle, code_cave_1_content, exe_address + code_cave_1_offset)
    write_memory(process_handle, function_jump_1_content, exe_address + function_jump_1_offset)
    write_memory(process_handle, code_cave_2_content, exe_address + code_cave_2_offset)
    write_memory(process_handle, function_jump_2_content, exe_address + function_jump_2_offset)
    write_memory(process_handle, code_cave_3_content, exe_address + code_cave_3_offset)
    write_memory(process_handle, function_jump_3_content, exe_address + function_jump_3_offset)
    kernel32.CloseHandle(process_handle)

def write_memory(handle, content, address):
    content_in_bytes = [int(byte, 16) for byte in content.split()]
    memory_buffer = (ctypes.c_ubyte * len(content_in_bytes))(*content_in_bytes)
    kernel32.WriteProcessMemory(handle, address, memory_buffer, len(content_in_bytes), None)

def read_memory(handle, address, length) -> ctypes.c_ubyte:
    memory_buffer = (ctypes.c_ubyte * length)()
    kernel32.ReadProcessMemory(handle, address, memory_buffer, length, None)
    return memory_buffer

# User interface
# yes it's garbage atm stfu I am watching tkinter playlist
def display_menu():
    print("\nMenu:")
    print("1. Create Litematic ")
    print("2. Exit")

# A convenient package I stole from the internet that carried 99% of the work of this app
# @Litemapy
def create_litematic(schematic_directory, filename):
    # Create a Region and Schematic
    reg = Region(0, 0, 0, 100, 100, 100)
    schem = reg.as_schematic(name="Realm", author="TreacherousDev", description="Made with Litemapy")
    byte_data = read_realm_data()

    chunk_size = 7
    # Iterate over the array in chunks of 7
    for i in range(0, len(byte_data), chunk_size):
        block_data = byte_data[i:i + chunk_size]
        # Translate bytes to Litematic format
        x = int(block_data[0])
        z = int(block_data[1])
        y = 99 - int(block_data[2])
        cc_id = int((block_data[6] << 8) | block_data[5])
        sculpty_variant = int(block_data[4])
        direction = bytes_to_direction(int(block_data[3]))
        mc_block = get_mc_block_from_cc_id(cc_id, direction)
        reg[x, y, z] = mc_block

    # Save the schematic with the user-provided filename
    schem_file_path = f"{schematic_directory}/{filename}.litematic"
    schem.save(schem_file_path)
    reset_counter()


def create_litematic_pixel(schematic_directory, filename):
    # Shortcut to create a schematic with a single region
    reg = Region(0, 0, 0, 200, 200, 200)
    schem = reg.as_schematic(name="Realm", author="TreacherousDev", description="Made with Litemapy")
    byte_data = read_realm_data()

    chunk_size = 7
    # Iterate over the array in chunks of 7
    for i in range(0, len(byte_data), chunk_size):
        block_data = byte_data[i:i + chunk_size]
        #T Translate bytes to Litematic format
        x = int(block_data[0])
        z = int(block_data[1])
        y = 99 - int(block_data[2])
        cc_id = int((block_data[6] << 8) | block_data[5])
        sculpty_variant = int(block_data[4])
        direction = bytes_to_direction(int(block_data[3]))
        mc_block = get_mc_block_from_cc_id(cc_id, direction)
        sculpted_blocks = [(sculpty_variant >> i) & 1 for i in range(7, -1, -1)]
        if all(bit == 0 for bit in sculpted_blocks):
            sculpted_blocks = [1] * 8
        
        # build 2x2x2 chunk based on bit values of byte
        if sculpted_blocks[7] == 1:
            reg[(x*2), (y*2)+1, (z*2)] = mc_block
        if sculpted_blocks[6] == 1:
            reg[(x*2)+1, (y*2)+1, (z*2)] = mc_block
        if sculpted_blocks[5] == 1:
            reg[(x*2), (y*2)+1, (z*2)+1] = mc_block
        if sculpted_blocks[4] == 1:
            reg[(x*2)+1, (y*2)+1, (z*2)+1] = mc_block
        if sculpted_blocks[3] == 1:
            reg[(x*2), (y*2), (z*2)] = mc_block
        if sculpted_blocks[2] == 1:
            reg[(x*2)+1, (y*2), (z*2)] = mc_block
        if sculpted_blocks[1] == 1:
            reg[(x*2), (y*2), (z*2)+1] = mc_block
        if sculpted_blocks[0] == 1:
            reg[(x*2)+1, (y*2), (z*2)+1] = mc_block

    # Save the schematic with the user-provided filename
    schem_file_path = f"{schematic_directory}/{filename}.litematic"
    schem.save(schem_file_path)
    reset_counter()

def address_to_bytes_string(address):
    byte_string = address.to_bytes(4, 'little')
    formatted_string = ' '.join(f'{b:02x}' for b in byte_string)
    return formatted_string + " "

# Code Injection parameters
process_name = "Cubic.exe"
data_base_address = 0
blueprint_memory_address = 0
counter_memory_address = 0
# Static Variables Reference
variables_content = ("00 00 00 00 00 00 00 63 63 63")
# Function 1
code_cave_1_offset = 0x2EC321
code_cave_1_content = ""
function_jump_1_offset = 0xC8923
function_jump_1_content = ("E9 F9 39 22 00 66 90")
# Function 2
code_cave_2_offset = 0x2EC4A6
code_cave_2_content = ""
function_jump_2_offset = 0x12CB020
function_jump_2_content = ("E9 81 14 02 FF")
# Function 3
code_cave_3_offset = 0x2EC63F
code_cave_3_content = ""
function_jump_3_offset = 0x1D96F1
function_jump_3_content = ("E9 49 2F 11 00 90")

#schematic_directory = "" #"C:/Users/adant/curseforge/minecraft/Instances/Litematica/schematics"

def manage_memory():
    global data_base_address
    global counter_memory_address 
    global blueprint_memory_address
    global code_cave_1_content
    global code_cave_2_content
    global code_cave_3_content

    data_base_address = allocate_memory_in_process(7000000)
    counter_memory_address = data_base_address
    blueprint_memory_address = data_base_address + 10
    x_start = address_to_bytes_string(data_base_address + 4)
    y_start = address_to_bytes_string(data_base_address + 5)
    z_start = address_to_bytes_string(data_base_address + 6)
    x_end = address_to_bytes_string(data_base_address + 7)
    y_end = address_to_bytes_string(data_base_address + 8)
    z_end = address_to_bytes_string(data_base_address + 9)
    bp_addr = address_to_bytes_string(blueprint_memory_address)
    counter_addr = address_to_bytes_string(data_base_address)

    code_cave_1_content	= (
        "66 50 8A 46 02 3A 05 " 
        + x_start + "0F 8C 49 00 00 00 3A 05 " + x_end + "0F 8F 3D 00 00 00 8A 46 04 3A 05 "
        + y_start + "0F 8C 2E 00 00 00 3A 05 " + y_end + "0F 8F 22 00 00 00 8A 46 06 3A 05 "
        + z_start + "0F 8C 13 00 00 00 3A 05 " + z_end + "0F 8F 07 00 00 00 66 58 E9 07 00 "
        "00 00 66 58 E9 66 00 00 00 66 52 66 51 88 E1 80 E1 F0 C0 E9 04 88 CA 66 59 66 50 66 "
        "25 FF 0F 66 3D 00 00 0F 84 42 00 00 00 53 51 B9 " + bp_addr + "03 0D " + counter_addr
        + "0F B6 5E 02 88 19 0F B6 5E 04 88 59 01 0F B6 5E 06 88 59 02 0F B6 DA 88 51 03 0F "
        "B6 5E 11 88 59 04 66 89 41 05 C7 41 07 FF FF FF FF 83 05 " + counter_addr + "07 59 "
        "5B 66 58 66 5A 66 89 06 C6 46 0C 00 E9 36 C5 DD FF") 
    code_cave_2_content = ("C7 05 " + counter_addr + "00 00 00 00 9C 50 89 3C 24 E9 6B EB FD 00")
    code_cave_3_content = (
    "53 52 BB " + bp_addr +  "81 3B FF FF FF FF 0F 84 33 00 00 00 0F B6 13 3A 50 02 0F 85 22 "
    "00 00 00 0F B6 53 01 3A 50 04 0F 85 15 00 00 00 0F B6 53 02 3A 50 06 0F 85 08 00 00 00 "
    "88 4B 04 E9 05 00 00 00 83 C3 07 EB C1 5A 5B 88 48 11 8B 4D 08 E9 65 D0 EE FF")


def main():
    manage_memory()
    inject_game_code()

    def select_directory():
        directory = filedialog.askdirectory(title="Select Schematics Directory")
        if directory:
            directory_entry.delete(0, tk.END)
            directory_entry.insert(0, directory)
            checkmark_label.config(text="✓", fg="#a3d39c")

    def open_mapping_window():
        # Create a new window for updating the mapping
        mapping_window = tk.Toplevel(root)
        mapping_window.title("Update Mapping")
        mapping_window.configure(bg="#f0f4f8")

        # Create a frame for the save and cancel buttons (fixed at the top)
        top_frame = tk.Frame(mapping_window, bg="#f0f4f8")
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Save button, stays at the top
        save_button = tk.Button(top_frame, text="Save", command=lambda: update_mapping(combobox_mapping, mapping_window),
                                font=("Helvetica", 10), bg="#a3d39c", fg="white", relief="flat", activebackground="#86b08a", padx=8, pady=4)
        save_button.pack(side=tk.LEFT, padx=5)

        # Cancel button, stays at the top
        cancel_button = tk.Button(top_frame, text="Cancel", command=mapping_window.destroy,
                                  font=("Helvetica", 10), bg="#f2545b", fg="white", relief="flat", activebackground="#f0323e", padx=8, pady=4)
        cancel_button.pack(side=tk.LEFT, padx=5)

        # Create a frame with a scrollbar for the list of mappings
        canvas = tk.Canvas(mapping_window, bg="#f0f4f8", highlightthickness=0)
        scrollbar = tk.Scrollbar(mapping_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f4f8")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Comboboxes for each ID mapping
        combobox_mapping = {}

        for id_value, block_name in cc_to_mc_mapping.items():
            row_frame = tk.Frame(scrollable_frame, bg="#f0f4f8")
            row_frame.pack(pady=5, padx=10)

            id_label = tk.Label(row_frame, text=f"ID {id_value}:", font=("Helvetica", 11), bg="#f0f4f8", fg="#4a4e69")
            id_label.pack(side=tk.LEFT, padx=5)

            combobox = ttk.Combobox(row_frame, values=block_options, font=("Helvetica", 11), state="readonly", width=20)
            combobox.set(block_name)  # Set current block
            combobox.pack(side=tk.LEFT, padx=5)

            combobox_mapping[id_value] = combobox

    def update_mapping(combobox_mapping, mapping_window):
        # Update the dictionary with the current selection from comboboxes
        for id_value, combobox in combobox_mapping.items():
            cc_to_mc_mapping[id_value] = combobox.get()

        # Update the status in the main window and close the update window
        status_label.config(text="Mapping updated successfully!", fg="#6c757d")
        mapping_window.destroy()

    def create_litematic_action():
        schematic_directory = directory_entry.get()
        filename = filename_entry.get()
        mode_selected = mode_var.get()

        if schematic_directory and filename:
            pid = get_pid()
            process_handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
            counter_buffer = read_memory(process_handle, counter_memory_address, 4)
            counter = ctypes.cast(counter_buffer, ctypes.POINTER(ctypes.c_uint32)).contents.value
            if counter == 0:
                status_label.config(text="Realm not loaded to memory. Please relog :)", fg="#f2545b")
                return
            
            if mode_selected == "normal":
                create_litematic(schematic_directory, filename)
            elif mode_selected == "sculpty":
                create_litematic_pixel(schematic_directory, filename)
            status_label.config(text=f"Litematic ({mode_selected.capitalize()} mode) created and saved as {filename}.litematic successfully!", fg="#6c757d")
        else:
            status_label.config(text="Warning: Please select a directory and enter a filename.", fg="#f2545b")

    root = tk.Tk()
    root.title("ELITE HAXOR")
    root.configure(bg="#f0f4f8")
    root.resizable(False, False)

    # Logo
    script_dir = os.path.dirname(__file__)
    image_path = os.path.join(script_dir, "elite_haxor_logo.png")
    image = tk.PhotoImage(file=image_path)
    logo = tk.Label(root, image=image)
    logo.pack(padx=18, pady=(18, 0))

    # Directory selection
    directory_label = tk.Label(root, text="Schematics Directory:", font=("Helvetica", 12), bg="#f0f4f8", fg="#4a4e69")
    directory_label.pack(pady=(20, 5))

    directory_frame = tk.Frame(root, bg="#f0f4f8")
    directory_frame.pack(padx=20, pady=5, fill=tk.X)

    directory_entry = tk.Entry(directory_frame, width=62, font=("Helvetica", 11), bg="#e8eaf6", fg="#4a4e69", relief="flat", highlightthickness=1, highlightbackground="#d4e6f1")
    directory_entry.pack(side=tk.LEFT, padx=(0, 10), pady=5, ipady=4)

    browse_button = tk.Button(directory_frame, text=" ⌕ ", command=select_directory, font=("Helvetica", 11), bg="#d4e6f1", fg="#4a4e69", relief="flat", activebackground="#b3cde0", padx=10)
    browse_button.pack(side=tk.LEFT, padx=(0, 10), pady=5)

    checkmark_label = tk.Label(directory_frame, text="", font=("Helvetica", 14, "bold"), bg="#f0f4f8")
    checkmark_label.pack(side=tk.LEFT, pady=5)

    # Filename entry
    filename_frame = tk.Frame(root, bg="#f0f4f8")
    filename_frame.pack(pady=(10, 5))

    filename_label = tk.Label(filename_frame, text="Save As:", font=("Helvetica", 12), bg="#f0f4f8", fg="#4a4e69")
    filename_label.pack(side=tk.LEFT, padx=(0, 10))

    filename_entry = tk.Entry(filename_frame, width=25, font=("Helvetica", 11), bg="#e8eaf6", fg="#4a4e69", relief="flat", highlightthickness=1, highlightbackground="#d4e6f1")
    filename_entry.pack(side=tk.LEFT, padx=(0, 10), pady=5, ipady=4)

    # Mode selection
    mode_frame = tk.Frame(root, bg="#f0f4f8")
    mode_frame.pack(pady=(10, 5))

    mode_label = tk.Label(mode_frame, text="Select Mode:", font=("Helvetica", 12), bg="#f0f4f8", fg="#4a4e69")
    mode_label.pack(side=tk.LEFT, padx=(0, 10))

    mode_var = tk.StringVar(value="normal")
    normal_radio = tk.Radiobutton(mode_frame, text="Normal", variable=mode_var, value="normal", font=("Helvetica", 11), bg="#f0f4f8", fg="#4a4e69", selectcolor="#e8eaf6")
    normal_radio.pack(side=tk.LEFT, padx=(0, 10))

    sculpty_radio = tk.Radiobutton(mode_frame, text="Sculpty", variable=mode_var, value="sculpty", font=("Helvetica", 11), bg="#f0f4f8", fg="#4a4e69", selectcolor="#e8eaf6")
    sculpty_radio.pack(side=tk.LEFT, padx=(0, 10))

    # Buttons
    button_frame = tk.Frame(root, bg="#f0f4f8")
    button_frame.pack(pady=8)

    create_button = tk.Button(button_frame, text="Create Litematic", command=create_litematic_action, font=("Helvetica", 11), bg="#a3d39c", fg="white", relief="flat", activebackground="#86b08a", padx=20, pady=10)
    create_button.pack(side=tk.LEFT, padx=10)

    update_button = tk.Button(button_frame, text="Update Mapping", command=open_mapping_window, font=("Helvetica", 11), bg="#69bdd6", fg="white", relief="flat", activebackground="#3f7e91", padx=20, pady=10)
    update_button.pack(side=tk.LEFT, padx=10)

    exit_button = tk.Button(button_frame, text="Exit", command=root.quit, font=("Helvetica", 11), bg="#f2545b", fg="white", relief="flat", activebackground="#f0323e", padx=20, pady=10)
    exit_button.pack(side=tk.LEFT, padx=10)

    # Status label
    status_label = tk.Label(root, text="", fg="#4a4e69", bg="#f0f4f8", font=("Helvetica", 11))
    status_label.pack(pady=3)

    info_label = tk.Label(root, text="Code written and compiled by TreacherousDev. \nFor inquiries, message me:\nDiscord - treacherousdev\nEmail - treacherousdev@gmail.com", fg="#4a4e69", bg="#f0f4f8", font=("Helvetica", 8))
    info_label.pack(pady=(3, 18))

    root.mainloop()


# Example function to allocate memory in a target process
def allocate_memory_in_process(size):
    pid = get_pid()
    process_handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not process_handle:
        raise Exception("Failed to open the process")
    
    # Allocate memory (7 million bytes)
    allocated_memory = VirtualAllocEx(process_handle, None, size, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
    if not allocated_memory:
        raise ctypes.WinError(ctypes.get_last_error())
    
    # print(f"Allocated memory at address: {allocated_memory:#x}")
    return allocated_memory


if __name__ == "__main__":
    main()





