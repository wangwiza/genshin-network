from definitions import DATA_DIR, XML_FILE

from bs4 import BeautifulSoup
import pandas as pd
import re
import html
import time


def get_genshin_soup():
    with open(DATA_DIR / XML_FILE, "r", encoding="utf8") as f:
        file = f.read()
    return BeautifulSoup(file, "lxml").find_all


def extract_all_characters(soup: BeautifulSoup):
    with open(f"{DATA_DIR}/characters.txt", "w", encoding="utf8") as f:
        for elem in soup(text=re.compile(r"{{Character Infobox")):
            page = elem.parent.parent.parent
            character_name = page.title.text
            if ":" not in character_name:
                f.write(f"{character_name}\n")


def extract_all_dialogue(soup: BeautifulSoup):
    with open(f"{DATA_DIR}/dialogues.txt", "w", encoding="utf8") as f:
        for elem in soup(text=re.compile(r"{{Dialogue Start}}")):
            conversations = re.findall(
                r"{{Dialogue Start}}(.+?){{Dialogue End}}", elem.text, re.DOTALL
            )
            for exchange in conversations:
                f.write(html.unescape(exchange))


def extract_all_dialogue_new():
    with open(f"{DATA_DIR}/{XML_FILE}", "r", encoding="utf8") as xml:
        with open(f"{DATA_DIR}/dialogues.txt", "w", encoding="utf8") as f:
            for line in xml:
                print(line)
            print("done.")


def clean_dialogues():
    with open(f"{DATA_DIR}/clean_dialogues.txt", "w") as clean_file:
        with open(f"{DATA_DIR}/dialogues.txt", "r") as dialogues:
            speaker_pattern = re.compile(r"'''(.+?):''' ")
            for line in dialogues:
                pass


if __name__ == "__main__":
    # soup = get_genshin_soup()
    # extract_all_dialogue(soup)
    extract_all_dialogue_new()
