tile-stat
=========

Gather and process usage statistics for map tiles hosted by web servers nginx and Apache

Usage
-----

```
gather.py [-h] [-o FILE] [-c NAME] source
```

### Positional arguments
`source` — log file to process

### Optional arguments

* `-h`, `--help` — show help message and exit
* `-o` _FILE_, `--output` _FILE_ — output raw data to file, format are choosing by extension (csv, xls, xlsx, htm, html, json)
* `-c` _NAME_, `--column` _NAME_ — process desired column (possible names are `style` and `zoom`)

Requirements
------------

* Python 3
* [matplotlib](https://matplotlib.org/), [pandas](https://pandas.pydata.org/) — _required_,
* openpyxl or xlwt — _optional for Excel output_.

### Install dependencies

```
pip install -r requirements.txt
```

Author
------

Alexander Sapozhnikov
<shoorick@cpan.org>
http://shoorick.ru/

