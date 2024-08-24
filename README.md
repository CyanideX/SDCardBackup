# SDCardBackup
 Automatically backup SD cards for Sony mirrorless cameras.

 ![sdbackup_demo](https://github.com/user-attachments/assets/3445f857-5937-4d63-ad13-507aa9f38f31)

SD Card Backup utomatically detects Sony structured SD cards, prompts user for backup name, and copies images to user's photo folder and the videos to the user's videos folder.

- Files are copied into folders labelled with the backup name, date, and time.
- Files are verified after copy, including number of files and sizes.
- Storage space is checked before copying.
- Confirmation popup after process completes with total files copied.
- Log saved next to program.

 # Compiling source to EXE

Here's how you can do it:

### Step 1: Install PyInstaller
First, you need to install `PyInstaller`. You can do this using `pip`:

```bash
pip install pyinstaller
```

### Step 2: Compile the Script
Navigate to the directory where your script is located and run the following command:

```bash
pyinstaller --onefile --windowed sdbackup.py
```

- `--onefile`: This option packages everything into a single executable file.
- `--windowed`: This option prevents a console window from appearing when you run the executable (useful for GUI applications).

### Step 3: Locate the Executable
After running the command, `PyInstaller` will create a `dist` directory in the same location as your script. Inside this directory, you will find the `sdbackup.exe` file.

### Step 4: Run the Executable
You can now run the `sdbackupd.exe` file on any Windows machine.

### Additional Tips:
- **Dependencies**: `PyInstaller` should automatically include all necessary dependencies, but if you encounter any issues, you may need to specify additional options or include files manually.
