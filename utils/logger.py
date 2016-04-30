# -*- coding: utf-8 -*-

from .timer import get_date, get_diff

def read_file(filePath):
	with open(filePath, 'rb') as file:
		print(file.read())

def append_content(filePath, content):
	with open(filePath, 'ab') as file:
		file.write(content+'\n')

def write_content(filePath, content):
	with open(filePath, 'wb') as file:
		file.write(content+'\n')

def log_performance(start, end, params, filePath):
	time = get_diff(start, end)
	date = get_date()
	content = date+" - Execution time = "+str(time)+" - "+params
	append_content(filePath, content)
	print(content)
