#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial, textwrap, os, tweepy
from datetime import datetime
from time import strftime, mktime, strptime, sleep

# provide your credentials
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

class Printer(object):

	def __init__(self, serialPrinter, searchterm, allowReplies=False, allowRetweets=True):
		self.printer = serialPrinter
		self.searchterm = searchterm
		self.allowReplies = allowReplies
		self.allowRetweets = allowRetweets

		# some fancy metadata stuff
		self.printHeadline(self.searchterm)

		lastIdFilename = "last_id_searchterm_%s" % self.searchterm.replace("#", "").split(" ")[0]
		microprintPath = os.path.dirname(os.path.abspath(__file__))
		self.savepointFile = os.path.join(microprintPath, lastIdFilename)

		# connect with Twitter
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		self.twitter = tweepy.API(auth)
		try:
			self.twitter.verify_credentials()
		except tweepy.error.TweepError, e:
			print "Twitter API error: %s" % e.message[0]["message"]
			quit()

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
			with open(self.savepointFile, "r") as file:
				return file.read()
		except IOError:
			return ""

	def writeSavepoint(self, lastId):
		# write last printed tweet id to file
		with open(self.savepointFile, "w") as file:
			file.write(str(lastId))


	def printRetweets(self):
		# search query
		timelineIterator = tweepy.Cursor(self.twitter.search, q=self.searchterm, since_id=self.getSavepoint()).items()

		# put everything into a list to be able to sort/filter
		timeline = []
		for status in timelineIterator:
			timeline.append(status)

		if len(timeline) == 0:
			print "No new Tweets at the moment."
			return

		lastTweetId = timeline[0].id

		if not self.allowReplies:
			# filter @replies out
			timeline = filter(lambda status: status.text[0] != "@", timeline)

		if not self.allowRetweets:
			# filter retweets out
			timeline = filter(lambda status: status.text[:3] != "RT ", timeline)

		timeline.reverse()
		print "%d items found." % len(timeline)

		for status in timeline:
			# Generates messages
			message = "(%(created)s) %(screenname)s: %(statusmessage)s\n\n" \
				% {"created" : status.created_at, "screenname" : status.from_user,
				"statusmessage" : status.text}

			# Wraps the text in order to avoid cut text
			message = textwrap.fill(text=message, width=48)
			message = message + "\n\n"
			self.printer.write(message.encode("cp437", "replace"))
			print message.encode("utf-8")

		self.writeSavepoint(lastTweetId)


# print to stdout instead of printer
class DryPrinter(object):
	def write(self, text):
		for line in text.split("\n"):
			print "[Printer] %s" % line


if __name__ == "__main__":
	import argparse

	# credentials empty?
	if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
		print "Please provide Twitter API credentials in '%s'." % os.path.abspath(__file__)
		quit()

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
		help="do not filter @replies out")
	parser.add_argument("-e", "--retweets", action="store_true",
		help="do not filter Retweets out")
	parser.add_argument("-s", "--sleep", type=int, default=60,
		help="sleep between searches (in seconds) (default: 60)")

	args = parser.parse_args()

	serialPrinter = DryPrinter() if args.dry else serial.Serial(args.device, args.baudrate)
	printer = Printer(serialPrinter, args.searchterm, args.replies, args.retweets)

	try:
		while True:
			printer.printRetweets()
			sleep(args.sleep)
	except KeyboardInterrupt:
		printer.cut()
