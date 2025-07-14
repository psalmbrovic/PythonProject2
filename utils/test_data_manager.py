import json
import csv
import os
from typing import Dict, List, Any
import openpyxl


class TestDataManager:
	"""Manage test data from various sources"""

	@staticmethod
	def load_json(filepath: str) -> Dict[str, Any]:
		"""Load data from JSON file"""
		with open(filepath, 'r') as file:
			return json.load(file)

	@staticmethod
	def load_csv(filepath: str) -> List[Dict[str, Any]]:
		"""Load data from CSV file"""
		data = []
		with open(filepath, 'r') as file:
			reader = csv.DictReader(file)
			for row in reader:
				data.append(row)
		return data

	@staticmethod
	def load_excel(filepath: str, sheet_name: str = None) -> List[Dict[str, Any]]:
		"""Load data from Excel file"""
		workbook = openpyxl.load_workbook(filepath)
		worksheet = workbook[sheet_name] if sheet_name else workbook.active

		# Get headers
		headers = [cell.value for cell in worksheet[1]]

		# Get data rows
		data = []
		for row in worksheet.iter_rows(min_row=2, values_only=True):
			row_data = dict(zip(headers, row))
			data.append(row_data)

		return data