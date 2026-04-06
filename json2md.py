from pathlib import Path
import json
from utils import json_to_markdown

if __name__ == "__main__":
    # save json to md
    input_path = Path("rest/Unternehmen_0.json")
    output_path = input_path.with_suffix(".md")

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    markdown = json_to_markdown(data)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Saved to {output_path}")