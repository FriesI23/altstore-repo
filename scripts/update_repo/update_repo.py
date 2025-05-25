#!/bin/bash
# encoding: utf-8
from typing import Iterable
from argparse import ArgumentParser

import logging
from altparse import AltSourceManager, Parser, altsource_from_file

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


source_data = [
    {
        "parser": Parser.GITHUB,
        "kwargs": {
            "repo_author": "FriesI23",
            "repo_name": "mhabit",
            "asset_regex": "mhabit-unsigned.ipa",
        },
        "ids": ["io.github.friesi23.mhabit"],
    }
]

alternate_data = {
    "io.github.friesi23.mhabit": {
        "beta": False,
    },
}


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-s", "--source-path", default="source.json")
    return parser.parse_args()


def update_altsource(source_path: str):
    src = altsource_from_file(source_path)
    mgr = AltSourceManager(src, source_data)
    try:
        mgr.update()
        mgr.update_hashes()
        mgr.alter_app_info(alternate_data)
        mgr.save(prettify=True, only_standard_props=False)
    except Exception as err:
        logging.error(f"Unable to update {mgr.src.name}.")
        logging.error(f"{type(err).__name__}: {str(err)}")


def main():
    args = parse_args()
    source_path = args.source_path
    logging.info(f"Source Path: {source_path}")
    update_altsource(source_path)


if __name__ == "__main__":
    main()
