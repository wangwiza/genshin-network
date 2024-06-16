from definitions import DATA_DIR, DUMP_URL
from pathlib import Path
import requests
import py7zr
from tqdm import tqdm


def download_file(url: str) -> Path:
    """Download a file from the given URL and save it to the data directory.

    Args:
        url (str): The URL of the file to download.

    Returns:
        The path to the downloaded file.
    """

    response = requests.get(url, stream=True)
    filename = DATA_DIR / url.split("/")[-1]
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    response.raise_for_status()
    with tqdm.wrapattr(
        open(filename, "wb"),
        "write",
        miniters=1,
        desc=filename.name,
        total=int(response.headers.get("content-length", 0)),
    ) as fout:
        for chunk in response.iter_content(chunk_size=8192):
            fout.write(chunk)
    return filename


def extract_7z_file(filename):
    """Extract a 7z file to the data directory.

    Args:
        filename (Path): The path to the 7z file.
    """

    with py7zr.SevenZipFile(filename, "r") as archive:
        print(f"Starting extraction of {filename}...")
        archive.extractall(DATA_DIR)
        print("Finished extraction.")


def main():
    filename = download_file(DUMP_URL)
    extract_7z_file(filename)


if __name__ == "__main__":
    main()
