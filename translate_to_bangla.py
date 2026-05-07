import os
from pathlib import Path
from translate import Translator

SRC_DIR = Path("docs")
TARGET_DIR = SRC_DIR / "bangla"
TARGET_DIR.mkdir(parents=True, exist_ok=True)

translator = Translator(to_lang="bn")  # Bengali

def translate_line(line: str) -> str:
    stripped = line.strip()
    # Preserve headings (lines starting with #) and code fences
    if stripped.startswith("#") or stripped.startswith("```") or "```" in stripped:
        return line
    # Translate non-empty lines
    if stripped:
        try:
            # Translate to Bengali
            translated = translator.translate(line)
            return translated + "\n"
        except Exception:
            # If translation fails, keep original line
            return line + "\n"
    # For empty lines, just return newline
    return "\n"

def translate_file(src_path: Path, dst_path: Path):
    with src_path.open("r", encoding="utf-8") as src_file, \
         dst_path.open("w", encoding="utf-8") as dst_file:
        for line in src_file:
            dst_file.write(translate_line(line))

if __name__ == "__main__":
    for md_path in SRC_DIR.glob("*.md"):
        if md_path.parent.name == "bangla":
            continue  # skip already translated files
        target_path = TARGET_DIR / md_path.name
        print(f"Translating {md_path} → {target_path}")
        translate_file(md_path, target_path)