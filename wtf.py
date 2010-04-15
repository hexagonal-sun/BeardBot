import bot, re, string

ask_re = re.compile("wtf is (\S*[^\?])\??")


word_lists = ["/usr/share/misc/acronyms", "/usr/share/misc/acronyms.comp"]


requiredBeardBotVersion = 0.1
class BeardBotModule(bot.BeardBotModule):
	def on_channel_message(self, source_name, source_host, message):
		found = ask_re.search(message)
		if found:
			word = found.group(1)
			description = self.translate(word)
			if description:
				self.bot.say(description)
			else:
				self.bot.say("Fuck knows!?")


	def translate(self, word_to_find):
		for file_name in word_lists:
			for line in filter(lambda l: len(l) and l[0] != '$',
					   map(string.strip,
					       open(file_name).xreadlines())):
				word, desc = map(string.strip, line.replace('\t', ' ').split(' ', 1))
				if word_to_find.upper() == word:
					return desc
		
