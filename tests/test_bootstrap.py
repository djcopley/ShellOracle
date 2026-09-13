from __future__ import annotations

import platform
import shutil
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from shelloracle.bootstrap import (
    get_bundled_script_path,
    get_rc_path,
    get_script_path,
    supported_shells,
    update_rc,
)
from shelloracle.providers import get_system_prompt


class TestSupportedShells:
    def test_pwsh_in_supported_shells(self):
        assert "pwsh" in supported_shells


class TestGetBundledScriptPath:
    def test_zsh(self):
        path = get_bundled_script_path("zsh")
        assert path.name == "shelloracle.zsh"

    def test_fish(self):
        path = get_bundled_script_path("fish")
        assert path.name == "shelloracle.fish"

    def test_bash(self):
        path = get_bundled_script_path("bash")
        assert path.name == "shelloracle.bash"

    def test_pwsh(self):
        path = get_bundled_script_path("pwsh")
        assert path.name == "shelloracle.ps1"
        assert path.exists()


class TestGetScriptPath:
    def test_zsh(self):
        path = get_script_path("zsh")
        assert path.name == ".shelloracle.zsh"

    def test_fish(self):
        path = get_script_path("fish")
        assert path.name == ".shelloracle.fish"

    def test_bash(self):
        path = get_script_path("bash")
        assert path.name == ".shelloracle.bash"

    def test_pwsh(self):
        path = get_script_path("pwsh")
        assert path.name == ".shelloracle.ps1"


class TestGetRcPath:
    def test_zsh(self):
        path = get_rc_path("zsh")
        assert path.name == ".zshrc"

    def test_fish(self):
        path = get_rc_path("fish")
        assert path.name == "config.fish"

    def test_bash(self):
        path = get_rc_path("bash")
        assert path.name == ".bashrc"

    @pytest.fixture
    def no_pwsh(self):
        with patch.object(shutil, "which", return_value=None):
            yield

    def test_pwsh_uses_reported_profile(self):
        reported = Path.home() / "OneDrive" / "Documents" / "PowerShell" / "Microsoft.PowerShell_profile.ps1"
        completed = subprocess.CompletedProcess(args=[], returncode=0, stdout=f"{reported}\n", stderr="")
        with (
            patch.object(shutil, "which", return_value="/usr/bin/pwsh"),
            patch.object(subprocess, "run", return_value=completed) as run,
        ):
            path = get_rc_path("pwsh")
        assert path == reported
        assert run.call_args.args[0][0] == "/usr/bin/pwsh"

    def test_pwsh_falls_back_when_pwsh_fails(self, monkeypatch):
        monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
        with (
            patch.object(shutil, "which", return_value="/usr/bin/pwsh"),
            patch.object(subprocess, "run", side_effect=subprocess.CalledProcessError(1, "pwsh")),
            patch.object(platform, "system", return_value="Darwin"),
        ):
            path = get_rc_path("pwsh")
        assert path == Path.home() / ".config" / "powershell" / "Microsoft.PowerShell_profile.ps1"

    def test_pwsh_windows(self, no_pwsh):
        with patch.object(platform, "system", return_value="Windows"):
            path = get_rc_path("pwsh")
        assert path.name == "Microsoft.PowerShell_profile.ps1"
        assert "Documents" in path.parts

    def test_pwsh_non_windows(self, no_pwsh, monkeypatch):
        monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
        with patch.object(platform, "system", return_value="Darwin"):
            path = get_rc_path("pwsh")
        assert path == Path.home() / ".config" / "powershell" / "Microsoft.PowerShell_profile.ps1"

    def test_pwsh_non_windows_xdg_config_home(self, no_pwsh, monkeypatch, tmp_path):
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        with patch.object(platform, "system", return_value="Linux"):
            path = get_rc_path("pwsh")
        assert path == tmp_path / "powershell" / "Microsoft.PowerShell_profile.ps1"


class TestUpdateRc:
    @pytest.fixture
    def rc_path(self, tmp_path):
        return tmp_path / "profile.ps1"

    @pytest.fixture
    def run_update_rc(self, tmp_path, rc_path):
        def run(script_path: Path) -> None:
            with (
                patch.object(Path, "home", return_value=tmp_path),
                patch("shelloracle.bootstrap.get_rc_path", return_value=rc_path),
                patch("shelloracle.bootstrap.get_script_path", return_value=script_path),
            ):
                update_rc("pwsh")

        return run

    def test_pwsh_profile_line_is_quoted_and_guarded(self, tmp_path, rc_path, run_update_rc):
        script_path = tmp_path / "John Smith" / ".shelloracle.ps1"
        run_update_rc(script_path)
        assert rc_path.read_text().strip() == f"if (Test-Path '{script_path}') {{ . '{script_path}' }}"

    def test_pwsh_profile_line_escapes_single_quotes(self, tmp_path, rc_path, run_update_rc):
        script_path = tmp_path / "O'Brien" / ".shelloracle.ps1"
        run_update_rc(script_path)
        escaped = str(script_path).replace("'", "''")
        assert f". '{escaped}'" in rc_path.read_text()

    def test_pwsh_profile_line_not_duplicated(self, tmp_path, rc_path, run_update_rc):
        script_path = tmp_path / ".shelloracle.ps1"
        run_update_rc(script_path)
        run_update_rc(script_path)
        assert rc_path.read_text().count("Test-Path") == 1


class TestGetSystemPrompt:
    def test_default_is_bash(self, monkeypatch):
        monkeypatch.delenv("SHOR_SHELL", raising=False)
        prompt = get_system_prompt()
        assert "Bash" in prompt
        assert "PowerShell" not in prompt

    def test_powershell(self, monkeypatch):
        monkeypatch.setenv("SHOR_SHELL", "powershell")
        prompt = get_system_prompt()
        assert "PowerShell" in prompt
        assert "Bash" not in prompt

    def test_powershell_case_insensitive(self, monkeypatch):
        monkeypatch.setenv("SHOR_SHELL", "POWERSHELL")
        prompt = get_system_prompt()
        assert "PowerShell" in prompt

    def test_unknown_shell_falls_back_to_bash(self, monkeypatch):
        monkeypatch.setenv("SHOR_SHELL", "unknown-shell")
        prompt = get_system_prompt()
        assert "Bash" in prompt
