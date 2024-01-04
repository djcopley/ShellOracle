# ShellOracle

ShellOracle is an innovative terminal utility designed for intelligent shell command generation, bringing a new level of
efficiency to your command-line interactions.

![ShellOracle](https://i.imgur.com/QM2LkAf.gif)

Explore our dynamic features and look forward to more exciting updates by giving us a ⭐ and a 👀

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [System Requirements](#system-requirements)
- [Feedback](#feedback)

## Introduction

In the ever-evolving landscape of command-line interfaces, ShellOracle emerges as a game-changer. This terminal utility
empowers users to effortlessly generate shell commands by simply describing their intentions. Whether you're a seasoned
developer or a command-line enthusiast, ShellOracle streamlines your workflow, making complex command creation an
intuitive and accessible process.

**Why ShellOracle?**

- **Intelligence at Your Fingertips:** No need to memorize intricate shell commands. Describe your task, and let
  ShellOracle intelligently generate the command for you.

- **Enhanced Productivity:** Say goodbye to manual command crafting. With ShellOracle, you can save time and focus on
  what matters by leveraging the power of natural language descriptions.

- **Versatile Integration:** Whether you're working on a quick one-liner or chaining multiple commands, ShellOracle
  adapts to your needs. Enjoy the flexibility of Unix pipe support and command history.

- **Self-hosted Control:** Take charge of your environment by running ShellOracle as a self-hosted utility. Full control
  means you tailor it to your preferences.

This is more than just a utility; it's a tool that transforms how you interact with the command line. With ShellOracle,
the language of the shell becomes more accessible, intuitive, and efficient.

## Features

Key features of ShellOracle include:

* Seamless shell command generation from written descriptions
* Command history for easy reference
* Unix pipe support for advanced command chaining
* Self-hosted for full control over your environment
* Highly configurable to adapt to your preferences

## Installation

Installing ShellOracle is easy!

1. First, pip install the `shelloracle` package
    ```zsh
    python3 -m pip install shelloracle
    ```
2. Next, run `shelloracle --init` and follow the prompts
    ```zsh
    python3 -m shelloracle --init
    ```

> [!NOTE]  
> If you chose Ollama as your LLM provider, you will need to install it from [here](https://ollama.ai/).

## Usage

ShellOracle is designed to be used as a ZSH Line Editor widget activated by the CTRL+F keyboard shortcut.

1. Press CTRL+F
2. Describe your command or goal
3. Press Enter

The generated command will be inserted into your shell prompt after a brief processing period.

### Ollama

Before using ShellOracle with Ollama, pull the model you want to use. The default model is `codellama:13b`. To pull the
default model, run:

```zsh
ollama pull codellama:13b
```

### OpenAI

To use ShellOracle with the OpenAI provider, create an [API key](https://platform.openai.com/account/api-keys). Edit
your `~/.shelloracle/config.toml` to change your provider and enter your API key.

### Other ways to run ShellOracle

ShellOracle can be run as a Python module with `python3 -m shelloracle` or using its entrypoint `shor`; however,
there are a few caveats with this method:
- Ensure your `~/.local/bin` directory is added to your PATH variable for the entrypoint to work.
- Running ShellOracle with this method will not automatically insert the result into your shell prompt.

### Tips

1. If you press CTRL+F with text in your ZLE buffer, all text left of your cursor will carry over to your ShellOracle
   prompt.
2. UP_ARROW and DOWN_ARROW cycle through your prompt history.
3. ShellOracle can be chained with other commands; try: `echo "find all the python files in my cwd" | shor`

## Configuration

ShellOracle's configuration is your gateway to tailoring the utility to match your preferences and requirements.
The `~/.shelloracle/config.toml` file serves as the control center for customizing various aspects of ShellOracle's
behavior.

### ShellOracle Settings

The `[shelloracle]` section in the configuration file lets you define global settings for ShellOracle:

```toml
[shelloracle]
provider = "Ollama"
```

Set the `provider` key to specify the Language Model (LLM) backend, with options currently including "Ollama" and 
"OpenAI."

### Provider Settings

Provider-specific configurations are handled through tags such as `[provider.Ollama]` or `[provider.OpenAI]`. Here's an
example for the Ollama provider:

```toml
[provider.Ollama]
host = "localhost"
port = 11434
model = "codellama:13b"
system_prompt = "..."
```

Change these options to match your desired configuration.

For OpenAI, if you opt for this provider, you'll need to provide
your [API key](https://platform.openai.com/account/api-keys):

```toml
[provider.OpenAI]
api_key = "your-api-key-here"
model = "gpt-3.5-turbo"
system_prompt = "..."
```

## System Requirements

### Software

ShellOracle supports ZSH on macOS and Linux. Bash support is planned; however, it is not currently 
supported.

### Hardware

For cloud providers like OpenAI, there are no specific system requirements.

If self-hosting, system requirements vary based on the model used. Refer to the Ollama model registry for more
information.

## Feedback

Encountered problems? [File an issue](https://github.com/djcopley/ShellOracle/issues/new). Feature requests are welcome,
and contributions can be made by opening a pull request.