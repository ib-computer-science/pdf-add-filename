# pdf-add-filename

A Linux command-line tool that stamps the name of a PDF file as centered text at the top of its first page, and writes the result to a new file.

## Requirements

- Python 3.8 or later
- Git (to clone the repository)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/pdf-add-filename.git
cd pdf-add-filename
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv .venv
.venv/bin/pip install --require-hashes -r requirements.txt
```

> **Note on hash pinning:** `requirements.txt` pins PyMuPDF to an exact version and its SHA-256 wheel hash. `--require-hashes` makes pip verify the downloaded file matches that hash before installing, guarding against a tampered package on PyPI or a compromised mirror (supply-chain attack).
>
> **Implications to be aware of:**
> - The hash in `requirements.txt` is for the **Linux x86_64** wheel. If you install on a different platform (macOS, Windows, or another CPU architecture), pip will download a different wheel and the hash will not match — installation will fail. To support other platforms, add their hashes too (run `pip download pymupdf==1.27.2 --no-deps` on each target platform, then `pip hash` the resulting wheel, and append each `--hash=sha256:…` to the same line in `requirements.txt`).
> - When upgrading PyMuPDF, you must update the pinned version *and* replace the hash(es).

### 3. Make the launcher script executable

```bash
chmod +x pdf-add-filename
```

### 4. Add the program to your PATH

The recommended approach is to create a symlink in `~/.local/bin`, which is on `$PATH` by default on most modern Linux distributions (Debian, Ubuntu, Fedora, etc.):

```bash
mkdir -p ~/.local/bin
ln -s "$PWD/pdf-add-filename" ~/.local/bin/pdf-add-filename
```

Verify that `~/.local/bin` is on your `$PATH`:

```bash
echo $PATH | grep -o '[^:]*local/bin[^:]*'
```

If it is missing, add the following line to your `~/.bashrc` (or `~/.profile` for login shells) and restart your terminal:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

After that you can invoke the tool from anywhere:

```bash
pdf-add-filename input.pdf output.pdf
```

> **Note:** The launcher script automatically uses the `.venv` inside the cloned repository. You do not need to activate the virtual environment manually.

## Usage

```
pdf-add-filename [OPTIONS] INPUT OUTPUT
```

| Argument | Description |
|---|---|
| `INPUT` | Path to the source PDF file |
| `OUTPUT` | Path to write the resulting PDF file |

### Options

| Option | Default | Description |
|---|---|---|
| `--color COLOR` | `red` | Color of the added text. Accepts named colors or hex values. |
| `--margin MARGIN` | `1cm` | Distance of the text from the top of the page. |
| `--font-size PT` | `12` | Font size in points. |

### Color values

Named colors: `red`, `green`, `blue`, `black`, `white`, `yellow`, `orange`, `purple`, `cyan`, `magenta`, `gray`

Hex values: `#rrggbb` or `rrggbb` — for example `#ff8800` or `ff8800`.

### Margin units

| Unit | Example |
|---|---|
| Centimetres | `1cm`, `1.5cm` |
| Millimetres | `10mm` |
| Inches | `0.5in` |
| Points (1/72 in) | `28pt` |

## Examples

Add filename in red at 1 cm from the top (defaults):

```bash
pdf-add-filename report.pdf report-labelled.pdf
```

Use a blue label, 5 mm from the top, 10 pt font:

```bash
pdf-add-filename report.pdf report-labelled.pdf --color blue --margin 5mm --font-size 10
```

Use a custom hex color:

```bash
pdf-add-filename report.pdf report-labelled.pdf --color "#ff8800"
```

## Uninstalling

Remove the symlink and the cloned directory:

```bash
rm ~/.local/bin/pdf-add-filename
rm -rf /path/to/pdf-add-filename
```

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

See [LICENSE.txt](LICENSE.txt) for the full license text.
