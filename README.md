# BashSenpai

BashSenpai is a command-line tool that brings the power of the BashSenpai API to your terminal. It allows you to ask questions and receive informative responses related to shell scripting, making it a valuable resource for both beginners and experienced users.

<div align="center">
    <br>
    <img src="media/screenshot.png" alt="Example usage of the BashSenpai command-line interface" title="BashSenpai in action">
</div>
<p align="center">
    <a href="https://bashsenpai.com/"><b>BashSenpai.com</b></a>
</p>


## Features

- Supercharged by ChatGPT.
- Refined prompts that take advantage of a multi-step self-refletion process for best possible results.
- Ask follow-up questions without providing any contxt; our API takes care of including your log history.
- Always get answers that can be run directly in the terminal along with helpful comment explanations.
- Nicely formatted responses with customizable colors for improved readability.
- Change the persona of BashSenpai to add a touch of fun and personality to your interactions.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Roadmap](#roadmap)

## Installation

We maintain up-to-date packages for the following Operating Systems and Linux distributions:

### Ubuntu-based

Install from PPA:

```shell
sudo add-apt-repository ppa:bashsenpai/cli
sudo apt update
sudo apt install senpai-cli
```

Supported distributions: **Ubuntu 22.04 LTS** or later, **Linux Mint 21** or later, **Pop!_OS 22.04**, **KDE neon 5.27**, **elementary OS 7**.

### RPM-based

Install from Copr:

```shell
sudo dnf copr enable bashsenpai/cli
sudo dnf install senpai-cli
```

Supported distributions: **Fedora 38**, **RHEL 9**, **CentOS Stream 9**.

### Arch Linux-based

Install from AUR:

```shell
yay -S senpai-cli
```

Supported distributions: any Arch-based rolling-release distribution that supports installing packages from the AUR. **Manjaro** should also work, but it's untested.

### MacOS

Install with Homebrew:

```shell
brew tap BashSenpai/core
brew install senpai-cli
```

### Windows

Download: **[Installer](https://bashsenpai.com/latest/BashSenpaiSetup.exe)**.

## Usage

To use BashSenpai, run the following command:

```shell
senpai [options] prompt
```

The `prompt` argument represents the question or a special command you want to execute. BashSenpai will send the prompt to the BashSenpai API and display the response in your terminal.

### Options

* `-n, --new`: ignores the previous history when sending a question. Use this option if you want to start fresh with each prompt.

### Examples

* Login to BashSenpai:

```shell
senpai login
```

This command prompts you to enter your authentication token and stores it in the configuration file.

* Change the persona of BashSenpai:

```shell
senpai become angry pirate
```

This command changes the persona of BashSenpai to an angry pirate, adding a fun twist to the responses. You are not limitted to a certain list of characters and can write anything you want here. Our smartly-designed backend API with multi-level prompts and instructions makes sure all crazy ideas can integrate nicely with the core functionality of the tool.

* Ask a question:

```shell
senpai how to disable SSH connections
```

This command sends the question to the BashSenpai API and displays an informative and well-formatted response.

## Configuration

* `--command-color`: sets the color of the commands in the responses. Valid options are: black, white, gray, red, greeen, yellow, blue, magenta and cyan. There are also brighter versions of each color, for example: "bright blue". You can also make colors bold, for example: "bold red" or "bold bright cyan".

* `--comment-color`: sets the color of the comments in the responses.

* `--run`, `--no-run`: sets whether to show the menu prompt to execute each returned command.

* `--meta`, `--no-meta`: sets whether to send OS metadata to improve the responses. Currently this includes OS type and version (all OSes), shell type (macOS and Linux), and architecture (macOS). Users may choose to disable this feature either for privacy reasons, or in cases where it produces unwanted results (for example if the tool is running on a Windows machine, but the user expects answers about Linux).

Please check our [Roadmap](#roadmap) section for new and planned features as we develop the configuration options. We are committed to making BashSenpai user-friendly, flexible and easily-configurable and we value your initial feedback. If you have any suggestions or feature requests, don't hesitate to use the appropriate tools provided by GitHub to share your thoughts with us.

## Contributing

We welcome contributions to enhance and improve the BashSenpai tool. If you have any ideas, bug reports, or feature requests, please open an issue on the GitHub repository. Feel free to fork the repository, make changes, and submit pull requests.

To contribute to BashSenpai, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and ensure that the code doesn't break any core functionality of the tool.
4. Commit your changes and push them to your forked repository.
5. Submit a pull request, providing a clear explanation of the changes you've made.

We appreciate your interest in BashSenpai and will do our best to review any pull requests in a timely manner and keep an open discussion of what our feature goals are to make the contribution process easier and smooth for both parties.

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for more information.

## Roadmap

### Version 0.80 (planned)

- [x] Better error handling: print better output on receiving an error from the API
- [x] Extra context: provide optional information about your own environment to improve the results
- [ ] Multi-language support: provided by ChatGPT

### Version 0.75 (finished)

- [x] MacOS build: proper MacOS integration
- [x] Windows build: native build script with an installer
- [x] Command execution: execute any provided list of commands directly in the terminal
- [x] Configurable color schemes: change the default colors so they fit better with your terminal configuration

### Other planned features

TBD.

## Maintainers

This project is maintained by:

- [Bogdan Tatarov](https://github.com/btatarov)
- [Nikolay Dyankov](https://github.com/nikolaydyankov)

We welcome contributions from the community. If you have any questions, suggestions, or bug reports, please feel free to reach out to any of the maintainers.
