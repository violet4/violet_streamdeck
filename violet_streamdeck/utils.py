#!/usr/bin/env python3
import os

assets_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')


def get_asset_path(filename:str):
    return os.path.join(assets_folder, filename)
