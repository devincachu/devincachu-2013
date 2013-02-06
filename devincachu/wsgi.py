# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devincachu.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
