from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _write_executable(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
    path.chmod(0o755)


def _script_workspace(tmp_path: Path) -> tuple[Path, Path]:
    workspace = tmp_path / "repo"
    bin_dir = tmp_path / "bin"
    (workspace / "scripts").mkdir(parents=True)
    bin_dir.mkdir()
    for name in ("install.sh", "test.sh"):
        shutil.copy2(ROOT / name, workspace / name)
    _write_executable(
        workspace / "scripts" / "prepare-build-ca.sh",
        "#!/usr/bin/env bash\nmkdir -p .build\n: > .build/ca-bundle.crt\nprintf '%s\\n' \"$PWD/.build/ca-bundle.crt\"\n",
    )
    return workspace, bin_dir


def test_reinstall_preserves_database_password(tmp_path: Path) -> None:
    workspace, bin_dir = _script_workspace(tmp_path)
    _write_executable(
        bin_dir / "docker",
        """#!/usr/bin/env bash
if [[ "$1" == "--version" ]]; then echo 'Docker version test'; exit 0; fi
if [[ "$1 $2" == "compose version" ]]; then echo 'v2.test'; exit 0; fi
if [[ "$1 $2" == "volume inspect" ]]; then exit 1; fi
if [[ "$1 $2 $3" == "compose ps --all" ]]; then echo api-id; exit 0; fi
if [[ "$1 $2" == "inspect --format" ]]; then echo running; exit 0; fi
exit 0
""",
    )
    _write_executable(
        bin_dir / "curl",
        "#!/usr/bin/env bash\ncase \"${*: -1}\" in */api/health) echo '{\"status\":\"ok\",\"method_questions\":128}' ;; esac\n",
    )
    env = {**os.environ, "PATH": f"{bin_dir}:{os.environ['PATH']}"}

    first = subprocess.run(
        ["bash", "install.sh"], cwd=workspace, env=env, input="8080\n1\n", text=True, capture_output=True
    )
    assert first.returncode == 0, first.stderr
    password_before = next(
        line for line in (workspace / ".env").read_text(encoding="utf-8").splitlines() if line.startswith("POSTGRES_PASSWORD=")
    )

    second = subprocess.run(
        ["bash", "install.sh"], cwd=workspace, env=env, input="8081\n1\n", text=True, capture_output=True
    )
    assert second.returncode == 0, second.stderr
    password_after = next(
        line for line in (workspace / ".env").read_text(encoding="utf-8").splitlines() if line.startswith("POSTGRES_PASSWORD=")
    )
    assert password_after == password_before
    assert "Vorhandene Datenbank-Konfiguration wird weiterverwendet" in second.stdout


def test_install_refuses_orphaned_database_volume(tmp_path: Path) -> None:
    workspace, bin_dir = _script_workspace(tmp_path)
    _write_executable(
        bin_dir / "docker",
        """#!/usr/bin/env bash
if [[ "$1" == "--version" ]]; then echo 'Docker version test'; exit 0; fi
if [[ "$1 $2" == "compose version" ]]; then echo 'v2.test'; exit 0; fi
if [[ "$1 $2" == "volume inspect" ]]; then exit 0; fi
exit 0
""",
    )
    _write_executable(bin_dir / "curl", "#!/usr/bin/env bash\nexit 0\n")
    env = {**os.environ, "PATH": f"{bin_dir}:{os.environ['PATH']}"}

    result = subprocess.run(["bash", "install.sh"], cwd=workspace, env=env, text=True, capture_output=True)

    assert result.returncode == 1
    assert "Datenbank-Volume, aber keine passende .env" in result.stderr
    assert "docker volume rm sovradar_sovradar_db_data" in result.stderr
    assert "docker compose down --volumes` in diesem Zustand NICHT" in result.stderr
    assert "unwiderruflich" in result.stderr
    assert not (workspace / ".env").exists()


def test_install_contains_safe_non_writable_runtime_preflight(tmp_path: Path) -> None:
    workspace, _ = _script_workspace(tmp_path)
    script = (workspace / "install.sh").read_text(encoding="utf-8")

    assert 'for runtime_path in .runtime .runtime/documents .runtime/exports .runtime/temp' in script
    assert '[[ -e "$runtime_path" && ! -w "$runtime_path" ]]' in script
    assert 'sudo chown -R' in script
    assert 'sudo mv .runtime' in script
    assert 'löscht Evidence-/Exportdaten absichtlich nicht automatisch' in script


def test_healthcheck_reports_restarting_api_without_waiting(tmp_path: Path) -> None:
    workspace, bin_dir = _script_workspace(tmp_path)
    _write_executable(bin_dir / "curl", "#!/usr/bin/env bash\nexit 22\n")
    _write_executable(
        bin_dir / "docker",
        """#!/usr/bin/env bash
if [[ "$1 $2 $3" == "compose ps --all" ]]; then echo api-id; exit 0; fi
if [[ "$1" == "inspect" ]]; then echo restarting; exit 0; fi
if [[ "$1 $2" == "compose logs" ]]; then echo 'database authentication failed' >&2; exit 0; fi
if [[ "$1 $2" == "compose ps" ]]; then echo 'api restarting' >&2; exit 0; fi
exit 0
""",
    )
    env = {**os.environ, "PATH": f"{bin_dir}:{os.environ['PATH']}"}

    result = subprocess.run(["bash", "test.sh"], cwd=workspace, env=env, text=True, capture_output=True, timeout=5)

    assert result.returncode == 1
    assert "Zustand 'restarting'" in result.stderr
    assert "database authentication failed" in result.stderr
