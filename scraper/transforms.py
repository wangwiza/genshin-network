import spacy
import json
from definitions import DATA_DIR
from spacy.tokens import Doc
from definitions import DATA_DIR, XML_FILE

from bs4 import BeautifulSoup
import pandas as pd
import re
import html
import os


def extract_all_dialogue_alt() -> str:
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
            else:
                pass
        print("done.")
    return f"{DATA_DIR}/dialogues.txt"


def extract_all_dialogue() -> str:
    """Extract all dialogue from the XML file and save it to a text file.

    Returns:
        str: The path to the saved dialogue text file.
    """

    # Corrected regular expression pattern
    dialogue_pattern = re.compile(
        r"""
    ^:+             # Starts with one or more colons
    (
        {{DIcon.*?}}.* |    # Matches {{DIcon}} followed by the rest of the text till newline
        (?:{{.*?}}\ )?      # Matches optional voice tag {{ }}
        '''[^:]+:''' .*       # Matches '''Name:''' where Name can be any characters name
    )
    """,
        re.VERBOSE,
    )

    try:
        with open(f"{DATA_DIR}/{XML_FILE}", "r", encoding="utf8") as src, open(
            f"{DATA_DIR}/dialogues.txt", "w", encoding="utf8"
        ) as dst:
            for line in src:
                if dialogue_pattern.match(line):
                    dst.write(clean_dialogue_line(line))
        print("Dialogue extraction complete.")
        return f"{DATA_DIR}/dialogues.txt"

    except FileNotFoundError:
        print(f"File not found: {DATA_DIR}/{XML_FILE}")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


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


def count_character_exchanges_in_dialogues():
    # Load English tokenizer, tagger, parser and NER
    nlp = spacy.load("en_core_web_trf")
    exchanges = {}
    with open(f"{DATA_DIR}/dialogues.txt", encoding="utf8") as dialogues:
        for line in dialogues:
            if not line.strip():
                continue
            doc = nlp(line)
            if not doc.ents:
                continue
            speaker = doc.ents[0].text
            if speaker not in exchanges:
                exchanges[speaker] = {}
            for entity in doc.ents[1:]:
                if entity.label_ == "PERSON":
                    exchanges[speaker][entity.text] = (
                        exchanges[speaker].get(entity.text, 0) + 1
                    )
    with open(f"{DATA_DIR}/exchanges.json", "w", encoding="utf8") as f:
        json.dump(exchanges, f, indent=4)
