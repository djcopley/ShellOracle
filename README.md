# ShellOracle

ShellOracle is a terminal utility for intelligent shell command generation.

![ShellOracle](https://i.imgur.com/QM2LkAf.gif)

More exciting stuff coming soon so ⭐ and 👀️ to stay in the loop.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Feedback](#feedback)

## Introduction

ShellOracle is a terminal utility allows you to generate shell commands from a written description.

## Features

A few of the key features of ShellOracle:

* Generate shell commands from written description with ease
* Command history
* Unix pipe support
* Self-hosted
* Fully configurable

## Installation

To install ShellOracle, download and run the installer python zip application with the following one-liner:
```zsh
curl -sSL https://raw.githubusercontent.com/djcopley/ShellOracle/master/installer.pyz -o /tmp/installer.pyz && python3 /tmp/installer.pyz
```

> [!NOTE]  
> ShellOracle uses Ollama as its default LLM provider. Follow the installation instructions [here](https://ollama.ai/).

## Usage

ShellOracle is primarily intended to be used as a ZSH Line Editor widget activated by the CTRL+F keyboard shortcut. 

1. Press CTRL+F
2. Describe your command or goal
3. Press enter

The generated command will be inserted into your shell prompt after a few seconds!

#### Ollama

Before running ShellOracle with Ollama, you must first pull the model you want to use. By default, ShellOracle uses the 
`codellama:13b model`. To pull the default model run:

```zsh
ollama pull codellama:13b
```

#### OpenAI

To run ShellOracle with the OpenAI provider, you must first create an 
[API key](https://platform.openai.com/account/api-keys). Edit your ~/.shelloracle/config.toml to change your provider 
and enter your API key.

#### Tips

1. If you hit CTRL+F with text already in your ZLE buffer, all the text left of your cursor will be carried over to your ShellOracle prompt
2. UP_ARROW and DOWN_ARROW will cycle through your prompt history
3. ShellOracle can be chained together with other commands; try: `echo "find all the python files in my cwd" | shor`

#### Other ways to run ShellOracle

ShellOracle can also be run as a python module, with `python3 -m shelloracle`, or with its entrypoint `shor`.

> [!NOTE]
> You must add your `~/.local/bin` directory to your [PATH]() for the entrypoint to work. Additionally, running 
> ShellOracle with this method will not automatically insert the result into your shell prompt, so you'll have to 
> copy and paste.

## System Requirements

If you are using a cloud provider like OpenAI, there are no system requirements.

If you are self-hosting, system requirements vary depending on the model you are running. The Ollama model registry 
has more information about 

## Configuration

ShellOracle configuration is handled by the ~/.shelloracle/config.toml file. The configuration looks like this:

```toml
[shelloracle]
# Shell oracle configuration settings
provider = "Ollama"

[provider.Ollama]
# Provider settings
model = "codellama:13b"

[provider.OpenAI]
api_key = ""
model = "gpt-3.5-turbo"
```

Setting the `provider` key lets ShellOracle know what LLM backend to use. Currently, the options for this field are
"Ollama" and "OpenAI".

Provider specific configuration is handled through the `[Provider.NAME]` tags.

## Contributing

If you run into any problems, feel free to [file an issue](https://github.com/djcopley/ShellOracle/issues/new).
Feature requests are always welcome. If you wish to contribute, open a pull-request.
