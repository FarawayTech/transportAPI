#!/usr/bin/env python
import logging
from . import line_colors, sms_tickets, stations


logging.info("Importing stations")
stations.main_import()
logging.info("Done.\n")

logging.info("Importing line color codes")
line_colors.main_import()
logging.info("Done.\n")

logging.info("Importing SMS ticket codes")
sms_tickets.main_import()
logging.info("Done.")
