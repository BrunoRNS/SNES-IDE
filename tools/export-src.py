from pathlib import Path
import time
import shutil
from zipfile import ZipFile

def get_executable_path():
    if getattr(sys, 'frozen', False):
        # PyInstaller executable
        print("executable path mode chosen")
        return str(os.path.dirname(sys.executable))
    else:
        # Normal script
        print("Python script path mode chosen")
        return str(os.path.dirname(os.path.abspath(__file__)))

try:
    # here, you select the SMC file
    print(r"Write down the FULL PATH of your SFC file '\\' in Windows systems")
    smc_file_path: Path = Path(input())

    # The path with the exporting DLLs
    exporting_path: Path = Path(get_executable_path()).parent / "libs" / "export"

    # Downloads Path:
    downloads_path: Path = Path.home() / "Downloads"

    # If the Exporting Path doesn't exists
    if not exporting_path.exists():
        # Raise an Error
        raise Exception("Exporting DLLs not found in libs directory!!")
    
    # If the Rom Path and File doesn't exists
    if not smc_file_path.exists():
        # Raise an Error
        raise Exception("The Path or the rom file does not exists...")

    # If the Rom Path doesn't indicate a file
    if not smc_file_path.is_file():
        # Raise an Error
        raise Exception("This is not a File, try again and send a true file.")

    # Verify if it is a SMC ROM, SFC Roms are not supported
    if smc_file_path.suffix.lower() != '.sfc':
        # Raise an Error
        raise Exception("This is not a SFC ROM, please select a SFC ROM.")
    
    # Choose a platform:
    print(f'Choose a platform for this ROM \n\n  ps2 \n\n  ps3-fw1.9 \n\n  ps3-fw3.4 \n\n  ps3-cfw3.55 \n\n  xboxone \n\n  windows32 \n\n  windows64 \n\n  MacOS \n\n  windowsARM \n\n  IOS \n\n  Android \n\n  WEB(low speed, recommended for small games only) \n\n\n ALERT! CASE SENSITIVE \n')
    platform: str = input()

    # Verify the platform and execute a different code for each one
    if platform == "ps2":
        print("PS2 platform selected.")
        # Wait a few seconds to continue
        time.sleep(2)

        # Define the file names for PS2 related files
        arquivos_ps2: tuple[Path] = (exporting_path / "ps2-1.dll", exporting_path / "ps2-2.dll")
        # Set the path for the ELF file, renaming it accordingly
        elf_path: Path = downloads_path / ('SNES_EMU' + '.ELF')
        # Set the path for the CNF file, renaming it accordingly
        cnf_path: Path = downloads_path / ('SYSTEM' + '.CNF')
        # Copy the first PS2 related file and rename it to ELF
        shutil.copy(arquivos_ps2[0], elf_path)
        # Copy the second PS2 related file and rename it to CNF
        shutil.copy(arquivos_ps2[1], cnf_path)

        # Create the ZIP archive
        with ZipFile(downloads_path / 'game.zip', 'w') as zipf:
            # Write the ELF file to the ZIP
            zipf.write(elf_path, elf_path.name)
            # Write the CNF file to the ZIP
            zipf.write(cnf_path, cnf_path.name)
            # Write the SMC file to the ZIP
            zipf.write(smc_file_path, smc_file_path.name)

        # Remove the temporary files (ELF and CNF)
        elf_path.unlink()
        cnf_path.unlink()
        
    # The following blocks are similar for each platform, so comments will be generalized
    elif platform.startswith("ps3"):
        print(f"PS3 firmware {platform.split('-')[-1]} platform selected.")
        # Wait a few seconds to continue
        time.sleep(2)

        # Copy the PKG and TXT files to the 'downloads' folder and rename them
        pkg_file: Path = exporting_path / f"{platform}.dll"
        pkg_path: Path = downloads_path / (pkg_file.stem + '.pkg')
        shutil.copy(pkg_file, pkg_path)

        info_file: Path = exporting_path / "ps3-inf.dll"
        info_path: Path = downloads_path / (info_file.stem + '.txt')
        shutil.copy(info_file, info_path)

        # Create the ZIP archive
        with ZipFile(downloads_path / 'game.zip', 'w') as zipf:
            # Write the TXT and PKG files to the ZIP
            zipf.write(info_path, info_path.name)
            zipf.write(pkg_path, pkg_path.name)
            # Write the SMC file to the ZIP
            zipf.write(smc_file_path, smc_file_path.name)

        # Remove the temporary files (TXT and PKG)
        pkg_path.unlink()
        info_path.unlink()

    # The following blocks handle other platforms that involve similar steps of copying and renaming files
    elif platform == "xboxone":
        print("XBOX ONE platform selected.")
        # Wait a few seconds to continue
        time.sleep(2)

        # Instructions for playing the game on XBOX ONE
        print("To play your game on XBOX ONE follow these steps: \n\n1: Download Internet Browser from Microsoft Store\n\n2: Open the OneDrive of your XBOX account and add the SMC ROM in any folder you want\n\n3: Open Internet Browser and go to this website: https://nesbox.com/embed\n\n4: Click on the canvas and press A button\n\n5: Login to OneDrive and open files from OneDrive\n\n6: Select the game, it should work at highest speed ever and HD resolution.\n\n7: For more details: nesbox.com\n")

        # End the script with a message for the user
        raise Exception("\n\nHave Fun!")

    # The following blocks handle Windows and MacOS platforms
    elif platform in ["windows32", "windows64", "MacOS", "windowsARM", "IOS"]:
        print(f"{platform} platform selected.")
        # Wait a few seconds to continue
        time.sleep(2)

        # Define the archive path based on the platform
        archive: Path = exporting_path / f"{platform}.dll"
        
        # Copy and rename the archive to ZIP
        zip_path: Path = downloads_path / ('game' + '.zip')
        shutil.copy(archive, zip_path)
        
        # Add the SMC file to the ZIP archive
        with ZipFile(zip_path, 'a') as zipf:
            zipf.write(smc_file_path, smc_file_path.name)

      
    elif platform == "Android":
        print("Android platform selected. Android 2.0+ supported...")
        # Wait a few seconds to continue
        time.sleep(2)

        archieve: Path = exporting_path / "apk_android_2.dll"
        
        zip_path = downloads_path / 'game.zip'
        with ZipFile(zip_path, 'w') as zipf:
            # rename the archieve to it's original name
            original_path = downloads_path / (archieve.stem + '.apk')
            shutil.copy(archieve, original_path)
            # Add files to zip compact folder
            zipf.write(original_path, original_path.name)
            zipf.write(smc_file_path, smc_file_path.name)

            # remove the temporary files
            original_path.unlink()
        
    elif platform == "WEB":
        print("WEB platform selected, atention! only for small games, big games usually don't have the same speed compared to others platforms.")
        # Wait a few seconds to continue
        time.sleep(2)

        # Dll path
        archieve: Path = exporting_path / "4web.dll"
        
        # copy and rename to zip
        zip_path: Path = downloads_path / ('game' + '.zip')
        shutil.copy(archieve, zip_path)
        
        # Add SMC to Zip file
        with ZipFile(zip_path, 'a') as zipf:
            zipf.write(smc_file_path, "main.sfc")

        
    else:
        raise Exception("Atention to case sensitive! The platform above isn't supported")

    # Finish Program
    raise Exception("Program Finished Succesfully, see your zip in downloads folder")

    

except Exception as e:
    # Print the Error or Returning comment
    print(e)
finally:
    # Wait the User to read the error to exit
    input("Press any key to exit...")
