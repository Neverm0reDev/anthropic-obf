# Anthropic Python Obfuscator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<p align="center">
  <img src="https://i.imgur.com/FAf6OPR.png" alt="Anthropic Logo" width="400">
</p>

## Overview

Anthropic is a powerful Python script obfuscator designed to protect your Python source code through multiple layers of encryption and obfuscation. It transforms your readable Python code into a complex, encrypted format that is extremely difficult to reverse-engineer while maintaining full functionality.

## Features

- **Multi-layered Protection**: Applies three distinct layers of obfuscation techniques
- **Random Variable Generation**: Creates unique, random variable names for each obfuscation session
- **Custom Encryption**: Implements custom string encryption with random keys
- **Marshal Compilation**: Compiles code and dumps it using Python's marshal module
- **Code Camouflage**: Disguises obfuscated code with misleading class structures
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/anthropic-obfuscator.git

# Navigate to the project directory
cd anthropic-obfuscator

# Install dependencies
pip install pystyle
```

## Usage

```bash
# Run the obfuscator
python anthropic.py
```

1. When prompted, drag and drop the Python file you want to obfuscate into the terminal.
2. The obfuscator will process your file through multiple layers of protection.
3. The obfuscated file will be saved with the prefix `obf-` in the same directory.

## How It Works

Anthropic applies three sophisticated layers of obfuscation:

### Layer 1
- Splits the code into random chunks
- Encrypts each chunk using a random key
- Shuffles the encrypted chunks
- Creates lambda functions to dynamically reconstruct the original code at runtime

### Layer 2
- Compiles the obfuscated code using Python's built-in `compile()` function
- Dumps the compiled code using the `marshal` module

### Layer 3
- Splits the marshalled bytecode into manageable chunks
- Embeds the chunks into a camouflaged class structure
- Adds misdirection code to make analysis more difficult
