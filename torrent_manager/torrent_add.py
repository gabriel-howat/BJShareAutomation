from qbittorrent import Client
from torrent_manager.disk_manager import get_drive_with_free_space
import os
import bencodepy
import re

directory = "C:\\BJ\\"


qb = Client('http://localhost:8080/')
qb.login('admin', 'Howat@123')

torrent_file_path = "C:\\BJ\\RACE.2023.S01.HDR.2160p.WEB.h265-EDITH.torrent"


def run_torrents_add():
    for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)):
                if filename.endswith(".torrent"):
                    file = directory + filename
                    torrent_file = open(file, 'rb')
                    print(" ")
                    print("File: " + file)
                    file_size = get_total_download_size2(file)
                    print("File size: " + str(round(file_size / (1024 ** 3), 2)) + " GB")
                    drive = get_drive_with_free_space(file_size=file_size, margin=1024*512)
                    print("Download no drive: " + drive)
                    if drive != "0":
                        qb.download_from_file(torrent_file, save_path=f"{drive}Downloads")


def get_total_download_size(torrent_file):
    with open(torrent_file, "rb") as file:
        data = bencodepy.decode(file.read())

    # Check if 'info' key exists in the decoded data
    if "info" in data:
        info = data["info"]

        # Check if 'length' key exists for single file torrents
        if "length" in info:
            return info["length"]

        # Calculate total size for multi-file torrents
        if "files" in info:
            return sum(file["length"] for file in info["files"])

    return 0

def get_total_download_size2(torrent_file):
    with open(torrent_file, "r", encoding="latin-1") as file:
        content = file.read()

    # Find the start and end positions of the "length" field
    lengths = re.findall(r"6:lengthi(\d+)e", content)
    if lengths:
        total_size_bytes = sum(int(length) for length in lengths)
    else:
        raise ValueError("Unable to find any 'length' fields in the torrent file.")



    #total_size_gb = total_size_bytes / (1024 ** 3)

    return total_size_bytes

if __name__ == "__main__":
    run_torrents_add()