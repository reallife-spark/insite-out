---
title: jetson-stats-repo
source_url: https://github.com/rbonghi/jetson_stats
fetched_at: 2026-11-26T08:23:37+00:00
engine: defuddle
defuddle_version: 0.19.13
content_sha256: 4587c5d13cd3e4f7666f761049c0ec961e4cc23f1b435e9444f55afa9b22df1a
status: captured
depth: 1
root_source: https://share.google/aimode/mhgoDgYotEKcIHMGo
---

## jetson-stats

[![PyPI - Downloads](https://camo.githubusercontent.com/19abb1cb8eea121a6538b4056144fbf4d526587ffcf86f5605e47ba590b388e6/68747470733a2f2f696d672e736869656c64732e696f2f707970692f64772f6a6574736f6e2d73746174732e737667)](https://pypistats.org/packages/jetson-stats) [![PyPI version](https://camo.githubusercontent.com/9c6284db051a31497f172f2d8bdaa77a84ef723e8ef542e3f3eb6f83727b5e74/68747470733a2f2f62616467652e667572792e696f2f70792f6a6574736f6e2d73746174732e737667)](https://badge.fury.io/py/jetson-stats) [![PyPI - Python Version](https://camo.githubusercontent.com/f856e9918c2b43cb205b120813e116e0f90230cfc7224bc35e576f23c06a0298/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f6a6574736f6e2d73746174732e737667)](https://www.python.org/) [![PyPI - Format](https://camo.githubusercontent.com/187ddf91c9fa3e509ad4b7ff9ee0427473300aaaecdde22bcf0459b6ed5ce2ce/68747470733a2f2f696d672e736869656c64732e696f2f707970692f666f726d61742f6a6574736f6e2d73746174732e737667)](https://pypi.org/project/jetson-stats/) [![GitHub](https://camo.githubusercontent.com/5bd1c5d134648fc1cfcde9aa5e5cb107006f2e0c4af10400ed7c0981bf6f86a0/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f72626f6e6768692f6a6574736f6e5f7374617473)](https://github.com/rbonghi/jetson_stats/blob/master/LICENSE) [![jetson-stats](https://camo.githubusercontent.com/c56a1c7046d7ea7979166c15de2e34fb8b023181d2afa977217e6270cf1851b6/68747470733a2f2f736e796b2e696f2f61647669736f722f707974686f6e2f6a6574736f6e2d73746174732f62616467652e737667)](https://snyk.io/advisor/python/jetson-stats) [![Docker Image Size (tag)](https://camo.githubusercontent.com/b9a47a1fad2de303456a6591cc7d02ab990a530b314cecf1ccdef3d7947b5cb4/68747470733a2f2f696d672e736869656c64732e696f2f646f636b65722f696d6167652d73697a652f72626f6e6768692f6a6574736f6e5f73746174732f6c6174657374)](https://hub.docker.com/r/rbonghi/jetson_stats) [![Docker Pulls](https://camo.githubusercontent.com/799ce7bde09cbb4b2c96ddd39a86e56592cda6a97af0399b6922e605a4a4ad57/68747470733a2f2f696d672e736869656c64732e696f2f646f636b65722f70756c6c732f72626f6e6768692f6a6574736f6e5f7374617473)](https://hub.docker.com/r/rbonghi/jetson_stats) [![CI & CD](https://github.com/rbonghi/jetson_stats/workflows/CI%20&%20CD/badge.svg)](https://github.com/rbonghi/jetson_stats/actions?query=workflow%3A%22CI+%26+CD%22) [![CodeQL](https://github.com/rbonghi/jetson_stats/actions/workflows/github-code-scanning/codeql/badge.svg?branch=master)](https://github.com/rbonghi/jetson_stats/actions/workflows/github-code-scanning/codeql)

[![Twitter Follow](https://camo.githubusercontent.com/0b7916702521cbf80373c1d9f02af48f8d39d06b39d2bae6c5435b90a7de010b/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f466f6c6c6f772d2534307261666661656c6c6f38362d3144413146323f6c6f676f3d74776974746572267374796c653d736f6369616c)](https://twitter.com/raffaello86) [![robo.panther](https://camo.githubusercontent.com/8132da490c8be747e7df4a778dde2d6e05a258ce56056dc4d619bdcc2ba7ff06/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f466f6c6c6f772d726f626f2e70616e746865722d4534343035463f7374796c653d736f6369616c266c6f676f3d696e7374616772616d)](https://www.instagram.com/robo.panther/) [![Join our Discord](https://camo.githubusercontent.com/cc8ff52f7fcc3a5c46a12c706f6151599874f768256f29c5a3b0759a55539313/68747470733a2f2f696d672e736869656c64732e696f2f646973636f72642f313036303536333737313034383836313831373f636f6c6f723d253233373238396461266c6162656c3d646973636f7264)](https://discord.gg/BFbuJNhYzS)

**jetson-stats** is a package for **monitoring** and **control** your [NVIDIA Jetson](https://developer.nvidia.com/buy-jetson) \[Thor, Orin, Xavier, Nano, TX\] series.

jetson-stats is a powerful tool to analyze your board, you can use with a stand alone application with `jtop` or import in your python script, the main features are:

- Decode hardware, architecture, L4T and NVIDIA Jetpack
- Monitoring, CPU, GPU, Memory, Engines, fan
- Control NVP model, fan speed, jetson\_clocks
- Importable in a python script
- Dockerizable in a container
- Do not need super user
- Tested on many different hardware configurations
- Works with all NVIDIA Jetpack

## Install

```
sudo apt update
sudo apt install python3-pip python3-setuptools -y
```

### Option 1: jetson-stats can be installed with pip, but need superuser:

```
sudo pip3 install -U jetson-stats
```

### Option 2: Install directly from GitHub

```
sudo pip3 install git+https://github.com/rbonghi/jetson_stats.git
```

### Option 3: Ubuntu 24.04

```
sudo pip3 install --break-system-packages -U jetson-stats
```

or

```
sudo pip3 install --break-system-packages git+https://github.com/rbonghi/jetson_stats.git
```

### Option 4: Run jtop with or without sudo, and install without --break-system-packages

This installation method works on all Jetson Developer Kits. *NOTE: For Jetson AGX Thor Dev Kit follow this*

```
sudo -v
curl -LsSf https://raw.githubusercontent.com/rbonghi/jetson_stats/master/scripts/install_jtop_torun_without_sudo.sh | bash
```

### Upgrade jtop

```
sudo -v
curl -LsSf https://raw.githubusercontent.com/rbonghi/jetson_stats/master/scripts/upgrade-jtop.sh | bash
```

---

## Run

Start jtop it's pretty simple just write `jtop`!

```
jtop
```

A simple interface will appear on your terminal, more capabilities are documented at [*jtop*](https://rnext.it/jetson_stats/jtop/jtop.html) page.

[![jtop](https://github.com/rbonghi/jetson_stats/raw/master/docs/images/jtop.gif)](https://github.com/rbonghi/jetson_stats)

## Library

You can use jtop such a python library to integrate in your software

```
from jtop import jtop

with jtop() as jetson:
    # jetson.ok() will provide the proper update frequency
    while jetson.ok():
        # Read tegra stats
        print(jetson.stats)
```

You can also use jtop with your *virualenv*!

More information available at [*advanced usage*](https://rnext.it/jetson_stats/advanced-usage.html) page.

## Docker

You can run directly in Docker jtop, you need only to:

1. Install jetson-stats on your **host**
2. Install jetson-stats on your container as well
3. Pass to your container `/run/jtop.sock:/run/jtop.sock`

You can try running this command

```
docker run --rm -it -v /run/jtop.sock:/run/jtop.sock rbonghi/jetson_stats:latest
```

More information available at [*docker*](https://rnext.it/jetson_stats/docker.html) documentation page.

## Sponsorship

If your company benefits from this library, please consider [💖 sponsoring its development](https://github.com/sponsors/rbonghi).

## Documentation

jetson-stats has usage and reference documentation at [https://rnext.it/jetson\_stats](https://rnext.it/jetson_stats), there is also a [🆘 troubleshooting](https://rnext.it/jetson_stats/troubleshooting.html) page.

## Community

jetson-stats has a [community Discord channel](https://discord.gg/BFbuJNhYzS) for asking questions and collaborating with other contributors. Drop by and say hello 👋
