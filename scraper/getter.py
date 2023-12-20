from definitions import ROOT_DIR, DATA_DIR
import os
import requests
import py7zr
from tqdm import tqdm

DUMP_URL = (
    "https://s3.amazonaws.com/wikia_xml_dumps/g/ge/gensinimpact_pages_current.xml.7z"
)


def download_file(url) -> str:
    response = requests.get(url, stream=True)
    filename = os.path.join(DATA_DIR, os.path.basename(DUMP_URL))
    response.raise_for_status()
    with tqdm.wrapattr(
        open(filename, "wb"),
        "write",
        miniters=1,
        desc=os.path.basename(filename),
        total=int(response.headers.get("content-length", 0)),
    ) as fout:
        for chunk in response.iter_content(chunk_size=8192):
            fout.write(chunk)
    return filename


def extract_7z_file(filename):
    with py7zr.SevenZipFile(filename, "r") as archive:
        print(f"Starting extraction of {filename}...")
        archive.extractall(DATA_DIR)
        print("Finished extraction.")


def main():
    filename = download_file(DUMP_URL)
    extract_7z_file(filename)


if __name__ == "__main__":
    main()
