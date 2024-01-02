import os
import shutil
import subprocess
import zipfile
from pathlib import Path

from prompt_toolkit import print_formatted_text
from prompt_toolkit.application import create_app_session_from_tty
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.shortcuts import confirm


def print_info(info: str) -> None:
    print_formatted_text(FormattedText([("ansiblue", info)]))


def print_error(error: str) -> None:
    print_formatted_text(FormattedText([("ansired", error)]))


def pip_output(text: str) -> None:
    print_formatted_text(FormattedText([("ansigray", text)]), end="")


def replace_home_with_tilde(path: Path) -> Path:
    relative_path = path.relative_to(Path.home())
    return Path("~") / relative_path


def ensure_zsh():
    shell = os.environ.get("SHELL")
    if "zsh" not in shell:
        print_error(f"'{shell}' is currently unsupported. "
                    f"Please open an issue https://github.com/djcopley/ShellOracle/issues.")
        exit(1)


def install_shelloracle():
    print_info("Installing shelloracle")
    python = shutil.which("python3")
    pip = subprocess.Popen([python, "-m", "pip", "install", "--upgrade", "shelloracle"],
                           stdout=subprocess.PIPE, text=True)
    for line in pip.stdout.readlines():
        pip_output(line)
    if (ret := pip.wait()) == 0:
        print_info("Successfully installed shelloracle")
    else:
        print_error(f"Unable to install shelloracle")
        exit(ret)


zshrc_path = Path.home() / ".zshrc"
shelloracle_zsh_dest = Path.home() / ".shelloracle.zsh"


def read_shelloracle_zsh():
    working_dir = Path(__file__).parent.absolute()
    zsh_path = "shelloracle.zsh"
    if working_dir.suffix == ".pyz":
        with zipfile.ZipFile(working_dir, "r") as zip_app:
            shelloracle_zsh = zip_app.read(zsh_path)
    else:
        shelloracle_zsh = (working_dir / zsh_path).read_bytes()
    return shelloracle_zsh


def write_shelloracle_zsh():
    shelloracle_zsh = read_shelloracle_zsh()
    shelloracle_zsh_dest.write_bytes(shelloracle_zsh)
    print_info(f"Successfully wrote key bindings to {replace_home_with_tilde(shelloracle_zsh_dest)}")


def update_zshrc():
    with zshrc_path.open("r") as file:
        zshrc = file.read()
    line = f"[ -f {shelloracle_zsh_dest} ] && source {shelloracle_zsh_dest}"
    if line not in zshrc:
        with zshrc_path.open("a") as file:
            file.write("\n")
            file.write(line)
    print_info(f"Successfully updated {replace_home_with_tilde(zshrc_path)}")


def install():
    with create_app_session_from_tty():
        ensure_zsh()
        install_shelloracle()

        if confirm("Enable terminal keybindings?", suffix=" ([y]/n) ") is False:
            exit(0)

        write_shelloracle_zsh()
        update_zshrc()


if __name__ == '__main__':
    install()