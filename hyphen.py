import bot, re

hyphenFinder = re.compile("(\w+)-ass (\w+)")

requiredBeardBotVersion = 0.1
class BeardBotModule(bot.BeardBotModule):
	def on_channel_message(self, source_name, source_host, message):
		found = hyphenFinder.search(message)
		if found:
			self.bot.say("(%s ass-%s)"%(found.groups()))
