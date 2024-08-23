# SDCardBackup
 Automatically backup SD cards for Sony mirrorless cameras.

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
