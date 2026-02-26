# lyutil

A lightweight collection of everyday Python utilities.

## Installation

```bash
pip install lyutil
```

## Modules

### Timestamps

Embed and extract timestamps in filenames.

```python
>>> from pathlib import Path
>>> from lyutil import FileTimestamp
```

**Add a timestamp to a filename:**

```python
>>> result = FileTimestamp.add(Path("path/to/file.txt"))
>>> result.file
path/to/file_2026-02-25_14-30-00.txt
>>> result.timestamp
2026-02-25 14:30:00
```

**Read the timestamp back:**

```python
>>> parsed = FileTimestamp.read(result.file)
>>> parsed.file
path/to/file.txt
>>> parsed.timestamp
2026-02-25 14:30:00
>>> parsed.age
0:00:12.345678
```

## Requirements

Python 3.14+

## Licence

[MIT](LICENCE)
