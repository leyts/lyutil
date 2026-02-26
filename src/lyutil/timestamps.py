"""Utilities for embedding timestamps in filenames."""

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, ClassVar, NamedTuple

from lyutil.exceptions import InvalidPathError, TimestampParseError

if TYPE_CHECKING:
    from pathlib import Path


class TimestampedFile(NamedTuple):
    """A path paired with the timestamp extracted from its filename."""

    file: Path
    timestamp: datetime

    @property
    def age(self) -> timedelta:
        """Time elapsed since the embedded timestamp."""
        return datetime.now() - self.timestamp  # noqa: DTZ005


class FileTimestamp:
    """Add and read timestamps in filenames."""

    _DT_FORMAT: ClassVar[str] = "%Y-%m-%d_%H-%M-%S"
    _SEPARATOR: ClassVar[str] = "_"

    @staticmethod
    def _validate_file(file: Path) -> None:
        """Raise ``InvalidPathError`` if *file* has no usable stem."""
        if not file.stem or file.stem.isspace():
            msg = "Path has no usable stem"
            raise InvalidPathError(msg)

    @staticmethod
    def _split_stem(stem: str) -> tuple[str, str]:
        """Split a stem into the original stem and raw timestamp.

        Args:
            stem: The filename stem to split.

        Returns:
            A ``(original_stem, raw_timestamp)`` tuple.

        Raises:
            TimestampParseError: If the stem is too short or the
                separator is missing.
        """
        sep: str = FileTimestamp._SEPARATOR
        min_length: int = len(
            datetime.min.strftime(format=FileTimestamp._DT_FORMAT) + sep  # noqa: DTZ901
        )

        if len(stem) <= min_length:
            msg = f"Stem too short to contain a timestamp: {stem}"
            raise TimestampParseError(msg)

        if stem[-min_length] != sep:
            msg = f"Expected {sep!r} before timestamp in: {stem}"
            raise TimestampParseError(msg)

        return stem[:-min_length], stem[-min_length + len(sep) :]

    @staticmethod
    def add(file: Path, timestamp: datetime | None = None) -> TimestampedFile:
        """Return a new path with a timestamp appended to the stem.

        Args:
            file: The original file path.
            timestamp: The datetime to embed. Defaults to ``datetime.now()``.

        Returns:
            A :class:`TimestampedFile` containing the timestamped path and
                the datetime used.
        """
        FileTimestamp._validate_file(file)

        if timestamp is None:
            timestamp = datetime.now()  # noqa: DTZ005

        formatted: str = timestamp.strftime(format=FileTimestamp._DT_FORMAT)
        stamped: Path = file.with_stem(
            stem=f"{file.stem}{FileTimestamp._SEPARATOR}{formatted}"
        )
        return TimestampedFile(file=stamped, timestamp=timestamp)

    @staticmethod
    def read(file: Path) -> TimestampedFile:
        """Extract a timestamp previously added by :meth:`add`.

        Args:
            file: A path whose stem ends with ``_YYYY-MM-DD_HH-MM-SS``.

        Returns:
            A :class:`TimestampedFile` containing the original path
            (without the timestamp) and the parsed ``datetime``.

        Raises:
            TimestampParseError: If *file* does not contain a valid
                timestamp suffix.
        """
        FileTimestamp._validate_file(file)
        org_stem, raw_ts = FileTimestamp._split_stem(file.stem)

        try:
            ts: datetime = datetime.strptime(  # noqa: DTZ007
                raw_ts, FileTimestamp._DT_FORMAT
            )
        except ValueError:
            msg = f"Could not parse timestamp: {raw_ts!r}"
            raise TimestampParseError(msg) from None

        org_file: Path = file.with_stem(stem=org_stem)
        return TimestampedFile(file=org_file, timestamp=ts)
