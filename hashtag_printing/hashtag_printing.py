#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial, textwrap, os
import twitter
from datetime import datetime
from time import strftime, mktime, strptime, sleep

class Printer(object):

	def __init__(self, serialPrinter, searchterm, allowReplies=False):
		self.printer = serialPrinter
		self.searchterm = searchterm
		self.allowReplies = allowReplies

		# some fancy metadata stuff
		self.printHeadline(self.searchterm)

		last_id_filename = "last_id_searchterm_%s" % self.searchterm.replace("#", "")
		microprint_path = os.path.dirname(os.path.abspath(__file__))
		self.savepoint_file = os.path.join(microprint_path, last_id_filename)

	def printHeadline(self, text, metadata=None):
		# Bigger font
		self.printer.write("\x1b\x21\x20%s\n\x1b\x21\0" % textwrap.fill(text,24))
		self.printer.write("------------------------------------------------\n")
		self.printer.write("%s\n" % strftime("%d.%m.%Y %H:%M"))

		if metadata != None:
			for i in range(0,len(metadata)):
				self.printer.write("%s\n" % metadata[i])

		self.printer.write("------------------------------------------------\n\n")


	def cut(self, partial=False):
		# feed paper
		self.printer.write("\n\n\n\n\n")

		if partial:
			self.printer.write("\x1b\x6D")
		else:
			self.printer.write("\x1b\x69")

	def getSavepoint(self):
		try:
			with open(self.savepoint_file, "r") as file:
				return file.read()
		except IOError:
			return ""

	def writeSavepoint(self, lastId):
		# write last printed tweet id to file
		with open(self.savepoint_file, "w") as file:
			file.write(str(lastId))


	def printRetweets(self):
		# search query
		twit = twitter.Twitter()
		timeline = twit.search(self.searchterm, since_id=self.getSavepoint(), max_results=999)

		print "%d items found." % len(timeline)

		if not self.allowReplies:
			# filter @replies out and reverse timeline
			timeline = filter(lambda status: status["text"][0] != "@", timeline)
			timeline.reverse()

		for status in timeline:
			# Generates messages
			timestamp = datetime.fromtimestamp(mktime(strptime(status["created_at"], 
				"%a, %d %b %Y %H:%M:%S +0000")))

			message = "(%(created)s) %(screenname)s: %(statusmessage)s\n\n" \
				% {"created" : timestamp, "screenname" : status["from_user"], 
				"statusmessage" : status["text"]}

			# Wraps the text in order to avoid cut text
			message = textwrap.fill(text=message, width=48)
			message = message + "\n\n"
			self.printer.write(message.encode("cp437", "replace"))
			print message

		if len(timeline) != 0:
			self.writeSavepoint(timeline[-1]["id"])


# print to stdout instead of printer
class DryPrinter(object):
	def write(self, text):
		for line in text.split("\n"):
			print "[Printer] %s" % line


if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(
		description="Prints tweets containing given search term on serial receipt printer.")
	parser.add_argument("searchterm", type=str, help="term to search for (e.g. #yourHashtag)")
	parser.add_argument("-d", "--device", type=str, default="/dev/ttyUSB0", 
		help="device name or port number (default: /dev/ttyUSB0)")
	parser.add_argument("-b", "--baudrate", type=int, default=19200, 
		help="baud rate (default: 19200)")
	parser.add_argument("-t", "--dry", action="store_true", 
		help="dry run (printing to stdout instead of serial receipt printer) (default: off)")
	parser.add_argument("-r", "--replies", action="store_true", 
		help="do not filter @replies out (default: off)")
	parser.add_argument("-s", "--sleep", type=int, default=60, 
		help="sleep between searches (in seconds) (default: 60)")

	args = parser.parse_args()

	serialPrinter = DryPrinter() if args.dry else serial.Serial(args.device, args.baudrate)
	printer = Printer(serialPrinter, args.searchterm, args.replies)

	try:
		while True:
			printer.printRetweets()
			sleep(args.sleep)
	except KeyboardInterrupt:
		printer.cut()
