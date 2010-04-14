import bot, re

# Matches a sed-style regex
regexReplace = re.compile("s/((\\\\\\\\|(\\\\[^\\\\])|[^\\\\/])+)/((\\\\\\\\|(\\\\[^\\\\])|[^\\\\/])*)((/(.*))?)")

requiredBeardBotVersion = 0.1
class BeardBotModule(bot.BeardBotModule):
	messages = []
	def on_channel_message(self, source_name, source_host, message):
		regex = regexReplace.match(message)
		if regex:
			search = regex.groups()[0]
			replace = regex.groups()[3]
			flags = regex.groups()[8]
			if flags == None:
				flags = ""
			
			self.do_substitution(search, replace, flags)
		else:
			self.remember_message(message)
	
	def remember_message(self, message):
		self.messages.append(message)
		self.messages = self.messages[-5:]
	
	def do_substitution(self, search, replace, flags):
		for message in self.messages[::-1]:
			if "g" in flags:
				count = 0
			else:
				count = 1
			
			new = re.sub(search, replace, message, count)
			if new != message:
				self.bot.say(new)
				self.remember_message(new)
				break
