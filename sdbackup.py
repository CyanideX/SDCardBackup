import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter.ttk import Progressbar
import getpass
import logging

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def get_free_space(folder):
    total, used, free = shutil.disk_usage(folder)
    return free

def backup_sd_card(sd_card_path, pictures_backup_path, videos_backup_path, backup_name):
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder_name = f"{backup_name}_{current_datetime}"

    dcim_source = os.path.join(sd_card_path, "DCIM")
    clip_source = os.path.join(sd_card_path, "PRIVATE", "M4ROOT", "CLIP")
    sub_source = os.path.join(sd_card_path, "PRIVATE", "M4ROOT", "SUB")

    pictures_destination = os.path.join(pictures_backup_path, backup_folder_name)
    videos_destination = os.path.join(videos_backup_path, backup_folder_name)

    total_files = count_files(dcim_source) + count_files(clip_source) + count_files(sub_source)
    total_size = get_directory_size(dcim_source) + get_directory_size(clip_source) + get_directory_size(sub_source)
    free_space = get_free_space(pictures_backup_path)

    if total_size > free_space:
        messagebox.showerror("Insufficient Space", "There is not enough free space to complete the backup.")
        logging.error("Insufficient space for backup.")
        return

    sd_card_files = get_all_files(dcim_source) | get_all_files(clip_source) | get_all_files(sub_source)
    auto_dump_files = get_all_files(pictures_backup_path) | get_all_files(videos_backup_path)

    existing_files_detected = sd_card_files & auto_dump_files
    if existing_files_detected:
        response = messagebox.askyesnocancel("Files Already Exist", "Some files already exist in the backup directory. Do you want to continue? (Yes: Copy all files, No: Copy only new files, Cancel: Cancel backup)")
        if response is None:
            logging.info("Backup cancelled by user due to existing files.")
            return
        elif not response:
            copy_only_new_files = True
        else:
            copy_only_new_files = False
    else:
        copy_only_new_files = False

    os.makedirs(pictures_destination, exist_ok=True)
    os.makedirs(videos_destination, exist_ok=True)

    progress_bar['maximum'] = total_files
    progress_bar['value'] = 0

    try:
        photo_files_copied = copy_directory(dcim_source, pictures_destination, copy_only_new_files, auto_dump_files)
        video_files_copied = copy_directory(clip_source, os.path.join(videos_destination, "CLIP"), copy_only_new_files, auto_dump_files)
        video_files_copied += copy_directory(sub_source, os.path.join(videos_destination, "SUB"), copy_only_new_files, auto_dump_files)

        if verify_backup(dcim_source, pictures_destination) and verify_backup(clip_source, os.path.join(videos_destination, "CLIP")) and verify_backup(sub_source, os.path.join(videos_destination, "SUB")):
            messagebox.showinfo("Backup Complete", f"All files have been backed up and verified successfully.\n\nPhotos backed up: {photo_files_copied}\nVideos backed up: {video_files_copied}", parent=root)
            logging.info("Backup completed successfully.")
        else:
            messagebox.showwarning("Backup Incomplete", "Some files were not backed up correctly.", parent=root)
            logging.warning("Backup incomplete. Some files were not backed up correctly.")
    except Exception as e:
        messagebox.showerror("Backup Failed", f"An error occurred during the backup: {e}", parent=root)
        logging.error(f"Backup failed: {e}")

    start_button.config(text="Done", state=tk.DISABLED)
    root.after(1000, root.destroy)

def count_files(directory):
    file_count = 0
    for root, dirs, files in os.walk(directory):
        file_count += len(files)
    return file_count

def get_directory_size(directory):
    total_size = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            total_size += os.path.getsize(os.path.join(root, file))
    return total_size

def get_all_files(directory):
    files_set = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            files_set.add(file)
    return files_set

def copy_directory(source, destination, copy_only_new_files, existing_files):
    files_copied = 0
    if os.path.exists(source):
        for root, dirs, files in os.walk(source):
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(destination, os.path.relpath(src_file, source))
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                if not copy_only_new_files or file not in existing_files:
                    shutil.copy2(src_file, dst_file)
                    progress_bar['value'] += 1
                    progress_bar.update()
                    files_copied += 1
        print(f"Copied {source} contents to {destination}")
        logging.info(f"Copied {source} contents to {destination}")
    else:
        print(f"Folder not found at {source}")
        logging.warning(f"Folder not found at {source}")
    return files_copied

def verify_backup(source, destination):
    for root, dirs, files in os.walk(source):
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(destination, os.path.relpath(src_file, source))
            if not os.path.exists(dst_file) or os.path.getsize(src_file) != os.path.getsize(dst_file):
                return False
    return True

def find_sd_card():
    drives = [f"{chr(x)}:\\" for x in range(65, 91) if os.path.exists(f"{chr(x)}:\\")]
    for drive in drives:
        avf_info_exists = os.path.exists(os.path.join(drive, "AVF_INFO"))
        dcim_exists = os.path.exists(os.path.join(drive, "DCIM"))
        private_exists = os.path.exists(os.path.join(drive, "PRIVATE"))
        
        if avf_info_exists and (dcim_exists or private_exists):
            return drive
    return None

def start_backup():
    sd_card_path = find_sd_card()
    if sd_card_path:
        print(f"Detected SD card at {sd_card_path}")
        backup_name = simpledialog.askstring("Backup Name", "Enter a name for the backup:", parent=root)
        if backup_name:
            backup_name = backup_name.replace(" ", "-")
            backup_sd_card(sd_card_path, pictures_backup_path, videos_backup_path, backup_name)
        else:
            messagebox.showwarning("No Backup Name", "No backup name provided. Backup cancelled.", parent=root)
    else:
        messagebox.showwarning("No SD Card Found", "No SD card with the required folders found.", parent=root)

# Automatically detect the user's folder for storing backups
username = getpass.getuser()
pictures_backup_path = os.path.join(f"C:\\Users\\{username}\\Pictures\\AUTO_DUMP")
videos_backup_path = os.path.join(f"C:\\Users\\{username}\\Videos\\AUTO_DUMP")

# Set up logging
logging.basicConfig(filename='backup_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create the GUI
root = tk.Tk()
root.title("SD Card Backup")

# Set window dimensions
window_width = 400
window_height = 120
center_window(root, window_width, window_height)

progress_bar = Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=20, padx=40)

start_button = tk.Button(root, text="Start Backup", command=start_backup)
start_button.pack(pady=10)

root.mainloop()
