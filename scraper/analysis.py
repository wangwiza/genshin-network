from definitions import DATA_DIR
import json

with open(f"{DATA_DIR}/exchanges.json", mode="r+", encoding="utf-8") as f:
    exchanges = json.load(f)
    for speaker in exchanges:
        for mention in exchanges[speaker]:
            exchanges[speaker][mention] += 1
    json.dump(exchanges, f, ensure_ascii=True, indent=4)
