import os
import shutil

from config import settings


def file_collection(file_type, source, destination):
    """Collects files from source and copies them to destination.

    Args:
        source: Path to the source directory.
        destination: Path to the destination directory.

    Returns:
        A list of paths to the copied media files.
    """

    print("#", "-" * 80)
    print(f"Collecting {file_type} files from /{source} to /{destination} ...")

    media_files = []

    for root, dirs, files in os.walk(source):
        for file in files:
            media_files.append(os.path.join(root, file))

    for source_file in media_files:
        destination_file = f"{destination}/{'/'.join(source_file.split('/')[1:])}"
        destination_folder = "/".join(destination_file.split("/")[:-1])

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        print(f"collect_{file_type} : /{source_file} -> /{destination_file}...")
        shutil.copy(source_file, destination_file)

    return media_files


def collect_static_files():
    """Collects static files from source and copies them to destination.

    Returns:
        A list of paths to the copied static files.
    """

    return file_collection(
        file_type="static",
        source=f"{settings.STATIC_PATH}",
        destination=f"{settings.BUILD_PATH}/{settings.STATIC_PATH}",
    )


def collect_media_files():
    """Collects media files from source and copies them to destination.

    Returns:
        A list of paths to the copied media files.
    """

    return file_collection(
        file_type="media",
        source=f"{settings.MEDIA_PATH}",
        destination=f"{settings.BUILD_PATH}/{settings.MEDIA_PATH}",
    )
