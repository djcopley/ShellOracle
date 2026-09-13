from __future__ import annotations

import platform
from pathlib import Path
from unittest.mock import patch

import pytest

from shelloracle.bootstrap import (
    get_bundled_script_path,
    get_rc_path,
    get_script_path,
    supported_shells,
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

    def test_pwsh_windows(self):
        with patch.object(platform, "system", return_value="Windows"):
            path = get_rc_path("pwsh")
        assert path.name == "Microsoft.PowerShell_profile.ps1"
        assert "Documents" in path.parts

    def test_pwsh_non_windows(self):
        with patch.object(platform, "system", return_value="Darwin"):
            path = get_rc_path("pwsh")
        assert path.name == "Microsoft.PowerShell_profile.ps1"
        assert ".config" in path.parts


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
