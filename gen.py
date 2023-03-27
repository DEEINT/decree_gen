import write
import auxil
import consts
import change_case

from numpy.random import choice, randint
import argparse
from os import makedirs, listdir
import re
from time import time
import json

from loguru import logger

def load_samples(samples_dir):

	with open(samples_dir + "/headers.txt") as headerfile:
		header = headerfile.read().split("\n")

	with open(samples_dir + "/names.txt") as namefile:
		name = namefile.read().split("\n")

	with open(samples_dir + "/intros.txt") as introfile:
		intro = introfile.read().split("\n")

	with open(samples_dir + "/instructions.json") as instructionfile:
		instructions = json.load(instructionfile)

	with open(samples_dir + "/execution_control.txt") as execution_controlfile:
		execution_control = execution_controlfile.read().split('\n')

	with open(samples_dir + "/responsible.json") as responsiblefile:
		responsible = json.load(responsiblefile)

	with open(samples_dir + "/creators.txt") as creatorfile:
		creator = creatorfile.read().split('\n')

	logo_list = listdir(samples_dir+"/logo")
	sign_list = listdir(samples_dir+"/signature")
	seal_list = listdir(samples_dir+"/seal")
		
	logger.debug(f"[header] length: {len(header)}")
	logger.debug(f"[name] length: {len(name)}")
	logger.debug(f"[intro] length: {len(intro)}")
	logger.debug(f"[instructions] length: {len(instructions)}")
	logger.debug(f"[execution_control] length: {len(execution_control)}")
	logger.debug(f"[responsible] length: {len(responsible)}")
	logger.debug(f"[creator] length: {len(creator)}")

	return (header, name, intro, instructions, execution_control, responsible,
			creator, logo_list, sign_list, seal_list)

def generate(data, formats, number_of_docs, samples_dir, is_image, out):

	logger.info(f"Using formats: {formats}")

	for idx in range(int(number_of_docs)):
		# название организации в шапке (кто инициатор), data[0][0] - название самого предприятия
		header = data[0][0]
		# тип документа. для хакатона два типа "Приказ по предприятию" (data[1][0]) и "Распоряжение по отделу" (data[1][1])
		name = data[1][0]
		# на будущее - генерировать intro генеративными сетями
		intro = choice(data[2])
		
		# выбор инструкций и исполнителей
		all_instructions = data[3]
		task_responsible_org = choice(data[0][1:6])
		if task_responsible_org == "Департамент разработки":
			task_responsible_org = choice(data[0][7:11])
		if task_responsible_org == "Департамент внедрения и эксплуатации":
			task_responsible_org = choice(data[0][12:])

		actions = []
		for item in all_instructions:
			if item["task_responsible_org"] == task_responsible_org:
				actions = item["task_texts"]
				break

		instructions = choice(actions, size=randint(1,10))

		# выбирается фраза типа "Контроль выполнения возложить на..."
		execution_control = choice(data[4], size=len(instructions))
		# выбор ответственного
		proper_persons = []
		for item in data[5]:
			if item[5] == task_responsible_org:
				proper_persons.append(item)

		responsible_arr = []
		for _ in range(len(instructions)):
			responsible_arr.append(proper_persons[randint(len(proper_persons))])
		responsibles = []
		for i in range(len(responsible_arr)):
			responsibles.append(change_case.create_responsible(execution_control[i], responsible_arr[i][0]))
		
		# создатель документа
		creator = choice(data[6])

		# дата документа
		date = auxil.generate_date(unixtime=True)

		# добавление картинок (логотип, подпись, печать)
		if is_image:
			logo = samples_dir + "logo/" + choice(data[7])
			sign = samples_dir + "signature/" + choice(data[8])
			seal = samples_dir + "seal/" + choice(data[9])
		else:
			logo, sign, seal = None, None, None

		instructions = write.extend_instruction(instructions, responsibles, execution_control, task_responsible_org, samples_dir)
		json_path = write.write_json(instructions, responsibles, date, out, idx)

		if 'd' in formats:
			docx_path = write.write_docx(header, name, intro, instructions, responsibles, creator, date[0], out, idx, logo, sign, seal)

		if 'p' in formats:
			pdf_path = write.write_pdf_linux(docx_path, out, idx)
			generation_data = (header, name, intro, instructions, responsibles, creator, date[0])
			
			if is_image:
				write.write_coords(json_path, pdf_path, header, name, intro, instructions, responsibles, creator, date[0], is_image=True)
			else:
				write.write_coords(json_path, pdf_path, header, name, intro, instructions, responsibles, creator, date[0])

		if 'j' in formats:
			write.write_jpg(out, idx)


def get_args():
	parser = argparse.ArgumentParser(
		description="Decrees generator",
		epilog="Example: python3 gen.py 50MB -f dp -s samples -o decrees -vv")

	parser.add_argument("number_of_docs", help="Number of documents, must be an integer",
						type=auxil.check_size_format)
	parser.add_argument("-i", "--image", help="use images (logo, signature, seal) in decree",
						action="store_true")
	parser.add_argument("-f", "--formats", help="formats to save (docx: d, pdf: p, jpg: j)",
						type=auxil.parse_formats, default="d", metavar="formats")
	parser.add_argument("-s", "--samples", help="path to dir with samples",
						metavar="path", type=str, default="./samples/")
	parser.add_argument("-o", "--out", help="path for output files",
						metavar="path", type=str, default="./decrees")
	parser.add_argument("-v", "--verbose", action="count", default=0,
						help="verbose output")

	return parser.parse_args()

def create_output_dirs(output_dirs_path, formats):
	try:
		makedirs(output_dirs_path + "/json")
		if 'd' in formats:
			makedirs(output_dirs_path + "/docx")
		if 'p' in formats:
			makedirs(output_dirs_path + "/pdf")
		if 'j' in formats:
			makedirs(output_dirs_path + "/jpg")
	except FileExistsError:
		pass


def main():
	global args
	args = get_args()
	auxil.logger_config(args.verbose)

	data = load_samples(args.samples)
	create_output_dirs(args.out, args.formats)

	logger.warning("Generation is started...")
	generate(data, args.formats, args.number_of_docs, args.samples, args.image, args.out)
	logger.warning("Generation is finished!")

if __name__ == '__main__':
	main()
