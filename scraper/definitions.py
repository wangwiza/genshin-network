from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
DUMP_URL = (
    "https://s3.amazonaws.com/wikia_xml_dumps/g/ge/gensinimpact_pages_current.xml.7z"
)
XML_FILE = Path(DUMP_URL).stem
