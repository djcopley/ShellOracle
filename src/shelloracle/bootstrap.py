import os
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


def ensure_zsh() -> None:
    shell = os.environ.get("SHELL")
    if shell is None:
        print_error("Unable to determine shell environment. If you are confident "
                    "that you are running in zsh, run again with `SHELL=zsh python3 -m shelloracle --init`")
        exit(1)
    if "zsh" not in shell:
        print_error(f"'{shell}' is currently unsupported. "
                    f"Please open an issue https://github.com/djcopley/ShellOracle/issues.")
        exit(1)


zshrc_path = Path.home() / ".zshrc"
shelloracle_zsh_dest = Path.home() / ".shelloracle.zsh"


def write_shelloracle_zsh() -> None:
    zsh_path = Path(__file__).parent.absolute() / "shelloracle.zsh"
    shelloracle_zsh = zsh_path.read_bytes()
    shelloracle_zsh_dest.write_bytes(shelloracle_zsh)
    print_info(f"Successfully wrote key bindings to {replace_home_with_tilde(shelloracle_zsh_dest)}")


def update_zshrc() -> None:
    zshrc_path.touch(exist_ok=True)
    with zshrc_path.open("r") as file:
        zshrc = file.read()
    line = f"[ -f {shelloracle_zsh_dest} ] && source {shelloracle_zsh_dest}"
    if line not in zshrc:
        with zshrc_path.open("a") as file:
            file.write("\n")
            file.write(line)
    print_info(f"Successfully updated {replace_home_with_tilde(zshrc_path)}")


def bootstrap() -> None:
    with create_app_session_from_tty():
        ensure_zsh()

        if confirm("Enable terminal keybindings?", suffix=" ([y]/n) ") is False:
            return

        write_shelloracle_zsh()
        update_zshrc()


if __name__ == '__main__':
    bootstrap()
