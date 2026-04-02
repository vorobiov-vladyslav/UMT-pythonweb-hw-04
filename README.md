# Async File Sorter

Python script that asynchronously reads files from a source folder and distributes them into subfolders based on file extension.

## Installation

```bash
pip install aiofiles aioshutil
```

## Usage

```bash
python sort_files.py <source_folder> [-o <output_folder>]
```

### Arguments

| Argument | Description | Default |
|---|---|---|
| `source` | Path to the source folder with files to sort | required |
| `-o`, `--output` | Path to the output folder | `dist` |

### Example

```bash
python sort_files.py ./my_files -o ./sorted
```

Result:
```
sorted/
├── jpg/
│   └── photo.jpg
├── pdf/
│   └── document.pdf
├── py/
│   └── script.py
├── gz/
│   └── archive.tar.gz
└── no_extension/
    └── Makefile
```

## Testing

The `test_files/` directory contains 20 sample files with various extensions and nested subdirectories.

Run the script on test files:

```bash
python sort_files.py test_files -o test_output
```

Clean up after testing:

```bash
rm -rf test_output
```
