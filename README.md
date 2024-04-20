# Statsbomb demo

Small demo of a Statsbomb pipeline

## Usage

A small script is included to start the data processing:

```sh
python cli.py
```

This script supports the following flags:

```sh
# download the events data
# (this will take long due to throttling of GitHub)
python cli.py --download
``` 

The script allows for processing the data in parallel using threads:

```sh
python cli.py --threads=4
```

This reads and processes the events data on 4 threads.
However, be a little bit careful with this.
It does not allow to be closed during the operation.