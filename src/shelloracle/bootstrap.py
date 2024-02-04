import inspect
import shutil
from pathlib import Path

from prompt_toolkit import print_formatted_text, prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.shortcuts import confirm

from .config import Configuration
from .providers import Provider, Setting, list_providers, get_provider


def print_info(info: str) -> None:
    print_formatted_text(FormattedText([("ansiblue", info)]))


def print_warning(warning: str) -> None:
    print_formatted_text(FormattedText([("ansiyellow", warning)]))


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


def get_settings(provider: Provider) -> list[tuple[str, Setting]]:
    settings = inspect.getmembers(provider, predicate=lambda p: isinstance(p, Setting))
    return settings


def write_shelloracle_config(provider, settings):
    configuration = (
        "[shelloracle]\n"
        "provider = %(provider)s\n"
        "\n"
        "[provider.%(provider)s]\n"
    ) % {"provider": provider.name}

    for setting in settings:
        setting_line = "%(name)s = %(value)s\n" % {"name": setting[0], "value": setting[1]}
        configuration += setting_line

    Configuration.filepath.write_text(configuration)


def install_keybindings() -> None:
    if not (shells := get_installed_shells()):
        print_warning("Cannot install keybindings: no compatible shells found. "
                      f"Supported shells: {', '.join(supported_shells)}")
        return
    if confirm("Enable terminal keybindings and update rc?", suffix=" ([y]/n) ") is False:
        return
    for shell in shells:
        write_script_home(shell)
        update_rc(shell)


def user_configure_settings(provider: Provider) -> list[tuple[str, str]]:
    settings = []
    for name, setting in get_settings(provider):
        value = prompt(f"{name}: ", default=str(setting.default))
        settings.append((name, value))
    return settings


def user_select_provider() -> Provider:
    providers = list_providers()
    completer = WordCompleter(providers, ignore_case=True)
    selected_provider = prompt(f"Choose your LLM provider ({', '.join(providers)}): ", completer=completer)
    case_insensitive_map = {p.lower(): p for p in providers}
    selected_provider = case_insensitive_map[selected_provider.lower()]
    provider = get_provider(selected_provider)
    return provider


def bootstrap_shelloracle() -> None:
    """Bootstrap shelloracle"""
    provider = user_select_provider()
    settings = user_configure_settings(provider)
    write_shelloracle_config(provider, settings)
    install_keybindings()
