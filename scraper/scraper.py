from definitions import DATA_DIR, XML_FILE

from bs4 import BeautifulSoup
import pandas as pd
import re
import html


def get_genshin_soup():
    with open(DATA_DIR / XML_FILE, "r", encoding="utf8") as f:
        file = f.read()
    return BeautifulSoup(file, "lxml")


def extract_all_titles(soup: BeautifulSoup):
    with open(f"{DATA_DIR}/titles.txt", "w", encoding="utf8") as f:
        for elem in soup(text=re.compile(r"{{Dialogue Start}}")):
            page = elem.parent.parent.parent
            character_name = page.title.text
            f.write(f"{character_name}\n")


def extract_all_dialogue() -> str:
    """Extract all dialogue from the XML file and save it to a text file."""

    with open(f"{DATA_DIR}/{XML_FILE}", "r", encoding="utf8") as src, open(
        f"{DATA_DIR}/dialogues.txt", "w", encoding="utf8"
    ) as dst:
        isDialogue = False
        skipping = False
        for line in src:
            if "<title>" in line:
                skipping = any(x in line for x in ("User:", "File:", "Template:"))
                continue
            if skipping:
                continue
            if "{{Dialogue End}}" in line:
                dst.write("\n")
                isDialogue = False
            elif "{{Dialogue Start}}" in line:
                isDialogue = True
            elif isDialogue:
                dst.write(clean_dialogue_line(line))
                # dst.write(line)
            else:
                pass
        print("done.")
    return f"{DATA_DIR}/dialogues.txt"


def clean_dialogue_line(line: str) -> str:
    """Clean a line of dialogue from the XML file.

    Args:
        line (str): The line of dialogue to clean.

    Returns:
        The cleaned line of dialogue.
    """

    line = line.replace("{{MC|Lumine|Aether|mc=1}}", "Lumine").replace(
        "{{MC|m=Aether|f=Lumine}}", "Aether"
    )
    if "{{DIcon" in line:
        start = line.find("}}") + 2
        line_without_prefix = f"Aether: {line[start:]}"
    else:
        line_without_prefix = line[line.find("'''") :]
    unescaped_line = html.unescape(html.unescape(html.unescape(line_without_prefix)))
    clean_line = (
        unescaped_line.replace("'''", "")
        .replace("[[", "")
        .replace("]]", "")
        .replace("|", ", ")
    )
    return clean_line


if __name__ == "__main__":
    extract_all_dialogue()
    # soup = get_genshin_soup()
    # extract_all_titles(soup)
