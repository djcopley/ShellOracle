import shutil
from pathlib import Path

from prompt_toolkit import print_formatted_text
from prompt_toolkit.application import create_app_session_from_tty
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.shortcuts import confirm


def print_info(info: str) -> None:
    print_formatted_text(FormattedText([("ansiblue", info)]))


def print_error(error: str) -> None:
    print_formatted_text(FormattedText([("ansired", error)]))


def replace_home_with_tilde(path: Path) -> Path:
    relative_path = path.relative_to(Path.home())
    return Path("~") / relative_path


supported_shells = ("zsh", "bash")


def get_installed_shells() -> list[str]:
    shells = []
    for shell in supported_shells:
        if shutil.which(shell):
            shells.append(shell)
    return shells


def get_bundled_script_path(shell: str) -> Path:
    parent = Path(__file__).parent
    if shell == "zsh":
        return parent / "shelloracle.zsh"
    elif shell == "bash":
        return parent / "shelloracle.bash"


def get_script_path(shell: str) -> Path:
    if shell == "zsh":
        return Path.home() / ".shelloracle.zsh"
    elif shell == "bash":
        return Path.home() / ".shelloracle.bash"


def get_rc_path(shell: str) -> Path:
    if shell == "zsh":
        return Path.home() / ".zshrc"
    elif shell == "bash":
        return Path.home() / ".bashrc"


def write_script_home(shell: str) -> None:
    shelloracle = get_bundled_script_path(shell).read_bytes()
    destination = get_script_path(shell)
    destination.write_bytes(shelloracle)
    print_info(f"Successfully wrote key bindings to {replace_home_with_tilde(destination)}")


def update_rc(shell: str) -> None:
    rc_path = get_rc_path(shell)
    rc_path.touch(exist_ok=True)
    with rc_path.open("r") as file:
        zshrc = file.read()
    shelloracle_script = get_script_path(shell)
    line = f"[ -f {shelloracle_script} ] && source {shelloracle_script}"
    if line not in zshrc:
        with rc_path.open("a") as file:
            file.write("\n")
            file.write(line)
    print_info(f"Successfully updated {replace_home_with_tilde(rc_path)}")


def bootstrap() -> None:
    with create_app_session_from_tty():
        if not (shells := get_installed_shells()):
            print_error(f"No compatible shells found. Supported shells: {', '.join(supported_shells)}")
            return
        if confirm("Enable terminal keybindings and update rc?", suffix=" ([y]/n) ") is False:
            return
        for shell in shells:
            write_script_home(shell)
            update_rc(shell)


if __name__ == '__main__':
    bootstrap()
