<p align="center">
  <img src="assets/banner.svg" alt="file-organizer" width="100%"/>
</p>

# file-organizer

A tiny, zero-dependency Python CLI that cleans up a messy folder (hello, `Downloads`) by sorting files into sub-folders by type.

- No dependencies, only the Python standard library (3.8+)
- `--dry-run` shows exactly what would happen before anything moves
- Never overwrites: name collisions become `name (1).ext`
- Skips hidden files and existing folders

## Install

```bash
git clone https://github.com/MofidChallenge10/file-organizer.git
cd file-organizer
pip install .
```

Or just run the single file without installing:

```bash
python file_organizer.py ~/Downloads --dry-run
```

## Usage

```bash
file-organizer [FOLDER] [--dry-run] [--version]
```

```bash
# preview first
file-organizer ~/Downloads --dry-run

# then do it
file-organizer ~/Downloads
```

Example output:

```text
Moved: holiday.jpg -> Images/holiday.jpg
Moved: invoice.pdf -> Documents/invoice.pdf
Moved: setup.exe -> Installers/setup.exe
Moved: notes.xyz -> Other/notes.xyz
4 file(s) organized.
```

## Categories

| Folder | Extensions |
|---|---|
| Images | jpg, jpeg, png, gif, bmp, webp, svg, heic, tiff |
| Documents | pdf, doc, docx, txt, md, rtf, odt, xls, xlsx, csv, ppt, pptx |
| Audio | mp3, wav, flac, aac, ogg, m4a |
| Video | mp4, mkv, avi, mov, webm, wmv |
| Archives | zip, rar, 7z, tar, gz, bz2, xz, tgz |
| Code | py, js, ts, html, css, json, java, c, cpp, go, rs, sh, yml, yaml |
| Installers | exe, msi, dmg, deb, rpm, apk, iso |
| Other | everything else |

Want different categories? Edit the `CATEGORIES` dictionary at the top of `file_organizer.py`.

## Tests

```bash
python -m unittest -v
```

## License

MIT
