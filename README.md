<p align="center">
  <img src="https://i.imgur.com/IsQYInJ.png" alt="ShellOracle logo"/>
</p>

<h1 align="center">ShellOracle</h1>

<p align="center">
  <a href="https://github.com/djcopley/ShellOracle/actions/workflows/tests.yml">
      <img src="https://github.com/djcopley/ShellOracle/actions/workflows/tests.yml/badge.svg?branch=main" alt="Tests">
  </a>
  <a href="https://badge.fury.io/py/shelloracle">
      <img src="https://badge.fury.io/py/shelloracle.svg" alt="PyPI version">
  </a>
  <a href="https://pypi.python.org/pypi/shelloracle/">
      <img src="https://img.shields.io/pypi/pyversions/shelloracle.svg" alt="PyPI Supported Python Versions">
  </a>
  <a href="https://pepy.tech/project/shelloracle">
      <img src="https://static.pepy.tech/badge/shelloracle" alt="Downloads">
  </a>
</p>

ShellOracle is an innovative terminal utility designed for intelligent shell command generation, bringing a new level of
efficiency to your command-line interactions. ShellOracle currently supports Ollama, LocalAI, and OpenAI!

![ShellOracle](https://i.imgur.com/GJX3eEq.gif)

Show your support for ShellOracle and keep an eye out for exciting new developments by clicking the ⭐ and a 👀!

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Providers](#providers)
- [Configuration](#configuration)
- [System Requirements](#system-requirements)
- [Feedback](#feedback)

## Features

Key features of ShellOracle include:

* Seamless shell command generation from written descriptions
* Command history for easy reference
* Unix pipe support for advanced command chaining
* Self-hosted for full control over your environment
* Highly configurable to adapt to your preferences

## Installation

Installing ShellOracle is easy!

1. [pipx](https://pipx.pypa.io/latest/) install the `shelloracle` package
    ```shell
    pipx install shelloracle
    ```
2. Configure ShellOracle and follow the prompts
    ```shell
    shor configure
    ```
3. Refer to the [providers](#providers) section for specific details regarding your chosen provider.

Upgrading to the latest version of ShellOracle is just as simple!

1. pipx upgrade the `shelloracle` package
    ```shell
   pipx upgrade shelloracle
   ```

*Installation with `pip` is supported, however, `pipx` is preferred for its automatic environment isolation.*

## Usage

ShellOracle is designed to be used as a BASH/ZSH widget activated by the CTRL+F keyboard shortcut.

1. Press CTRL+F
2. Describe your command
3. Press Enter

The generated command will be inserted into your shell prompt after a brief processing period.

### Other ways to run ShellOracle

ShellOracle can be run as a Python module with `python3 -m shelloracle` or using its entrypoint `shor`, however,
running ShellOracle with this method will not automatically insert the result into your shell prompt.

### Tips

1. If you press CTRL+F with text in your ZLE buffer, all text left of your cursor will carry over to your ShellOracle
   prompt.
2. ⬆️ arrow and ⬇️ arrow cycle through your prompt history.
3. ShellOracle can be chained with other commands; try: `echo "find all the python files in my cwd" | shor`

## Providers

### Ollama

Before using ShellOracle with Ollama, pull the model you chose in the configure step.
For example, if you chose `dolphin-mistral`, run:

```shell
ollama pull dolphin-mistral
```

Refer to the [Ollama docs](https://ollama.ai) for installation, available models, and usage.

### OpenAI

To use ShellOracle with the OpenAI provider, create an [API key](https://platform.openai.com/account/api-keys). Edit
your `~/.shelloracle/config.toml` to change your provider and enter your API key.

### LocalAI

Refer to the [LocalAI docs](https://localai.io/) for installation, available models, and usage.

## Configuration

ShellOracle's configuration is your gateway to tailoring the utility to match your preferences and requirements.
The `~/.shelloracle/config.toml` file serves as the control center for customizing various aspects of ShellOracle's
behavior.

## System Requirements

### Software

ShellOracle supports BASH and ZSH on macOS and Linux.

### Hardware

For cloud providers like OpenAI, there are no hardware requirements.

If running locally, refer to your model for hardware requirements.

## Feedback

Encountered problems? [File an issue](https://github.com/djcopley/ShellOracle/issues/new). Feature requests are welcome,
and contributions can be made by opening a pull request.

## License

This software is licensed under the GPLv3 license.
