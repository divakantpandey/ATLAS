"""The service Dockerfiles install Python dependencies from hashed locks.

geometric-lens and v3-service must install requirements using --require-hashes
and --only-binary :all: (issue #333, refs #202).
"""
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("dockerfile,lockfile", [
    ("geometric-lens/Dockerfile", "geometric-lens/requirements-lock.txt"),
    ("v3-service/Dockerfile", "v3-service/requirements-lock.txt"),
])
def test_dockerfile_installs_with_require_hashes_and_only_binary(dockerfile, lockfile):
    df_path = ROOT / dockerfile
    lock_path = ROOT / lockfile

    assert df_path.exists(), f"{dockerfile} does not exist"
    assert lock_path.exists(), f"{lockfile} does not exist"

    df_content = df_path.read_text(encoding="utf-8")
    lock_content = lock_path.read_text(encoding="utf-8")

    assert "--require-hashes" in df_content, f"{dockerfile} must install with --require-hashes"
    assert "--only-binary :all:" in df_content, f"{dockerfile} must install with --only-binary :all:"
    assert "--hash=sha256:" in lock_content, f"{lockfile} has no sha256 hashes"
