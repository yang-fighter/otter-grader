############################################
##### Metadata Parser for Local Grader #####
############################################

import yaml
import json
import glob
import os
import re

from utils import *

class GradescopeParser:
	"""Metadata parser for Gradescope exports"""

	def __init__(self, submissions_dir):
		# open metadata file and load into Python object
		with open(os.path.join(submissions_dir, "submission_metadata.yml")) as f:
			metadata = yaml.safe_load(f)

		# initialize metadata list
		self._metadata = []
		for file in metadata:
			self._metadata += [{

				# metadata is separated by filename into a list of submitters
				# and we use the SID as the identifier
				"identifier": metadata[file][":submitters"][0][":sid"],
				"filename": file
			}]

	def get_metadata(self):
		"""Returns mapping of identifiers to files"""
		return self._metadata

	def get_identifiers(self):
		"""Returns list of submission identifiers"""
		return [file["identifier"] for file in self._metadata]

	def get_filenames(self):
		"""Returns list of filenames in the submission directory"""
		return [file["filename"] for file in self._metadata]

class CanvasParser:
	"""Metadata parser for Canvas exports"""
	def __init__(self, submissions_dir):
		# list all files in the submissions directory since Canvas
		# doesn't output a metadata file
		submissions = list_files(submissions_dir)

		# intialize metadata list and iterate through the files
		self._metadata = []
		for file in submissions:
			# extract the identifier from the filename, which is everything
			# before the first underscore, meaning
			# somestudent_12345_67890_SomeStudent.ipynb -> somestudent
			identifier = re.match(r"(\w+?)\_", file)[1]

			# add the identifier and filename to the metadata list
			self._metadata += [{
				"identifier": identifier,
				"filename": file
			}]

	def get_metadata(self):
		"""Returns mapping of identifiers to files"""
		return self._metadata

	def get_identifiers(self):
		"""Returns list of submission identifiers"""
		return [file["identifier"] for file in self._metadata]

	def get_filenames(self):
		"""Returns list of filenames in the submission directory"""
		return [file["filename"] for file in self._metadata]


class JSONParser:
	"""Metadata parser for JSON format"""
	def __init__(self, file_path):
		# open JSON file and load contents into a string
		with open(file_path) as f:
			metdata = f.read()

		# parse string with json library
		self._metadata = json.loads(metdata)

		# check that the JSON file has the correct structure
		assert type(self._metadata) == list, "JSON metadata is not a list"
		
		# check that each item in the JSON file is of correct type
		# and as "identifier" and "filename" keys
		for file in self._metadata:
			assert type(file) == dict, "JSON metadata does not have dictionaries"
			assert "identifier" in file.keys(), "JSON metadata does not contain \"identifier\" key"
			assert "filename" in file.keys(), "JSON metadata does not contain \"filename\" key"

	def get_metadata(self):
		"""Returns mapping of identifiers to files"""
		return self._metadata

	def get_identifiers(self):
		"""Returns list of submission identifiers"""
		return [file["identifier"] for file in self._metadata]

	def get_filenames(self):
		"""Returns list of filenames in the submission directory"""
		return [file["filename"] for file in self._metadata]

class YAMLParser:
	"""Metadata parser for YAML format"""
	def __init__(self, file_path):
		# open the YAML file and parse with yaml library
		with open(file_path) as f:
			self._metadata = yaml.safe_load(f)

		# check that the YAML file has the correct structure
		assert type(self._metadata) == list, "YAML metadata is not a list"
		
		# check that each item in the YAML file is of correct type
		# and as "identifier" and "filename" keys
		for file in self._metadata:
			assert type(file) == dict, "YAML metadata does not have dictionaries"
			assert "identifier" in file.keys(), "YAML metadata does not contain \"identifier\" key"
			assert "filename" in file.keys(), "YAML metadata does not contain \"filename\" key"

	def get_metadata(self):
		"""Returns mapping of identifiers to files"""
		return self._metadata

	def get_identifiers(self):
		"""Returns list of submission identifiers"""
		return [file["identifier"] for file in self._metadata]

	def get_filenames(self):
		"""Returns list of filenames in the submission directory"""
		return [file["filename"] for file in self._metadata]