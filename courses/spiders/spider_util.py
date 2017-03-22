# Author: Noel Buruca - University of Maryland, College Park
# This file contains common utility functions

### Imports ####
import time
import datetime
import sys

# Gets the current time in the format yyyy-mm-dd hh:mm:ss
def get_time_string():
	ime_stamp = time.time()
	date_time = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
	return date_time

# Opens a logfile and returns the file descriptor
def open_file(file_name, option):
	file_handler = open(file_name, option)
	return file_handler

# Prints debug statement
def print_and_debug(file_handler, str):
	file_handler.write(get_time_string() + ", DEBUG: " + str)

# Prints failure message and terminates the program
def fail_and_die(file_handler, str):
	file_handler.write(get_time_string() + ", FAIL: " + str)
	print "Terminating due to critical error. Please see " + file_handler.name() + " for more info."
	sys.exit()