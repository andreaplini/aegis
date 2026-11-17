from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_python


class CheckPythonTests(unittest.TestCase):
    def test_accepts_the_minimum_version(self) -> None:
        self.assertTrue(check_python.version_is_supported((3, 9), (3, 9)))

    def test_accepts_a_newer_minor_version(self) -> None:
        self.assertTrue(check_python.version_is_supported((3, 14), (3, 9)))

    def test_rejects_an_older_minor_version(self) -> None:
        self.assertFalse(check_python.version_is_supported((3, 8), (3, 9)))


if __name__ == "__main__":
    unittest.main()
