#!/usr/bin/env python

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devincachu.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
