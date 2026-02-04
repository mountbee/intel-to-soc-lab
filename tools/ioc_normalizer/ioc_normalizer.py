#!/usr/bin/env python3
"""IOC normalizer CLI.

Parses IOC inputs from txt/csv and outputs normalized IOCRecord JSON.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from ipaddress import ip_address
from pathlib import Path
from typing import Iterable, List
from urllib.parse import urlsplit, urlunsplit


HASH_MD5_RE = re.compile(r"^[A-Fa-f0-9]{32}$")
HASH_SHA1_RE = re.compile(r"^[A-Fa-f0-9]{40}$")
HASH_SHA256_RE = re.compile(r"^[A-Fa-f0-9]{64}$")
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,63}$")
DOMAIN_RE = re.compile(r"^(?=.{1,253}$)([A-Za-z0-9-]{1,63}\.)+[A-Za-z]{2,63}$")
Record = dict[str, object]


def parse_input(path: Path) -> List[str]:
    """Parse input file (txt/csv) into raw IOC strings."""
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    values: List[str] = []
    suffix = path.suffix.lower()

    if suffix == ".csv":
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                return values
            field_map = {name.strip().lower(): name for name in reader.fieldnames}
            if "value" in field_map:
                key = field_map["value"]
            else:
                key = reader.fieldnames[0]
            for row in reader:
                raw = (row.get(key) or "").strip()
                if raw:
                    values.append(raw)
        return values

    with path.open(encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.lstrip().startswith("#"):
                continue
            for token in re.split(r"[,\s]+", stripped):
                token = token.strip()
                if token:
                    values.append(token)
    return values


def classify_ioc(value: str) -> str:
    """Classify IOC type based on value."""
    val = value.strip()
    if not val:
        return "unknown"

    try:
        ip = ip_address(val)
        if ip.version == 4:
            return "ip"
    except ValueError:
        pass

    if HASH_MD5_RE.fullmatch(val):
        return "hash_md5"
    if HASH_SHA1_RE.fullmatch(val):
        return "hash_sha1"
    if HASH_SHA256_RE.fullmatch(val):
        return "hash_sha256"

    parts = urlsplit(val)
    if parts.scheme in {"http", "https"} and parts.netloc:
        return "url"

    if EMAIL_RE.fullmatch(val):
        return "email"

    if DOMAIN_RE.fullmatch(val):
        return "domain"

    return "unknown"


def normalize_value(value: str, ioc_type: str) -> str:
    """Normalize IOC value based on type."""
    val = value.strip()

    if ioc_type in {"hash_md5", "hash_sha1", "hash_sha256"}:
        return val.lower()

    if ioc_type == "domain":
        return val.lower()

    if ioc_type == "email":
        if "@" in val:
            local, domain = val.split("@", 1)
            return f"{local}@{domain.lower()}"
        return val.lower()

    if ioc_type == "url":
        parts = urlsplit(val)
        if parts.scheme and parts.netloc:
            scheme = parts.scheme.lower()
            netloc = parts.netloc.lower()
            return urlunsplit((scheme, netloc, parts.path, parts.query, parts.fragment))
        return val

    if ioc_type == "ip":
        try:
            return str(ip_address(val))
        except ValueError:
            return val

    return val


def dedup_key(record: Record) -> tuple[str, str]:
    """Create a deterministic deduplication key for a record."""
    ioc_type = record.get("type", "unknown")
    value = record.get("value", "")

    if ioc_type in {"domain", "email"}:
        return (ioc_type, value.lower())

    if ioc_type == "url":
        parts = urlsplit(value)
        if parts.scheme and parts.netloc:
            scheme = parts.scheme.lower()
            netloc = parts.netloc.lower()
            normalized = urlunsplit((scheme, netloc, parts.path, parts.query, parts.fragment))
            return (ioc_type, normalized)
        return (ioc_type, value.lower())

    if ioc_type in {"hash_md5", "hash_sha1", "hash_sha256"}:
        return (ioc_type, value.lower())

    return (ioc_type, value)


def deduplicate(records: Iterable[Record]) -> List[Record]:
    """Remove duplicate records while preserving first-seen order."""
    seen = set()
    output = []
    for record in records:
        key = dedup_key(record)
        if key in seen:
            continue
        seen.add(key)
        output.append(record)
    return output


def build_record(value: str, args: argparse.Namespace) -> Record:
    """Build IOCRecord dict from raw value and CLI args."""
    ioc_type = classify_ioc(value)
    normalized = normalize_value(value, ioc_type)

    record = {
        "type": ioc_type,
        "value": normalized,
        "source": args.source,
        "confidence": args.confidence,
        "context": "normalized from input",
    }

    if args.first_seen:
        record["first_seen"] = args.first_seen
    if args.last_seen:
        record["last_seen"] = args.last_seen
    if args.pack:
        record["pack"] = args.pack
    if args.tag:
        record["tags"] = args.tag

    return record


def run(args: argparse.Namespace) -> int:
    """Run normalization process and write JSON output."""
    if not (1 <= args.confidence <= 5):
        print("Error: --confidence harus bernilai 1-5", file=sys.stderr)
        return 2

    input_path = Path(args.input)
    try:
        values = parse_input(input_path)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    records = [build_record(value, args) for value in values]
    records = deduplicate(records)
    records.sort(key=lambda r: (str(r.get("type", "")), str(r.get("value", ""))))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(records, handle, indent=2, ensure_ascii=True)
        handle.write("\n")

    return 0


def build_parser() -> argparse.ArgumentParser:
    """Construct CLI argument parser."""
    parser = argparse.ArgumentParser(description="IOC normalizer")
    parser.add_argument("--input", required=True, help="Path input (txt/csv)")
    parser.add_argument("--output", required=True, help="Path output JSON")
    parser.add_argument("--source", required=True, help="Source label")
    parser.add_argument("--confidence", type=int, default=3, help="Confidence 1-5")
    parser.add_argument("--pack", help="Pack name (pack01/pack02)")
    parser.add_argument("--tag", action="append", default=[], help="Tag (repeatable)")
    parser.add_argument("--first-seen", dest="first_seen", help="ISO 8601")
    parser.add_argument("--last-seen", dest="last_seen", help="ISO 8601")
    return parser


def main() -> int:
    """CLI entrypoint."""
    parser = build_parser()
    args = parser.parse_args()
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
