import shutil
from pathlib import Path

import pytest

TMP_DIR = Path(__file__).resolve().parent / "_tmp"


@pytest.fixture
def data_dir():
    shutil.rmtree(TMP_DIR, ignore_errors=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    yield TMP_DIR
    shutil.rmtree(TMP_DIR, ignore_errors=True)
