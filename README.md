# Youtube Search Extension

> A [ulauncher](https://ulauncher.io/) extension

Uses selenium to visit YouTube and BeautifulSoup to parse response.

## Install `selenium` and `BeautifulSoup`

```bash
pip3 install beautifulsoup4==4.9.1
pip3 install selenium==3.141.0
```

If you use a different python environment (conda/pyenv/pipenv), Ulauncher will continue to use the system version. Install packages to the system version of python in that case.

```bash
/usr/bin/pip3 install beautifulsoup4==4.9.1
/usr/bin/pip3 install selenium==3.141.0
```

## Install chromium driver

For debian based distro (Ubuntu, Mint, etc):
```bash
sudo apt install chromium-chromedriver
```

Tested using `ChromeDriver 85.0.4183.102` on `Ubuntu 20.04.1 LTS`

## Search for YouTube Videos

![screenshot](screenshot.png)

Developed by [LifeOfCoding | Jimmy Rousseau](https://github.com/lifeofcoding)

Contributed by [Rabin](https://github.com/therj) |
[Code Something](https://github.com/cs-rjoshi)
