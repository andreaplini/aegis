#!/usr/bin/env python3
"""Check the current interpreter against the configured minimum version."""

import sys


def version_is_supported(actual, minimum):
    return tuple(actual[: len(minimum)]) >= tuple(minimum)


def main():
    minimum = tuple(int(part) for part in sys.argv[1].split("."))
    actual = tuple(sys.version_info[: len(minimum)])
    if version_is_supported(actual, minimum):
        return 0

    required = ".".join(str(part) for part in minimum)
    found = ".".join(str(part) for part in actual)
    print(
        f"Versione Python minima richiesta: {required}. Versione trovata: {found}.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
