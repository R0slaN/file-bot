import os
import os.path
import pathlib
import shutil

import multivolumefile
import py7zr


def compress(file_path: pathlib.Path, volume_size: int = 26214400):
    filters = [{"id": py7zr.FILTER_COPY}]

    if os.path.exists(file_path):
        name = pathlib.PurePath(file_path).name
        archive_path = os.path.abspath("archives")

        os.mkdir(os.path.join(archive_path, name))
        with multivolumefile.open(
            f"archives\\{name}\\{name}.7z", mode="wb", volume=volume_size
        ) as split:
            with py7zr.SevenZipFile(split, "w", filters=filters) as archive:
                archive.writeall(path=file_path, arcname=name)
        return name


def decompress(name):
    archive_path = os.path.abspath("archives")
    archive_location = os.path.join(archive_path, name)

    if os.path.exists(archive_location):
        filenames = os.listdir(archive_location)

        with open(f"combined\\{name}.7z", "ab") as outfile:
            for fname in filenames:
                with open(os.path.join(archive_location, fname), "rb") as infile:
                    outfile.write(infile.read())


def clean():
    shutil.rmtree("temp")
    shutil.rmtree("archives")
    os.mkdir("temp")
    os.mkdir("archives")

# compress("E:\\Users\\RSLN\\Downloads\\Dolphin-x64\\")
# decompress("Dolphin-x64")
