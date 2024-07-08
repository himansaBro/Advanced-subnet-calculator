# Advanced Subnet Calculator

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Overview

Advanced Subnet Calculator is a CLI tool written in Python for calculating IPv4 subnets. This tool supports both standard subnetting and Variable Length Subnet Masking (VLSM). It is designed to help network administrators and enthusiasts efficiently manage and allocate IP addresses within a network.

## Features

- Convert decimal to 8-bit binary and vice versa
- Binary counting for subnet calculations
- Generate subnets based on the main network address, CIDR, and the number of subnets
- Calculate subnet masks, network addresses, broadcast addresses, and maximum nodes
- Support for both standard subnetting and VLSM
- Input validation for IP addresses and subnet counts

## Requirements

- Python 3.10 or higher
- Compatible with Windows, Linux, and macOS

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/himansaBro/Advanced-subnet-calculator.git
    cd Advanced-subnet-calculator
    ```

2. Run the script:
    ```bash
    python3 subnet_calculator.py
    ```

## Usage

1. **Standard Subnetting**
    ```plaintext
    Enter IP/CIDR..(e to exit)..............: 192.168.1.0/24
    Enter number of Subnets,0 for no subnets: 4
    Use VLSM Subnetting(y=yes/n=no/i=info)..: n
    ```

    Output:
    ```plaintext
    Main # 192.168.1.0/24
        -Nodes            : 256
        -Subnet Mask      : 255.255.255.0
        -Network Adress   : 192.168.1.0
        -Brodcast Adress  : 192.168.1.255 

    Subnet # 1 	 192.168.1.0 / 26
        -Nodes            : 64
        -Subnet Mask      : 255.255.255.192
        -Network Adress   : 192.168.1.0
        -Brodcast Adress  : 192.168.1.63 
    ```

2. **VLSM Subnetting**
    ```plaintext
    Enter IP/CIDR..(e to exit)..............: 192.168.1.0/24
    Enter number of Subnets,0 for no subnets: 6
    Use VLSM Subnetting(y=yes/n=no/i=info)..: y
    ```

    Output:
    ```plaintext
    Main # 192.168.1.0/24
        -Nodes            : 256
        -Subnet Mask      : 255.255.255.0
        -Network Adress   : 192.168.1.0
        -Brodcast Adress  : 192.168.1.255 

    Subnet # 1 	 192.168.1.128 / 26
        -Nodes            : 64
        -Subnet Mask      : 255.255.255.192
        -Network Adress   : 192.168.1.128
        -Brodcast Adress  : 192.168.1.191
        -Subnet Level     : 0 
    ```

## Subnetting Methods

### Standard Subnet Masking (Normal Way)
This method is simpler and creates equal-sized subnets. It may lead to IP address wastage if the number of required subnets is not a power of 2.

### Variable Length Subnet Masking (VLSM)
This method allows for subnets of varying sizes, making efficient use of IP addresses. It is more flexible but also more complex.

## Input Validation

The tool includes checks for:
- Valid IP addresses and CIDR notation
- Valid subnet counts that the network can handle

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments

- Developed by Himansa [CodeHack] (github.com/himansaBro)
- Inspired by network administration needs and IP address management

## Contact

For suggestions, comments, or contributions, please contact [himansarajapacksha@gmail.com](mailto:himansarajapacksha@gmail.com).

