from litemapy import Region, BlockState
import ctypes
from ctypes import wintypes
import psutil
import tkinter as tk
from tkinter import ttk, filedialog
import json
import os
import sys
from collections import Counter
from block_data import block_options, cc_block_name


block_options = sorted(block_options)

def get_mc_block_from_cc_id(cc_id: str, direction: str) -> BlockState:
    mc_id  = "minecraft:" + cc_to_mc_mapping.get(str(cc_id), "smooth_stone")
    mc_block = BlockState(mc_id, facing=direction, waterlogged="false")
    match mc_id:
        case "minecraft:air":
            mc_block = mc_block.with_properties(facing = None)
        case "minecraft:pointed_dropstone":
            mc_block = mc_block.with_properties(vertical_direction = "up")
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

block_list = {}

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

        # Build 2x2x2 chunk based on bit values of byte
        if all(bit == 0 for bit in sculpted_blocks):
            sculpted_blocks = [1] * 8
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

def allocate_memory_in_process(size):
    pid = get_pid()
    process_handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not process_handle:
        raise Exception("Failed to open the process")
    
    allocated_memory = VirtualAllocEx(process_handle, None, size, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
    if not allocated_memory:
        raise ctypes.WinError(ctypes.get_last_error())
    return allocated_memory

# Code Injection parameters
process_name = "Cubic.exe"
data_base_address = 0
blueprint_memory_address = 0
counter_memory_address = 0
# Static Variables Reference
variables_content = ("00 00 00 00 00 00 00 63 63 63")
# Function 1
code_cave_1_offset = 0x2ED4F7
code_cave_1_content = ""
function_jump_1_offset = 0xC8BE8
function_jump_1_content = ("E9 0A 49 22 00 66 90")
# Function 2
code_cave_2_offset = 0x2ED5E0 
code_cave_2_content = ""
function_jump_2_offset = 0x193E5F 
function_jump_2_content = ("E9 7C 97 15 00 66 90")
# Function 3
code_cave_3_offset = 0x2ED616
code_cave_3_content = ""
function_jump_3_offset = 0x1DAEE2
function_jump_3_content = ("E9 2F 27 11 00 90")

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
        "5B 66 58 66 5A 66 89 06 C6 46 0C 00 E9 25 B6 DD FF") 
    code_cave_2_content = ("C7 05 " + counter_addr + "00 00 00 00 83 4D FC FF 8D 4D AC E9 70 68 EA FF")
    code_cave_3_content = (
    "53 52 BB " + bp_addr +  "81 3B FF FF FF FF 0F 84 33 00 00 00 0F B6 13 3A 50 02 0F 85 22 "
    "00 00 00 0F B6 53 01 3A 50 04 0F 85 15 00 00 00 0F B6 53 02 3A 50 06 0F 85 08 00 00 00 "
    "88 4B 04 E9 05 00 00 00 83 C3 07 EB C1 5A 5B 88 48 11 8B 4D 08 E9 7F D8 EE FF")

cc_to_mc_mapping = {}
def main():
    manage_memory()
    inject_game_code()

      # Get the path to the directory where the script is located
    if getattr(sys, 'frozen', False):
        # If the script is bundled as an executable
        script_dir = os.path.dirname(sys.executable)
    else:
        # If running as a standard Python script
        script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the path to save the mapping preferences (in the same directory as the script/exe)
    mapping_file_path = os.path.join(script_dir, 'block_mappings.json')

    # Load the mapping initially when the program starts
    def load_mapping():
        if os.path.exists(mapping_file_path):
            with open(mapping_file_path, 'r') as f:
                return json.load(f)
        else:
            # If no saved mapping, return an empty dictionary
            return {}

    # Load previously saved mapping into a global variable
    global cc_to_mc_mapping
    cc_to_mc_mapping = load_mapping()

    def save_mapping():
        for key, value in cc_to_mc_mapping.items():
            if value in block_options:
                continue
            cc_to_mc_mapping[key] = "smooth_stone"
        # Save the current mapping to the file
        with open(mapping_file_path, 'w') as f:
            json.dump(cc_to_mc_mapping, f, indent=4)  # Use indent for readability


    def select_directory():
        directory = filedialog.askdirectory(title="Select Schematics Directory")
        if directory:
            directory_entry.delete(0, tk.END)
            directory_entry.insert(0, directory)
            checkmark_label.config(text="✓", fg="#a3d39c")

    combobox_mapping = {}

    def open_global_mapping_window():

        # Create a new window for updating the mapping
        mapping_window = tk.Toplevel(root)
        mapping_window.title("Update Mapping")
        mapping_window.configure(bg="#f0f4f8")
        mapping_window.geometry("600x720")
        mapping_window.resizable(False, False)

        def clear_search():
            search_entry.delete(0, tk.END)  # Clear the search entry
            search_items()  # Reset to show all items

        def load_visible_rows(page):
            # Clear all rows in the data_frame before adding new rows
            for widget in data_frame.winfo_children():
                widget.destroy()

            # Calculate start and end indices
            start = page * items_per_page
            end = min(start + items_per_page, len(filtered_items))

            # Create comboboxes for the current page
            for i in range(start, end):
                id_value, block_name = filtered_items[i]

                row_frame = tk.Frame(data_frame, bg="#f0f4f8")
                row_frame.pack(pady=5, padx=10, anchor='w')

                id_label = tk.Label(row_frame, text=f"{cc_block_name.get(int(id_value), 'Unknown')}:", 
                                    font=("Helvetica", 11), bg="#f0f4f8", fg="#4a4e69", width=30, anchor='w')
                id_label.pack(side=tk.LEFT, padx=5, anchor='w')

                combobox = ttk.Combobox(row_frame, values=block_options, font=("Helvetica", 11), state="normal", width=20)
                combobox.set(block_name)  # Set current block
                combobox.pack(side=tk.LEFT, padx=5)   

                # Store combobox reference
                combobox_mapping[id_value] = combobox
                
                # Bind the selection change to save the mapping
                combobox.bind("<<ComboboxSelected>>", lambda e, id_value=id_value: update_mapping_on_change(id_value))
                combobox.bind("<KeyRelease>",combobox_search, add="+") 
                combobox.bind("<KeyRelease>", lambda e, id_value=id_value: update_mapping_on_change(id_value), add="+")

        def update_page():
            # Load visible rows based on the current page
            load_visible_rows(current_page)
            total_pages = (len(filtered_items) + items_per_page - 1) // items_per_page  # Calculate total pages
            # Update button states
            prev_button.config(state=tk.NORMAL if current_page > 0 else tk.DISABLED)
            next_button.config(state=tk.NORMAL if current_page < total_pages - 1 else tk.DISABLED)

        def change_page(delta):
            nonlocal current_page
            current_page += delta
            update_page()

        def search_items(*args):
            nonlocal current_page
            search_term = search_entry.get().lower()  # Get the search term and convert to lowercase
            nonlocal filtered_items
            # Filter items based on search term
            filtered_items = [(id_value, block_name) for id_value, block_name in cc_to_mc_mapping.items()
                            if search_term in cc_block_name.get(int(id_value), '').lower()]

            current_page = 0  # Reset to first page after search
            update_page()  # Update the visible rows

                # Bind the search bar to call search_items when the text changes
        
                # Create a frame for the save and cancel buttons
        
        bottom_frame = tk.Frame(mapping_window, bg="#f0f4f8")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        # Exit button
        exit_button = tk.Button(bottom_frame, text="Exit", command=mapping_window.destroy,
                                font=("Helvetica", 10), bg="#f2545b", fg="white", relief="flat", activebackground="#f0323e", padx=8, pady=4)
        exit_button.pack(side=tk.RIGHT, padx=5)

        # Create a frame for the search bar
        search_frame = tk.Frame(mapping_window, bg="#f0f4f8")
        search_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 0))
        # Search bar
        search_label = tk.Label(search_frame, text="Search:", bg="#f0f4f8", fg="#4a4e69", font=("Helvetica", 11))
        search_label.pack(side=tk.LEFT)
        search_entry = tk.Entry(search_frame, width=56, font=("Helvetica", 11), bg="#e8eaf6", fg="#4a4e69", relief="flat", highlightthickness=1, highlightbackground="#d4e6f1")
        search_entry.pack(side=tk.LEFT, padx=5, pady=5, ipady=4)
        clear_search_button = tk.Button(search_frame, text=" X ", command=lambda: clear_search(),
                                        font=("Helvetica", 10), bg="#f2545b", fg="white", relief="flat", activebackground="#f0323e", padx=8, pady=3)
        clear_search_button.pack(side=tk.LEFT, padx=0)

        # Previous button
        prev_button = tk.Button(bottom_frame, text="Previous", command=lambda: change_page(-1),
                                font=("Helvetica", 10), bg="#a3d39c", fg="white", relief="flat", activebackground="#86b08a", padx=8, pady=4)
        prev_button.pack(side=tk.LEFT, padx=5)
        # Next button
        next_button = tk.Button(bottom_frame, text="Next", command=lambda: change_page(1),
                                font=("Helvetica", 10), bg="#a3d39c", fg="white", relief="flat", activebackground="#86b08a", padx=8, pady=4)
        next_button.pack(side=tk.LEFT, padx=5)

        # Create a frame for comboboxes
        data_frame = tk.Frame(mapping_window, bg="#f0f4f8")
        data_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Pagination variables
        items_per_page = 18  # Number of items to display per page
        current_page = 0  # Current page index
        filtered_items = list(cc_to_mc_mapping.items())  # Initialize with all items
        search_entry.bind("<KeyRelease>", search_items)
        # Load the initial rows
        update_page()

    def update_mapping_on_change(id_value):
        # Update the dictionary with the current selection from the combobox
        cc_to_mc_mapping[str(id_value)] = combobox_mapping[id_value].get()
        # Save the updated mapping to a file
        save_mapping()
        # Update the status in the main window
        status_label.config(text="Mapping updated and saved successfully!", fg="#6c757d")

    def update_mapping(combobox_mapping, mapping_window):
        # Update the dictionary with the current selection from comboboxes
        for id_value, combobox in combobox_mapping.items():
            cc_to_mc_mapping[str(id_value)] = combobox.get()

        # Save the updated mapping to a file
        save_mapping()

        # Update the status in the main window and close the update window
        status_label.config(text="Mapping updated and saved successfully!", fg="#6c757d")
        mapping_window.destroy()

    def combobox_search(event):
        combobox = event.widget  # Get the Combobox widget from the event
        value = combobox.get()
        if value == "":
            combobox['values'] = block_options  # Restore the full list when input is cleared
        else:
            query = [item for item in block_options if value.lower() in item.lower()]
            combobox['values'] = query  # Update the dropdown options

    def open_realm_block_mapping_window():
        chunk_size = 7
        byte_data = read_realm_data()
        blocks_in_realm = []
        for i in range(0, len(byte_data), chunk_size):
            block_data = byte_data[i:i + chunk_size]
            blocks_in_realm.append(int((block_data[6] << 8) | block_data[5]))
        block_id_count = dict(Counter(blocks_in_realm))
        block_id_count = dict(sorted(block_id_count.items(), key=lambda item: item[1], reverse=True))
        
        # Create a new window
        mapping_window = tk.Toplevel(root)
        mapping_window.title("Block ID Mapping")
        mapping_window.geometry("500x600")
        mapping_window.configure(bg="#f0f4f8")

        # Comboboxes to map each block ID to a Minecraft block
        combobox_mapping = {}

        # Create a frame for the mappings and a scrollbar
        canvas = tk.Canvas(mapping_window, bg="#f0f4f8", highlightthickness=0)
        scrollbar = tk.Scrollbar(mapping_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f4f8")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Display the block ID and count with a dropdown for each
        for block_id, count in block_id_count.items():
            row_frame = tk.Frame(scrollable_frame, bg="#f0f4f8")
            row_frame.pack(pady=5, padx=10)

            id_label = tk.Label(row_frame, text=f"({count}) {cc_block_name.get(int(block_id), "Unknown")}:", font=("Helvetica", 11), bg="#f0f4f8", fg="#4a4e69", width=20, anchor='w')
            id_label.pack(side=tk.LEFT, padx=5, anchor='w')

            combobox = ttk.Combobox(row_frame, values=block_options, font=("Helvetica", 11), state="normal", width=20)
            combobox.set(cc_to_mc_mapping.get(str(block_id), "smooth_stone"))  # Default to the first option
            combobox.pack(side=tk.LEFT, padx=5)
            combobox.bind("<KeyRelease>",combobox_search)      

            # Store the combobox in a dictionary with the block ID as the key
            combobox_mapping[block_id] = combobox
        # Save button to confirm selections
        save_button = tk.Button(mapping_window, text="Save and Create Litematic", command= lambda: on_save_and_create_litematic(combobox_mapping, mapping_window), bg="#a3d39c", fg="white", font=("Helvetica", 11), relief="flat")
        save_button.pack(pady=10)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def on_open_realm_block_mapping_window():
        schematic_directory = directory_entry.get()
        filename = filename_entry.get()

        if schematic_directory and filename:
            pid = get_pid()
            process_handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
            counter_buffer = read_memory(process_handle, counter_memory_address, 4)
            counter = ctypes.cast(counter_buffer, ctypes.POINTER(ctypes.c_uint32)).contents.value
            if counter == 0:
                status_label.config(text="Realm not loaded to memory. Please relog :)", fg="#f2545b")
                return
            open_realm_block_mapping_window()
        else:
            status_label.config(text="Warning: Please select a directory and enter a filename.", fg="#f2545b")

    def on_save_and_create_litematic(combobox_mapping, mapping_window):
        update_mapping(combobox_mapping, mapping_window)
        create_litematic_action()

    def create_litematic_action():
        schematic_directory = directory_entry.get()
        filename = filename_entry.get()
        mode_selected = mode_var.get()   
        if mode_selected == "normal":
                create_litematic(schematic_directory, filename)
        elif mode_selected == "sculpty":
            create_litematic_pixel(schematic_directory, filename)
        status_label.config(text=f"Litematic ({mode_selected.capitalize()} mode) created and saved as {filename}.litematic successfully!", fg="#6c757d")


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

    create_button = tk.Button(button_frame, text="Create Litematic", command=on_open_realm_block_mapping_window, font=("Helvetica", 11), bg="#a3d39c", fg="white", relief="flat", activebackground="#86b08a", padx=20, pady=10)
    create_button.pack(side=tk.LEFT, padx=10)

    update_button = tk.Button(button_frame, text="Update Mapping", command=open_global_mapping_window, font=("Helvetica", 11), bg="#69bdd6", fg="white", relief="flat", activebackground="#3f7e91", padx=20, pady=10)
    update_button.pack(side=tk.LEFT, padx=10)

    exit_button = tk.Button(button_frame, text="Exit", command=root.quit, font=("Helvetica", 11), bg="#f2545b", fg="white", relief="flat", activebackground="#f0323e", padx=20, pady=10)
    exit_button.pack(side=tk.LEFT, padx=10)

    # Status label
    status_label = tk.Label(root, text="", fg="#4a4e69", bg="#f0f4f8", font=("Helvetica", 11))
    status_label.pack(pady=3)

    info_label = tk.Label(root, text="Code written and compiled by TreacherousDev. \nFor inquiries, message me:\nDiscord - treacherousdev\nEmail - treacherousdev@gmail.com", fg="#4a4e69", bg="#f0f4f8", font=("Helvetica", 8))
    info_label.pack(pady=(3, 18))

    root.mainloop()


if __name__ == "__main__":
    main()

# to build: 
# pyinstaller --onefile --noconsole --add-data "elite_haxor_logo.png;." --add-data "block_data.py;." --add-data "block_mappings.json;." Elite_Haxor.py


