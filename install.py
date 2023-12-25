import os
import shutil
import subprocess
from pathlib import Path

from prompt_toolkit import print_formatted_text
from prompt_toolkit.application import create_app_session_from_tty
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.shortcuts import confirm

shelloracle_zsh = """\
# Define the function shelloracle-widget
shelloracle-widget() {
  # Set options and suppress any error messages
  setopt localoptions noglobsubst noposixbuiltins pipefail no_aliases 2> /dev/null

  # Run the shelloracle python module and store the result in the "selected" array
  local selected=( $(SHOR_DEFAULT_PROMPT=${LBUFFER} python3 -m shelloracle) )

  # Get the return status of the last executed command
  local ret=$?

  # Reset the prompt
  zle reset-prompt

  # Set the BUFFER variable to the selected result
  BUFFER=$selected

  # Set the CURSOR position at the end of BUFFER
  CURSOR=$#BUFFER

  # Return the status
  return $ret
}

# Register the function as a ZLE widget
zle -N shelloracle-widget

# Install the ZLE widget as a keyboard shortcut Ctrl+F
bindkey '^F' shelloracle-widget
"""


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
shelloracle_zsh_path = Path.home() / ".shelloracle.zsh"


def write_shelloracle_zsh():
    with shelloracle_zsh_path.open("w") as f:
        f.write(shelloracle_zsh)
    print_info(f"Successfully wrote key bindings to {replace_home_with_tilde(shelloracle_zsh_path)}")


def update_zshrc():
    with zshrc_path.open("r") as file:
        zshrc = file.read()
    line = f"[ -f {shelloracle_zsh_path} ] && source {shelloracle_zsh_path}"
    if line not in zshrc:
        with zshrc_path.open("a") as file:
            file.write("\n")
            file.write(line)
    print_info(f"Successfully updated {replace_home_with_tilde(zshrc_path)}")


if __name__ == "__main__":
    with create_app_session_from_tty():
        ensure_zsh()
        install_shelloracle()

        if (install_shell_scripts := confirm("Install zsh scripts?", suffix=" ([y]/n) ")) is False:
            exit(0)

        write_shelloracle_zsh()
        update_zshrc()
