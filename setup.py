import setuptools
import os
from _version import __version__ as version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = ""
with open("FlexibleDate/requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

requirements = requirements.split("\n")

def list_folders(directory: str) -> list:
    """Creates a list of all the folders in a directory.

    Args:
        directory (str): the directory to search

    Returns:
        list: A list of all the folders in the directory
    """
    folders = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path) and item != "__pycache__":
            folders.append(item_path)
    other_folders = [list_folders(item_path) for item_path in folders]
    for folder in other_folders:
        folders.extend(folder)
    return folders

folder_path = "FlexibleDate"
folders = list_folders(folder_path)
folders.append("FlexibleDate")
print(folders)

setuptools.setup(
    name='FlexibleDate',
    version=version,
    author='Record Linking Lab',
    author_email='recordlinkinglab@gmail.com',
    description='This is a library used to make fuzzy date comparisons.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/byuawsfhtl/FlexibleDate.git',
    project_urls = {
        "Bug Tracker": "https://github.com/byuawsfhtl/FlexibleDate/issues"
    },
    packages=folders,
    install_requires=requirements,
    package_data={"": ["*.json", "*.txt"]},
)