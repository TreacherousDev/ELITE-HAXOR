from litemapy import Region, BlockState
import ctypes
from ctypes import wintypes
import psutil

# Yes, I had to do this all manually. 
# May you shed a tear for all the lost time, hope and sanity that went into making this switch table.
# The worst part is that it is not even remotely close to being complete. Wonderful :))
def convert_mc_id_to_cc_id(cc_id: str) -> str:
    cc_id = int(cc_id)
    match cc_id:
        case 0:
            return "minecraft:air"
        case 100:
            return "minecraft:dirt"
        case 101:
            return "minecraft:grass_block"
        case 105:
            return "minecraft:mud"
        case 106:
            return "minecraft:iron_ore"
        case 109:
            return "minecraft:sand"
        case 111:
            return "minecraft:cobblestone"
        case 112:
            return "minecraft:coal_ore"
        case 113:
            return "minecraft:sweet_berry_bush"
        case 116:
            return "minecraft:oxeye_daisy"
        case 117:
            return "minecraft:red_mushroom"
        case 119:
            return "minecraft:white_terracotta"
        case 120:
            return "minecraft:light_gray_terracotta"
        case 127:
            return "minecraft:dead_bush"
        case 133:
            return "minecraft:granite"
        case 138:
            return "minecraft:water"
        case 141:
            return "minecraft:pink_tulip"
        case 142:
            return "minecraft:red_tulip"
        case 143:
            return "minecraft:blue_orchid"
        case 144:
            return "minecraft:dandelion"
        case 145:
            return "minecraft:snow_block"
        case 146:
            return "minecraft:smooth_basalt"
        case 147:
            return "minecraft:packed_ice"
        case 217:
            return "minecraft:birch_fence"
        case 218:
            return "minecraft:azalea_leaves"
        case 219:
            return "minecraft:mycelium"
        case 220:
            return "minecraft:blackstone"
        case 221:
            return "minecraft:spruce_fence"
        case 222:
            return "minecraft:spruce_leaves"
        case 223:
            return "minecraft:dead_tube_coral_block"
        case 224:
            return "minecraft:oak_fence"
        case 225:
            return "minecraft:oak_leaves"
        case 226:
            return "minecraft:red_mushroom"
        case 227:
            return "minecraft:cactus"
        case 228:
            return "minecraft:lily_pad"
        case 229:
            return "minecraft:dark_oak_fence"
        case 230:
            return "minecraft:sculk"
        case 231:
            return "minecraft:soul_soil"
        case 233:
            return "minecraft:gold_ore"
        case 234:
            return "minecraft:spruce_leaves"
        case 235:
            return "minecraft:blue_ice"
        case 238:
            return "minecraft:sweet_berry_bush"
        case 239:
            return "minecraft:sweet_berry_bush"
        case 240:
            return "minecraft:lava"
        case 241:
            return "minecraft:sweet_berry_bush"
        case 242:
            return "minecraft:sweet_berry_bush"
        case 243:
            return "minecraft:sweet_berry_bush"
        case 244:
            return "minecraft:sweet_berry_bush"
        case 245:
            return "minecraft:sweet_berry_bush"
        case 246:
            return "minecraft:sweet_berry_bush"
        case 247:
            return "minecraft:sweet_berry_bush"
        case 248:
            return "minecraft:sweet_berry_bush"
        case 249:
            return "minecraft:jungle_fence"
        case 250:
            return "minecraft:jungle_leaves"
        case 251:
            return "minecraft:jungle_fence"
        case 302:
            return "minecraft:grass_block"
        case 303:
            return "minecraft:muddy_mangrove_roots"
        case 372:
            return "minecraft:skeleton_skull"
        case 373:
            return "minecraft:fern"
        case 390:
            return "minecraft:beehive"
        case 856:
            return "minecraft:sugar_cane"
        case _:
            return "minecraft:smooth_stone"

# Windows API bullshit
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
MAX_MODULE_NAME32 = 255
psapi = ctypes.WinDLL('psapi.dll')
kernel32 = ctypes.WinDLL('kernel32.dll')
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
    process_handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, pid)
    if not process_handle:
        raise Exception("Failed to open the process")
    
    # Write the bytes to memory region
    ctypes.windll.kernel32.WriteProcessMemory(process_handle, counter_memory_address, (ctypes.c_ubyte * 4)(0x00, 0x00, 0x00, 0x00), 4, None)
    ctypes.windll.kernel32.CloseHandle(process_handle)

# Grab the data of all non air blocks
# x, y, z, direction, sculpty variant, block id
def read_block_data() -> list:
    pid = get_pid()
    process_handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, pid)
    if not process_handle:
        raise Exception("Failed to open the process")
    
    # Get the value of counter varlable
    # This determines the size of the block data array
    counter_buffer = (ctypes.c_ubyte * 4)()
    ctypes.windll.kernel32.ReadProcessMemory(process_handle, counter_memory_address, counter_buffer, 4, None)
    data_length = ctypes.cast(counter_buffer, ctypes.POINTER(ctypes.c_uint32)).contents.value

    # Get the block data array of bytes
    blueprint_buffer = (ctypes.c_ubyte * data_length)()
    ctypes.windll.kernel32.ReadProcessMemory(process_handle, blueprint_memory_address, blueprint_buffer, data_length, None)
    ctypes.windll.kernel32.CloseHandle(process_handle)
    return list(blueprint_buffer)

# Inject bytes into targeted memory regions
def inject_game_code():
    pid = get_pid()
    process_handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, pid)
    if not process_handle:
        raise Exception("Failed to open the process")
    
    exe_address = get_base_address(pid, process_name)
    code_cave_1_buffer = (ctypes.c_ubyte * len(code_cave_1_in_bytes))(*code_cave_1_in_bytes)
    ctypes.windll.kernel32.WriteProcessMemory(process_handle, exe_address + code_cave_1_offset, code_cave_1_buffer, len(code_cave_1_in_bytes), None)
    function_jump_1_buffer = (ctypes.c_ubyte * len(function_jump_1_in_bytes))(*function_jump_1_in_bytes)
    ctypes.windll.kernel32.WriteProcessMemory(process_handle, exe_address + function_jump_1_offset, function_jump_1_buffer, len(function_jump_1_in_bytes), None)
    ctypes.windll.kernel32.WriteProcessMemory(process_handle, 0x09000000, (ctypes.c_byte * 10)(0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x63, 0x63, 0x63), 10, None)
    ctypes.windll.kernel32.CloseHandle(process_handle)

# User interface
# yes it's garbage atm stfu I am watching tkinter playlist
def display_menu():
    print("\nMenu:")
    print("1. Create Litematic ")
    print("2. Exit")

# A convenient package I stole from the internet that carried 99% of the work of this app
# @Litemapy
def create_litematic(schematic_directory):
    # Shortcut to create a schematic with a single region
    reg = Region(0, 0, 0, 100, 100, 100)
    schem = reg.as_schematic(name="Realm", author="TreacherousDev", description="Made with Litemapy")
    byte_data = read_block_data()

    chunk_size = 7
    # Iterate over the array in chunks of 7
    for i in range(0, len(byte_data), chunk_size):
        block_data = byte_data[i:i + chunk_size]
        # Terminate on end
        if len(block_data) > chunk_size:
            continue
        #T Translate bytes to Litematic format
        x = int(block_data[0])
        z = int(block_data[1])
        y = 99 - int(block_data[2])
        cc_id = (block_data[6] << 8) | block_data[5]
        mc_id = convert_mc_id_to_cc_id(cc_id)
        reg[x, y, z] = BlockState(mc_id)

    # Save the schematic
    print("done")
    reset_counter()
    schem.save(schematic_directory + "/EliteHaxor.litematic")
    print (schematic_directory + "/EliteHaxor.litematic")

process_name = "Cubic.exe"
blueprint_memory_address = 0x09000010
counter_memory_address = 0x09000000
code_cave_1_offset = 0x2EC321
code_cave_1_content = (
    "66 50 8A 46 02 3A 05 04 00 00 09 0F 8C 49 00 00 00 3A 05 07 00 00 09 0F 8F 3D 00 00 00 8A 46 04 "
    "3A 05 05 00 00 09 0F 8C 2E 00 00 00 3A 05 08 00 00 09 0F 8F 22 00 00 00 8A 46 06 3A 05 06 00 00 "
    "09 0F 8C 13 00 00 00 3A 05 09 00 00 09 0F 8F 07 00 00 00 66 58 E9 07 00 00 00 66 58 E9 66 00 00 "
    "00 66 52 66 51 88 E1 80 E1 F0 C0 E9 04 88 CA 66 59 66 50 66 25 FF 0F 66 3D 00 00 0F 84 42 00 00 "
    "00 53 51 B9 10 00 00 09 03 0D 00 00 00 09 0F B6 5E 02 88 19 0F B6 5E 04 88 59 01 0F B6 5E 06 88 "
    "59 02 0F B6 DA 88 51 03 0F B6 5E 11 88 59 04 66 89 41 05 C7 41 07 FF FF FF FF 83 05 00 00 00 09 "
    "07 59 5B 66 58 66 5A 66 89 06 C6 46 0C 00 E9 36 C5 DD FF"
    )
code_cave_1_in_bytes = [int(byte, 16) for byte in code_cave_1_content.split()]
function_jump_1_offset = 0xC8923
function_jump_1_content = ("E9 F9 39 22 00 66 90")
function_jump_1_in_bytes = [int(byte, 16) for byte in function_jump_1_content.split()]
#schematic_directory = "" #"C:/Users/adant/curseforge/minecraft/Instances/Litematica/schematics"


def main(): 
    inject_game_code()
    schematic_directory = input("Paste Minecraft Schematics directory below. \nEx: C:/Users/Adam/curseforge/minecraft/Instances/Litematica/schematics/ \nDirectory: ")
    while True:
        display_menu()
        choice = input("Choose an option: ")
        if choice == '1':
            create_litematic(schematic_directory)

        elif choice == '2':
            print("Program Terminated!")
            continue
    
if __name__ == "__main__":
    main()







