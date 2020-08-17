# dlc2json: DLC Results Converter to JSON

## Requirements

The requirements are specified in the `requirements.txt`, to install them:
```sh
$ sudo pip3 install -r requirements.txt
```

## Usage

```sh
$ ./dlcPickleToJson.py -h
usage: dlcPickleToJson.py [-h] [-d OUTP_DIR] INPUT [INPUT ...]

DLC results converter from pickle to JSON.

positional arguments:
  INPUT                 Wildcards of input files in the Python Pickle format
                        to be converted

optional arguments:
  -h, --help            show this help message and exit
  -d OUTP_DIR, --outp-dir OUTP_DIR
                        Output directory for the converted files. The input
                        directory is used by default. (default: None)
```

For example:
```sh
$ ./dlcPickleToJson.py -d . ../LarvaDeT/data/for_artem_larvae_for_training/vid*.pickle
onverting ../LarvaDeT/data/for_artem_larvae_for_training/vid3DLC_resnet50_B7_v44_v45Aug5shuffle1_200000_full.pickle ...
  converted to:./vid3DLC_resnet50_B7_v44_v45Aug5shuffle1_200000_full.json
Converting ../LarvaDeT/data/for_artem_larvae_for_training/vid3DLC_resnet50_B7_v44_v45Aug5shuffle1_200000_meta.pickle ...
  converted to:./vid3DLC_resnet50_B7_v44_v45Aug5shuffle1_200000_meta.json
```
