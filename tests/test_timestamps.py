"""Tests for lyutil.timestamps."""

from datetime import datetime
from pathlib import Path

import pytest
import time_machine

from lyutil import (
    FileTimestamp,
    InvalidPathError,
    TimestampedFile,
    TimestampParseError,
)

TEST_FILE_PATH = Path("/path/to/file.txt")
TEST_DATETIME = datetime(2025, 6, 20, 14, 5, 59)  # noqa: DTZ001
TEST_FILENAMES: set[str] = {
    ".gitignore",
    "create_cache_dir.sh",
    "data.tar.gz",
    "file.txt",
    "Makefile",
}

time_machine.naive_mode = time_machine.NaiveMode.LOCAL  # ty: ignore[invalid-assignment]


class TestFileTimestampAdd:
    """Tests for ``FileTimestamp.add``."""

    def test_default_timestamp_format(self):
        """Output stem ends with a correctly formatted timestamp."""
        result: TimestampedFile = FileTimestamp.add(TEST_FILE_PATH)
        _, raw_ts = result.file.stem.split(sep="_", maxsplit=1)
        datetime.strptime(raw_ts, FileTimestamp._DT_FORMAT)  # noqa: DTZ007, SLF001

    @pytest.mark.time_machine(TEST_DATETIME, tick=False)
    def test_explicit_timestamp(self):
        """An explicit datetime produces the expected path."""
        result: TimestampedFile = FileTimestamp.add(TEST_FILE_PATH)
        assert result.file.name == "file_2025-06-20_14-05-59.txt"
        assert result.timestamp == TEST_DATETIME

    def test_preserves_parent(self):
        """The directory portion of the path is unchanged."""
        result: TimestampedFile = FileTimestamp.add(TEST_FILE_PATH)
        assert result.file.parent == TEST_FILE_PATH.parent

    @pytest.mark.parametrize("path", [Path(), Path(" ")])
    def test_blank_stem_raises(self, path: Path):
        """A path with no stem raises ``InvalidPathError``."""
        with pytest.raises(InvalidPathError, match="no usable stem"):
            FileTimestamp.read(path)


class TestFileTimestampRead:
    """Tests for ``FileTimestamp.read``."""

    @pytest.mark.time_machine(TEST_DATETIME, tick=False)
    @pytest.mark.parametrize("filename", TEST_FILENAMES)
    def test_roundtrip(self, tmp_path: Path, filename: str):
        """Parsing a stamped path recovers the original path and datetime."""
        original: Path = tmp_path / filename
        stamped: TimestampedFile = FileTimestamp.add(original)
        parsed: TimestampedFile = FileTimestamp.read(stamped.file)

        assert parsed.file == original
        assert parsed.timestamp == TEST_DATETIME

    def test_invalid_no_timestamp(self):
        """A path with no timestamp raises ``TimestampParseError``."""
        with pytest.raises(TimestampParseError, match="too short"):
            FileTimestamp.read(Path("file.txt"))

    def test_invalid_timestamp_content(self):
        """Correct length and separator but bogus date digits."""
        with pytest.raises(TimestampParseError, match="Could not parse"):
            FileTimestamp.read(Path("file_2025-13-99_25-70-99.txt"))

    def test_invalid_empty_original_stem(self):
        """A stem that is only separator + timestamp has no original stem."""
        with pytest.raises(TimestampParseError):
            FileTimestamp.read(Path("_2025-06-20_14-05-59.txt"))

    @pytest.mark.parametrize("path", [Path(), Path(" ")])
    def test_blank_stem_raises(self, path: Path):
        """A path with no stem raises ``InvalidPathError``."""
        with pytest.raises(InvalidPathError, match="no usable stem"):
            FileTimestamp.read(path)
