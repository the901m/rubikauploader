# help command:
## Uploading:

```shell
$ python3 rubikauploader.py -h
usage: rubikauploader.py [-h] [-p PASSWORD] files [files ...]

positional arguments:
  files

options:
  -h, --help            show this help message and exit
  -p, --password PASSWORD

```
## Downloading:

```shell
$ python3 rubikadownloader.py -h
usage: rubikadownloader.py [-h] [-i INPUT] [-o OUTPUT]

Rubika Manifest to Aria2 Link Generator

options:
  -h, --help           show this help message and exit
  -i, --input INPUT    Path to manifest file (e.g., manifest_123.txt)
  -o, --output OUTPUT  Output file for aria2 links
```

# Showcase:

## Uploading:

```shell
$ python3 rubikauploader.py *mp3
Files read from disk: 18 
Archive size: 168158521 bytes (161 MiB) 
Everything is Ok 
Uploading: 1770995540434306799.7z.001 
✅ Success & Logged: 1770995540434306799.7z.001 
Uploading: 1770995540434306799.7z.002 
✅ Success & Logged: 1770995540434306799.7z.002 
Uploading: 1770995540434306799.7z.003 
✅ Success & Logged: 1770995540434306799.7z.003 
Uploading: 1770995540434306799.7z.004 
✅ Success & Logged: 1770995540434306799.7z.004 
Uploading: 1770995540434306799.7z.005 
✅ Success & Logged: 1770995540434306799.7z.005 
Uploading: 1770995540434306799.7z.006 
✅ Success & Logged: 1770995540434306799.7z.006 
Uploading: 1770995540434306799.7z.007 
✅ Success & Logged: 1770995540434306799.7z.007 
Uploading: 1770995540434306799.7z.008 
✅ Success & Logged: 1770995540434306799.7z.008 
Uploading: 1770995540434306799.7z.009 
✅ Success & Logged: 1770995540434306799.7z.009 
📜 Uploading manifest...
```

## Downloading:

```shell
$ python3 rubikadownloader.py -i 'manifest_1770995540434306799.txt'
📡 Processing 9 parts from manifest_1770995540434306799.txt...
🔗 Fetching link for: 1770995540434306799.7z.009...
✅ Done! Saved 9 links to captured_link.txt
👉 Run: aria2c -i captured_link.txt -j 5
```
