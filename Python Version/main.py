import os
import subprocess
import urllib.request
import inquirer

APKTOOL_DIR = 'bin'
ORIGINAL_DIR = '1.Original_File'
DECOMPILE_DIR = '2.Decomple_File'
RECOMPILE_DIR = '3.Recomple_File'

APKTOOL_JAR_URL = 'bin/apktool.jar'
APKTOOL_BAT_URL = 'bin/apktool.bat'

APKTOOL_JAR_PATH = os.path.join(APKTOOL_DIR, 'apktool.jar')
APKTOOL_BAT_PATH = os.path.join(APKTOOL_DIR, 'apktool.bat')

def download_file(url, dest_path):
    if not os.path.exists(dest_path):
        print(f"Downloading {url} to {dest_path} ...")
        urllib.request.urlretrieve(url, dest_path)
        print(f"File {dest_path} downloaded successfully.")

def decompile_apk(apk_file):
    apk_name = os.path.splitext(os.path.basename(apk_file))[0]
    output_dir = os.path.join(DECOMPILE_DIR, apk_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    subprocess.run([APKTOOL_BAT_PATH, 'd', apk_file, '-o', output_dir, '-f'])

def recompile_apk(decompiled_dir):
    apk_name = os.path.basename(decompiled_dir)
    output_file = os.path.join(RECOMPILE_DIR, f'{apk_name}.apk')
    subprocess.run([APKTOOL_BAT_PATH, 'b', decompiled_dir, '-o', output_file])

os.makedirs(APKTOOL_DIR, exist_ok=True)
os.makedirs(ORIGINAL_DIR, exist_ok=True)
os.makedirs(DECOMPILE_DIR, exist_ok=True)
os.makedirs(RECOMPILE_DIR, exist_ok=True)

download_file(APKTOOL_JAR_URL, APKTOOL_JAR_PATH)
download_file(APKTOOL_BAT_URL, APKTOOL_BAT_PATH)

def print_ascii_art():
    green = '\033[92m'
    reset = '\033[0m'
    ascii_art = r'''
  ____         __    ___    ____   ____  _  _
 (_  _) ___   /__\  / __)  (  _ \ ( ___)( \/ )
  _)(_ (___) /(__)\ \__ \   )(_) ) )__)  \  / 
 (____)     (__)(__)(___/()(____/ (____)  \/  
================================================
Title   : Apktools - Decompiled & Recompiled Apk
Version : 1.0 (Python)
Site    : https://i-as.dev
Github  : https://github.com/fitri-hy/apktool
Creator : Fitri HY
================================================
    '''
    print(f"{green}{ascii_art}{reset}")
    
def main_menu():
    print_ascii_art()
    while True:
        apk_files = [f for f in os.listdir(ORIGINAL_DIR) if f.endswith('.apk')]

        menu_questions = [
            inquirer.List('action',
                          message="Select an action",
                          choices=['Decompile APK', 'Recompile APK', 'Exit'],
                          ),
        ]
        menu_answers = inquirer.prompt(menu_questions)

        if menu_answers['action'] == 'Decompile APK':
            if not apk_files:
                print("APK file is not available in the Original_File folder.")
            else:
                decompile_questions = [
                    inquirer.List('apk_file',
                                  message="Select APK file to decompile",
                                  choices=apk_files,
                                  ),
                ]
                decompile_answers = inquirer.prompt(decompile_questions)
                selected_apk = decompile_answers['apk_file']

                decompile_apk(os.path.join(ORIGINAL_DIR, selected_apk))
                print(f"File {selected_apk} decompiled successfully.")

        elif menu_answers['action'] == 'Recompile APK':
            decompiled_dirs = [f for f in os.listdir(DECOMPILE_DIR) if os.path.isdir(os.path.join(DECOMPILE_DIR, f))]
            if not decompiled_dirs:
                print("APK file is not available in the Decomple_File folder.")
            else:
                recompile_questions = [
                    inquirer.List('decompiled_dir',
                                  message="Select decompilated results to recompile",
                                  choices=decompiled_dirs,
                                  ),
                ]
                recompile_answers = inquirer.prompt(recompile_questions)
                selected_decompiled_dir = recompile_answers['decompiled_dir']

                recompile_apk(os.path.join(DECOMPILE_DIR, selected_decompiled_dir))
                print(f"Folder {selected_decompiled_dir} recompiled successfully.")

        elif menu_answers['action'] == 'Exit':
            print("Exit the program.")
            break

main_menu()
