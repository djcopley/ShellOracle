[![Tests](https://github.com/djcopley/ShellOracle/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/djcopley/ShellOracle/actions/workflows/tests.yml)
[![PyPI version](https://badge.fury.io/py/shelloracle.svg)](https://badge.fury.io/py/shelloracle)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/shelloracle.svg)](https://pypi.python.org/pypi/shelloracle/)
[![Downloads](https://static.pepy.tech/badge/shelloracle/month)](https://pepy.tech/project/shelloracle)

# ShellOracle

ShellOracle is an innovative terminal utility designed for intelligent shell command generation, bringing a new level of
efficiency to your command-line interactions. ShellOracle currently supports Ollama, LocalAI, and OpenAI!

![ShellOracle](https://i.imgur.com/mg1rCzd.gif)

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

Meet ShellOracle—a handy tool that makes working with the command line a bit smoother. This terminal utility lets you
create shell commands by describing what you want to do in plain language. ShellOracle simplifies the process of
crafting complex commands by removing the need to google and comb man pages.

**Why ShellOracle?**

* **No More Memorizing:** Forget about remembering complex shell commands. Just tell ShellOracle what you need, and
  it'll generate the command for you.

* **Save Time, Stay Focused:** Say goodbye to manual command crafting. ShellOracle helps you save time and concentrate
  on what really matters by using natural language descriptions.

* **Adaptable to Your Needs:** Whether it's a quick one-liner or a sequence of commands, ShellOracle is flexible. It
  supports Unix pipes and keeps track of your command history.

* **Your Control, Your Way:** Run ShellOracle as a self-hosted utility to have complete control. Tailor it to your
  preferences and make it work just the way you want.

Give it a try and see how it fits into your workflow!

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
    ```shell
    python3 -m pip install shelloracle
    ```
2. Next, run `shelloracle init` and follow the prompts
    ```shell
    python3 -m shelloracle init
    ```

**Ollama**

> [!IMPORTANT]
> ShellOracle uses [Ollama](https://ollama.ai/) as its default LLM provider. If you are using the default configuration,
> the following steps are required.

3. Install [Ollama](https://ollama.ai/)
4. Download the default model
    ```shell
    ollama pull codellama:13b
    ```

## Usage

ShellOracle is designed to be used as a BASH/ZSH widget activated by the CTRL+F keyboard shortcut.

1. Press CTRL+F
2. Describe your command
3. Press Enter

The generated command will be inserted into your shell prompt after a brief processing period.

### Ollama

Before using ShellOracle with Ollama, pull the model you want to use. The default model is `codellama:13b`. To pull the
default model, run:

```shell
ollama pull codellama:13b
```

### OpenAI

To use ShellOracle with the OpenAI provider, create an [API key](https://platform.openai.com/account/api-keys). Edit
your `~/.shelloracle/config.toml` to change your provider and enter your API key.

### LocalAI



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

Set the `provider` key to specify the Language Model (LLM) backend, with options currently including "Ollama", 
"LocalAI", and "OpenAI."

### Provider Settings

Provider-specific configurations are handled through the `[provider.*]` keys. Here's an
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

ShellOracle supports BASH and ZSH on macOS and Linux.

### Hardware

For cloud providers like OpenAI, there are no specific system requirements.

If self-hosting, system requirements vary based on the model used. Refer to the Ollama model registry for more
information.

## Feedback

Encountered problems? [File an issue](https://github.com/djcopley/ShellOracle/issues/new). Feature requests are welcome,
and contributions can be made by opening a pull request.
