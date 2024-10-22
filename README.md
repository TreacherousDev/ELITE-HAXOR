## ELITE HAXOR
### An Extraordinary Litematica Integrated, Translator Embedded, Highly Automated Xeroxer Of Realms
This program converts a Cubic Castles realm into a .litematic file that can be imported into Minecraft using the Litematica Mod. Works only on Windows OS 64-bit x86-64 systems.

## Prerequisites:
- Windows OS x86_64 64-bit w/ admin privileges
- Minecraft Java Edition
- Minecraft ModLoader client w/ Litematica
- Cubic Castles Steam Version

## Installation:
Look for the latest version from the link below and follow the instructions

https://github.com/TreacherousDev/ELITE-HAXOR/releases

## Setup and Usage
1. Launch Cubic Castles
2. Run the batch file included in the zip.
3. Once ELITE HAXOR is opened, select a file directory and enter file name. The file directory should be the schematics folder of the Litematica instance. ex: "C:/Users/adant/curseforge/minecraft/Instances/Litematica/schematics"
4. Click on "Create Litematic". You may need to relog in Cubic Castles if the realm is not yet loaded - a prompt will tell you if you need to.
5. Another window will pop up showing you all the block mappings of the blocks currently in the realm. You can edit this before saving.
6. Your litematica file will be created in a few moments. You can then head over to Minecraft and import it to the world.

## Sample Outputs
![image](https://github.com/user-attachments/assets/6d05b286-5e61-4122-9b26-4cdfbb49f124)
![image](https://github.com/user-attachments/assets/4d0052ce-e6ba-4f33-9209-a37920c77fb3)
![image](https://github.com/user-attachments/assets/1c5f899f-8fc1-4f21-9a36-6281a0ebac53)

## Building your own Version
### Prerequisites
You will need to install the latest version of Python, along with the follwing packages:
- Litemapy, Numpy, Ctypes, Psutil, Json, OS, Sys, Pyinstaller

### Setup
Clone the repository or download it as a ZIP and unpack.

Using file explorer, go to the root folder of the project and type `cmd` on the directory. This should open command prompt at this file location.

Type th e following command below and press enter:
```pyinstaller --onefile --noconsole --add-data "elite_haxor_logo.png;." --add-data "block_data.py;." --add-data "block_mappings.json;." Elite_Haxor.py```

Wait for the build to finish, and afterwards you can test your new build located inside the `dist` folder.
