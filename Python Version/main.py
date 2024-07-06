import os
import subprocess
import urllib.request
import inquirer
from pathlib import Path

APKTOOL_DIR = 'bin'
ORIGINAL_DIR = '1.Original_File'
DECOMPILE_DIR = '2.Decomple_File'
RECOMPILE_DIR = '3.Recomple_File'
KEYSTORE_DIR = '4.Keystore'
SIGNED_APK_DIR = '5.Signed_APK'

APKTOOL_JAR_URL = 'bin/apktool.jar'
APKTOOL_BAT_URL = 'bin/apktool.bat'
KEYSTORE_FILE = 'my-release-key.keystore'

APKTOOL_JAR_PATH = os.path.join(APKTOOL_DIR, 'apktool.jar')
APKTOOL_BAT_PATH = os.path.join(APKTOOL_DIR, 'apktool.bat')
KEYSTORE_PATH = os.path.join(KEYSTORE_DIR, KEYSTORE_FILE)
SIGNED_APK_PATH = os.path.join(SIGNED_APK_DIR)

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
    return output_file

def generate_keystore():
    if not os.path.exists(KEYSTORE_PATH):
        print(f"Generating keystore {KEYSTORE_FILE}...")
        subprocess.run([
            'keytool', '-genkey', '-v', '-keystore', KEYSTORE_PATH, '-alias', 'mykey', '-keyalg', 'RSA',
            '-keysize', '2048', '-validity', '10000', '-storepass', 'password', '-keypass', 'password'
        ])
        print(f"Keystore {KEYSTORE_FILE} generated successfully.")

def sign_apk(apk_file):
    signed_apk_file = os.path.join(SIGNED_APK_DIR, os.path.basename(apk_file))
    if not os.path.exists(SIGNED_APK_DIR):
        os.makedirs(SIGNED_APK_DIR)
    print(f"Signing APK {apk_file}...")
    subprocess.run([
        'jarsigner', '-verbose', '-sigalg', 'SHA1withRSA', '-digestalg', 'SHA1',
        '-keystore', KEYSTORE_PATH, '-storepass', 'password', '-keypass', 'password',
        apk_file, 'mykey'
    ])
    os.rename(apk_file, signed_apk_file)
    print(f"APK signed successfully. Signed APK is located at {signed_apk_file}.")
    return signed_apk_file

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
Version : 2.0 (Python)
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
                          choices=['Decompile APK', 'Recompile APK', 'Generate Keystore', 'Sign APK', 'Exit'],
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

                output_file = recompile_apk(os.path.join(DECOMPILE_DIR, selected_decompiled_dir))
                print(f"Folder {selected_decompiled_dir} recompiled successfully.")
                print(f"Recompiled APK is located at {output_file}.")

        elif menu_answers['action'] == 'Generate Keystore':
            generate_keystore()

        elif menu_answers['action'] == 'Sign APK':
            apks_to_sign = [f for f in os.listdir(RECOMPILE_DIR) if f.endswith('.apk')]
            if not apks_to_sign:
                print("No APKs available to sign in the Recompile_File folder.")
            else:
                sign_questions = [
                    inquirer.List('apk_file',
                                  message="Select APK file to sign",
                                  choices=apks_to_sign,
                                  ),
                ]
                sign_answers = inquirer.prompt(sign_questions)
                selected_apk = sign_answers['apk_file']

                signed_apk_path = sign_apk(os.path.join(RECOMPILE_DIR, selected_apk))
                print(f"Signed APK is located at {signed_apk_path}.")

        elif menu_answers['action'] == 'Exit':
            print("Exit the program.")
            break

if __name__ == '__main__':
    os.makedirs(APKTOOL_DIR, exist_ok=True)
    os.makedirs(ORIGINAL_DIR, exist_ok=True)
    os.makedirs(DECOMPILE_DIR, exist_ok=True)
    os.makedirs(RECOMPILE_DIR, exist_ok=True)
    os.makedirs(KEYSTORE_DIR, exist_ok=True)
    os.makedirs(SIGNED_APK_DIR, exist_ok=True)

    download_file(APKTOOL_JAR_URL, APKTOOL_JAR_PATH)
    download_file(APKTOOL_BAT_URL, APKTOOL_BAT_PATH)

    main_menu()
