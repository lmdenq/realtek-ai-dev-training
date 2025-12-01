"""
A robust log parser for Mobile + NetService + AIInference logs.

Author: <your name>
Date  : 2025-11-24
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional

# --------------------------------------------------------------------------- #
# 1.  LogEntry data class
# --------------------------------------------------------------------------- #
@dataclass
class LogEntry:
    """
    Represents a single log entry.

    Attributes
    ----------
    timestamp : str
        The timestamp of the log (e.g. "2025-11-16 09:00:01").
    level : str
        Log level: INFO / WARN / ERROR / DEBUG.
    source : str
        Origin of the log: MobileApp / NetService / AIInference.
    fields : Dict[str, str]
        All key=value pairs parsed from the log line.
    raw_message : str
        Any remaining text that is NOT in key=value format.
    """
    timestamp: str
    level: str
    source: str
    fields: Dict[str, str]
    raw_message: str = ""

# --------------------------------------------------------------------------- #
# 2.  Helper functions
# --------------------------------------------------------------------------- #

def _split_header_and_body(line: str) -> Optional[tuple[str, str, str, str]]:
    """
    Split a raw log line into timestamp, level, source and the remaining body.

    Parameters
    ----------
    line : str
        A raw log line.

    Returns
    -------
    tuple[str, str, str, str] | None
        (timestamp, level, source, body) or None if the line is invalid.
    """
    parts = line.split()
    if len(parts) < 4:
        # Not enough tokens to form a valid log entry
        return None

    # Timestamp is the first two tokens (date + time)
    timestamp = f"{parts[0]} {parts[1]}"
    level = parts[2]
    source = parts[3]
    body = " ".join(parts[4:])
    return timestamp, level, source, body


def _parse_body(body: str) -> tuple[Dict[str, str], str]:
    """
    Extract key=value pairs from the body string.

    Parameters
    ----------
    body : str
        The body part of the log line (everything after source).

    Returns
    -------
    tuple[Dict[str, str], str]
        A dictionary of parsed key/value pairs and a string containing
        everything that was not parsed as a key=value pair.
    """
    fields: Dict[str, str] = {}
    # We keep a list of tokens that were NOT key=value
    raw_tokens: List[str] = []

    # Regular expression that matches key=value.  It supports:
    #   - unquoted values (no spaces)
    #   - quoted values (double quotes)
    kv_pattern = re.compile(r'(\w+)=(".*?"|\S+)')

    for token in body.split():
        match = kv_pattern.fullmatch(token)
        if match:
            key, value = match.group(1), match.group(2)
            # Remove surrounding quotes if present
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            fields[key] = value
        else:
            raw_tokens.append(token)

    raw_message = " ".join(raw_tokens)
    return fields, raw_message

# --------------------------------------------------------------------------- #
# 3.  Core parser
# --------------------------------------------------------------------------- #

def parse_line(line: str) -> Optional[LogEntry]:
    """
    Parse a single line of log into a :class:`LogEntry`.

    Parameters
    ----------
    line : str
        A raw log line read from the log file.

    Returns
    -------
    LogEntry | None
        A `LogEntry` object if the line could be parsed,
        otherwise ``None`` (e.g. blank line or malformed entry).
    """
    header = _split_header_and_body(line)
    if header is None:
        return None

    timestamp, level, source, body = header
    fields, raw_message = _parse_body(body)
    return LogEntry(
        timestamp=timestamp,
        level=level,
        source=source,
        fields=fields,
        raw_message=raw_message,
    )

# --------------------------------------------------------------------------- #
# 4.  Public API
# --------------------------------------------------------------------------- #

def parse_file(file_path: str | Path) -> List[LogEntry]:
    """
    Parse an entire log file.

    Parameters
    ----------
    file_path : str | pathlib.Path
        Path to the log file.

    Returns
    -------
    List[LogEntry]
        A list of parsed log entries.
    """
    path = Path(file_path)
    entries: List[LogEntry] = []

    # Using UTF‑8 is safe for most log files; change if your logs use a
    # different encoding.
    with path.open(encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.rstrip("\n")
            if not line:
                # Skip empty lines
                continue
            entry = parse_line(line)
            if entry is not None:
                entries.append(entry)

    return entries


def write_json_lines(output_path: str | Path, entries: Iterable[LogEntry]) -> None:
    """
    Write a collection of LogEntry objects as JSON Lines.

    Each line is a JSON representation of the LogEntry.
    This format is convenient for ingestion into ELK/Databricks/Redshift,
    etc.

    Parameters
    ----------
    output_path : str | pathlib.Path
        Destination file.  It will be created or truncated.
    entries : Iterable[LogEntry]
        Log entries to write.
    """
    out_path = Path(output_path)
    with out_path.open("w", encoding="utf-8") as f:
        for entry in entries:
            # asdict() turns the dataclass into a plain dict
            json_line = json.dumps(asdict(entry), ensure_ascii=False)
            f.write(json_line + "\n")


# --------------------------------------------------------------------------- #
# 5.  Demo / CLI wrapper (optional)
# --------------------------------------------------------------------------- #
def _demo() -> None:
    """
    Simple command‑line demo: read *log.txt* and write *log.jsonl*.
    """
    log_file = Path("./datasets/example_mobile_ai.log")          # <-- change to your log file
    output_file = Path("example_logs.jsonl")     # <-- output destination

    entries = parse_file(log_file)
    write_json_lines(output_file, entries)

    print(f"Parsed {len(entries)} log entries.")
    print(f"JSON Lines written to {output_file}")

if __name__ == "__main__":
    _demo()