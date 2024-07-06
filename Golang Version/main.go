package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"github.com/AlecAivazis/survey/v2"
)

const (
	APKTOOL_DIR      = "bin"
	ORIGINAL_DIR     = "1.Original_File"
	DECOMPILE_DIR    = "2.Decomple_File"
	RECOMPILE_DIR    = "3.Recomple_File"
	APKTOOL_JAR_URL  = "bin/apktool.jar"
	APKTOOL_BAT_URL  = "bin/apktool.bat"
)

func downloadFile(url, destPath string) error {
	if _, err := os.Stat(destPath); os.IsNotExist(err) {
		fmt.Printf("Downloading %s to %s ...\n", url, destPath)
		resp, err := http.Get(url)
		if err != nil {
			return err
		}
		defer resp.Body.Close()
		out, err := os.Create(destPath)
		if err != nil {
			return err
		}
		defer out.Close()
		_, err = io.Copy(out, resp.Body)
		if err != nil {
			return err
		}
		fmt.Printf("File %s downloaded successfully.\n", destPath)
	}
	return nil
}

func decompileApk(apkFile string) error {
	apkName := strings.TrimSuffix(filepath.Base(apkFile), filepath.Ext(apkFile))
	outputDir := filepath.Join(DECOMPILE_DIR, apkName)
	if err := os.MkdirAll(outputDir, os.ModePerm); err != nil {
		return err
	}
	cmd := exec.Command(filepath.Join(APKTOOL_DIR, "apktool.bat"), "d", apkFile, "-o", outputDir, "-f")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	return cmd.Run()
}

func recompileApk(decompiledDir string) error {
	apkName := filepath.Base(decompiledDir)
	outputFile := filepath.Join(RECOMPILE_DIR, fmt.Sprintf("%s.apk", apkName))
	cmd := exec.Command(filepath.Join(APKTOOL_DIR, "apktool.bat"), "b", decompiledDir, "-o", outputFile)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	return cmd.Run()
}

func setupDirectories() error {
	dirs := []string{APKTOOL_DIR, ORIGINAL_DIR, DECOMPILE_DIR, RECOMPILE_DIR}
	for _, dir := range dirs {
		if err := os.MkdirAll(dir, os.ModePerm); err != nil {
			return err
		}
	}
	return nil
}

func printASCIIArt() {
	fmt.Println(`
  ____         __    ___    ____   ____  _  _
 (_  _) ___   /__\  / __)  (  _ \ ( ___)( \/ )
  _)(_ (___) /(__)\ \__ \   )(_) ) )__)  \  /
 (____)     (__)(__)(___/()(____/ (____)  \/  
================================================
Title   : Apktools - Decompiled & Recompiled Apk
Version : 1.0 (Golang)
Site    : https://i-as.dev
Github  : https://github.com/fitri-hy/apktool
Creator : Fitri HY
================================================
`)
}

func mainMenu() {
	printASCIIArt()
	for {
		files, _ := filepath.Glob(filepath.Join(ORIGINAL_DIR, "*.apk"))
		var action string
		prompt := &survey.Select{
			Message: "Select an action:",
			Options: []string{"Decompile APK", "Recompile APK", "Exit"},
		}
		survey.AskOne(prompt, &action)

		switch action {
		case "Decompile APK":
			if len(files) == 0 {
				fmt.Println("APK file is not available in the Original_File folder.")
			} else {
				var apkFile string
				prompt := &survey.Select{
					Message: "Select APK file to decompile:",
					Options: files,
				}
				survey.AskOne(prompt, &apkFile)

				err := decompileApk(apkFile)
				if err != nil {
					fmt.Printf("Error decompiling APK: %v\n", err)
				} else {
					fmt.Printf("File %s decompiled successfully.\n", filepath.Base(apkFile))
				}
			}

		case "Recompile APK":
			dirs, _ := filepath.Glob(filepath.Join(DECOMPILE_DIR, "*"))
			if len(dirs) == 0 {
				fmt.Println("APK file is not available in the Decomple_File folder.")
			} else {
				var decompiledDir string
				prompt := &survey.Select{
					Message: "Select decompiled results to recompile:",
					Options: dirs,
				}
				survey.AskOne(prompt, &decompiledDir)

				err := recompileApk(decompiledDir)
				if err != nil {
					fmt.Printf("Error recompiling APK: %v\n", err)
				} else {
					fmt.Printf("Folder %s recompiled successfully.\n", filepath.Base(decompiledDir))
				}
			}

		case "Exit":
			fmt.Println("Exit the program.")
			return
		}
	}
}

func main() {
	if err := setupDirectories(); err != nil {
		fmt.Printf("Error setting up directories: %v\n", err)
		return
	}

	if err := downloadFile(APKTOOL_JAR_URL, filepath.Join(APKTOOL_DIR, "apktool.jar")); err != nil {
		fmt.Printf("Error downloading apktool.jar: %v\n", err)
		return
	}

	if err := downloadFile(APKTOOL_BAT_URL, filepath.Join(APKTOOL_DIR, "apktool.bat")); err != nil {
		fmt.Printf("Error downloading apktool.bat: %v\n", err)
		return
	}

	mainMenu()
}
