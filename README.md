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
- Interact with the BashSenpai API to ask questions and receive detailed answers.
- Store and manage your interaction history for future reference.
- Customize the persona of BashSenpai to add a touch of fun and personality to your interactions.
- Beautifully formatted responses using colors and comments for improved readability.

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

### RPM-based (Fedora, CentOS Stream, RHEL)

Install from Copr:

```shell
sudo dnf copr enable bashsenpai/cli
sudo dnf install senpai-cli
```

### Arch Linux-based

Install from AUR:

```shell
yay -S senpai-cli
```

### MacOS

Istall with Homebrew:

```shell
brew tap BashSenpai/homebrew-core
brew install senpai-cli
```

### Windows

Download: **[Installer](https://github.com/BashSenpai/cli/releases/download/v0.72b/BashSenpaiSetup.exe)**.

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

### Version 0.80

- [ ] Extra context: provide extra optional information about your own environment to improve the results
- [ ] Multi-language support: provided by ChatGPT. If you have interest in helping us improve these, open a new pull request

### Version 0.75 (planned)

- [x] MacOS build: proper MacOS integration
- [x] Windows build: native build script with an installer
- [ ] Command execution: execute any provided list of commands directly in the terminal with an optional feature to edit each one beforehand
- [ ] Configurable color schemes: ability to change the default colors so they fit better with your terminal configuration

### Other planned features

TBD.

## Maintainers

This project is maintained by:

- [Bogdan Tatarov](https://github.com/btatarov)
- [Nikolay Dyankov](https://github.com/nikolaydyankov)

We welcome contributions from the community. If you have any questions, suggestions, or bug reports, please feel free to reach out to any of the maintainers.
