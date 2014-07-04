#!/usr/bin/env python
# encoding=UTF-8

import tornadoredis


CONNECTION_POOL = tornadoredis.ConnectionPool(max_connections=64,
                                              wait_for_available=True)

