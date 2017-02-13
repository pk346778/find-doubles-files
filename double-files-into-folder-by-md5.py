import os
import sys
import pprint
import hashlib
from send2trash import send2trash

class FileData:
	def __init__(self, md5_hash, file_path, file_name):
		self.md5_hash = md5_hash
		self.file_path = file_path
		self.file_name = file_name

	def __repr__(self):
		return self.md5_hash + ':' + os.path.join(self.file_path, self.file_name)

	def __cmp__(self, other):
		if __lt__(self, other):
			return -1
		elif __gt__(self, other):
			return 1
		else:
			return 0

	def __gt__(self, other):
		return self.__repr__() > other.__repr__()

	def __lt__(self, other):
		return self.__repr__() < other.__repr__()

	def __ge__(self, other):
		return self.__repr__() >= other.__repr__()

	def __le__(self, other):
		return self.__repr__() <= other.__repr__()


def walk(dir, file_data=[]):
	for name in os.listdir(dir):
		path = os.path.join(dir, name)
		if os.path.isfile(path):
			file_data.append(FileData(get_md5(path), dir, name))
		else:
			walk(path, file_data)

	return file_data

def get_md5(file_path_full):
	with open(file_path_full, 'rb') as f:
		read_data = f.read()
		return hashlib.md5(read_data).hexdigest()

def remove_non_double_into_same_folder(file_data, field_name):
	md5_counter = {}
	for item in file_data:
		item_field_value = item.__dict__[field_name]
		if item_field_value in md5_counter:
			md5_counter[item_field_value] += 1
		else:
			md5_counter[item_field_value] = 1

	return sorted([item for item in file_data if md5_counter[item.__dict__[field_name]] != 1])

def remove_non_double_into_two_folders(base_dir, other_dir, field_name):
	return [item_other for item_other in other_dir if item_other.__dict__[field_name] in set([item_base.__dict__[field_name] for item_base in base_dir])]

def print_result(dir_name, list_to_print, field_name):
	if len(list_to_print) == 0:
		return

	print('Double file in direcotry: ' + dir_name)

	flag = ''
	for i in list_to_print:
		if flag != i.__dict__[field_name]:
			flag = i.__dict__[field_name]
			print('')
		print(i.file_path)


if __name__ == '__main__':

	trash = '/home/qiwi/Downloads/trash'

	type = sys.argv[1]
	field_name = ''

	if type == 'by-md5':
		field_name = 'md5_hash'
	elif type == 'by-file-name':
		field_name = 'file_name'
	elif type == 'sync':
		field_name = '' # fixme
	else:
		raise RuntimeError('Bad compare type!')

	folders = sys.argv[1:]

	if len(folders) == 2:
		file_data = walk(folders[1])
		double_files = remove_non_double_into_same_folder(file_data, field_name)
		print_result(folders[1], double_files, field_name)
	else:
		base_dir = folders[1]
		# other_dirs = folders[1:]
		base_dir_links = walk(base_dir)
		print('Base direcotry: ' + base_dir + '\n')

		for other_dir in folders[2:]:
			other_dir_link = walk(other_dir, [])
			double_files = remove_non_double_into_two_folders(base_dir_links, other_dir_link, field_name)
			print_result(other_dir, double_files, field_name)

			for i in double_files:
				# os.rename(os.path.join(i.file_path, i.file_name), os.path.join(trash, i.file_name))
				send2trash(os.path.join(i.file_path, i.file_name))
