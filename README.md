# big-fiubrother-core

This repository contains many packages used in many applications
in the big-fiubrother system. This includes:
- [big-fiubrother-core-application](modules/application/README.md)
- [big-fiubrother-core-events](modules/application/README.md)
- [big-fiubrother-core-video_storages](modules/application/README.md)

## Build package

### Install

```shell
# Install build
python3 -m pip install --upgrade build

# Install virtual environments
sudo apt install python3.8-venv
```

### Build

```shell
python3 -m build
```

## Upload package

### Install

```shell
# Install twine to upload to PyPi
python3 -m pip install --upgrade twine

# Upgrade requests to avoid problems with twine
pip3 install --upgrade requests
```

### Upload

```shell
python3 -m twine upload dist/*
```