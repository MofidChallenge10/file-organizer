#!/usr/bin/env python3
"""file-organizer: sort the files of a folder into sub-folders by file type."""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

__version__ = "0.1.0"

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".heic", ".tiff"},
    "Documents": {
        ".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".odt",
        ".xls", ".xlsx", ".csv", ".ppt", ".pptx",
    },
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "Video": {".mp4", ".mkv", ".avi", ".mov", ".webm", ".wmv"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".tgz"},
    "Code": {
        ".py", ".js", ".ts", ".html", ".css", ".json", ".java",
        ".c", ".cpp", ".go", ".rs", ".sh", ".yml", ".yaml",
    },
    "Installers": {".exe", ".msi", ".dmg", ".deb", ".rpm", ".apk", ".iso"},
}
OTHER = "Other"


def category_for(path: Path) -> str:
    """Return the category folder name for a file based on its extension."""
    ext = path.suffix.lower()
    for name, extensions in CATEGORIES.items():
        if ext in extensions:
            return name
    return OTHER


def unique_destination(dest: Path) -> Path:
    """Return a path that does not exist yet: 'a.txt' -> 'a (1).txt' -> 'a (2).txt'."""
    if not dest.exists():
        return dest
    stem, suffix = dest.stem, dest.suffix
    n = 1
    while True:
        candidate = dest.with_name(f"{stem} ({n}){suffix}")
        if not candidate.exists():
            return candidate
        n += 1


def plan(folder: Path) -> list[tuple[Path, Path]]:
    """List (source, destination) pairs for every visible file directly in `folder`."""
    moves = []
    for item in sorted(folder.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue
        moves.append((item, folder / category_for(item) / item.name))
    return moves


def organize(folder: Path, dry_run: bool = False) -> list[tuple[Path, Path]]:
    """Move files into category sub-folders. Nothing is touched when dry_run is True."""
    done = []
    for src, dest in plan(folder):
        dest = unique_destination(dest)
        if not dry_run:
            dest.parent.mkdir(exist_ok=True)
            shutil.move(str(src), str(dest))
        done.append((src, dest))
    return done


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="file-organizer",
        description="Organize the files of a folder into sub-folders by type.",
    )
    parser.add_argument("folder", nargs="?", default=".", help="folder to organize (default: current directory)")
    parser.add_argument("-n", "--dry-run", action="store_true", help="show what would happen without moving anything")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    folder = Path(args.folder).expanduser().resolve()
    if not folder.is_dir():
        print(f"Error: '{folder}' is not a directory", file=sys.stderr)
        return 1

    moves = organize(folder, dry_run=args.dry_run)
    if not moves:
        print("Nothing to organize.")
        return 0

    verb = "Would move" if args.dry_run else "Moved"
    for src, dest in moves:
        print(f"{verb}: {src.name} -> {dest.relative_to(folder)}")
    suffix = "would be organized" if args.dry_run else "organized"
    print(f"{len(moves)} file(s) {suffix}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
