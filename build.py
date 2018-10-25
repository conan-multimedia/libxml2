#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import platform
import os

from bincrafters import build_template_default

os.environ['CONAN_USERNAME'] = os.environ.get('CONAN_USERNAME','conanos')

if __name__ == "__main__":

    builder = build_template_default.get_builder(pure_c=True)

    items = []
    for item in builder.items:
        # add msys2 and mingw as a build requirement for mingw builds
        if platform.system() == "Windows" and item.settings["compiler"] == "gcc" and \
                not item.options.get("libxml2:shared", False):
            new_build_requires = copy.copy(item.build_requires)
            new_build_requires["*"] = new_build_requires.get("*", []) + \
                ["mingw_installer/1.0@conan/stable",
                 "msys2_installer/latest@bincrafters/stable"]
            items.append([item.settings, item.options, item.env_vars,
                          new_build_requires, item.reference])
        else:
            items.append(item)
    builder.items = items

    builder.run()
