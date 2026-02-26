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
>>> print(result.file)
file_2026-02-25_14-30-00.txt
>>> print(result.timestamp)
2026-02-25 14:30:00
```

**Read the timestamp back:**

```python
>>> parsed = FileTimestamp.read(result.file)
>>> print(parsed.file)
file.txt
>>> print(parsed.timestamp)
2026-02-25 14:30:00
>>> print(parsed.age)
0:00:12.345678
```

## Requirements

Python 3.14+

## Licence

[MIT](LICENCE)
