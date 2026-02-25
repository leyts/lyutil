# lyutil

A lightweight collection of everyday Python utilities.

## Modules

### Timestamps

Embed and extract timestamps in filenames.

```python
from pathlib import Path
from lyutil import FileTimestamp
```

**Add a timestamp to a filename:**

```python
>>> result = FileTimestamp.add(Path("backup.tar.gz"))
>>> print(result.file)
backup_2026-02-25_14-30-00.tar.gz
>>> print(result.timestamp)
2026-02-25 14:30:00
```

**Read the timestamp back:**

```python
>>> parsed = FileTimestamp.read(result.file)
>>> print(parsed.file)
backup.tar.gz
>>> print(parsed.timestamp)
2026-02-25 14:30:00
>>> print(parsed.age)
0:00:12.345678
```

## Requirements

Python 3.14+

## Licence

[MIT](LICENCE)
