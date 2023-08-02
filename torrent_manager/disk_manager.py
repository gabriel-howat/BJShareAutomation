import psutil
import random

previous_drive = None
ongoing_torrents = {}

def get_free_space(disk):
    disk_usage = psutil.disk_usage(disk)
    free_space = disk_usage.free
    return free_space

def get_available_drives():
    partitions = psutil.disk_partitions()
    drives = [partition.device for partition in partitions if partition.fstype]
    return drives

def get_drive_with_free_space(file_size, filename="", margin=0):
    global previous_drive

    #drives = [get_available_drives()]
    drives = ["D:\\", "E:\\", "F:\\", "G:\\", "H:\\", "I:\\"]

    if previous_drive:
        drives.remove(previous_drive)

    available_drives = []
    for drive in drives:
        disk_usage = psutil.disk_usage(drive)

        ongoing_torrents_drive = ongoing_torrents.get(drive, {})
        ongoing_torrents_size = sum(ongoing_torrents_drive.values())

        free_space = disk_usage.free - ongoing_torrents_size
        if free_space >= (file_size + margin):
            available_drives.append(drive)

    if not available_drives:
        print("No drives with sufficient free space found")
        return "0"

    selected_drive = random.choice(available_drives)
    previous_drive = selected_drive

    ongoing_torrents_drive = ongoing_torrents.get(selected_drive, {})
    ongoing_torrents_drive[filename] = file_size
    ongoing_torrents[selected_drive] = ongoing_torrents_drive

    return selected_drive