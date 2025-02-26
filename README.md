# Ping_Sweeper_Tool

## Overview
The **Simple Ping Sweep Tool** is a Python-based utility that allows users to perform a ping sweep on a list of IP addresses or domain names. It utilizes the `ping3` library to check the reachability of targets and provides a summary of response times and packet statistics.

## Features
- Multi-threaded ping sweeping for faster execution
- Supports both IP addresses and DNS hostnames
- Displays reachability status and response times
- Provides ping statistics including sent, received, lost packets, and round-trip times
- User-friendly CLI with color-coded output

Usage

Run the script using the following command:
```sh
python ping_sweep.py -i <IP1> <IP2> ... <IPn>
```
Example

To scan multiple IP addresses:
```sh
    python ping_sweep.py -i 8.8.8.8 8.8.4.4 example.com
```

Command-Line Arguments

| Argument | Description |
| -------- | ------- |
| -i, --input | List of IP addresses or DNS names to sweep (required) |
| -h, --help | Show help message and usage information |

