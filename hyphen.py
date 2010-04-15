from base_module import *
import re

hyphenFinder = re.compile("(\w+)-ass (\w+)")

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	def on_channel_message(self, source_name, source_host, message):
		found = hyphenFinder.search(message)
		if found:
			self.bot.say("(%s ass-%s)"%(found.groups()))
