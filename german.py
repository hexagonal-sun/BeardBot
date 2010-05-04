from base_module import *
import re
import string

swaps = {
	"s":"z",
	"th":"z",
	"w":"V",
	"v":"W",
	"V":"v",
	"W":"w",
	"I":"ich",
}

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	@on_addressed_match("(?:in )german:?\s+(.*)", re.I)
	def german(self, source_name, source_host, message, translate):
		for find, replace in swaps.iteritems():
			translate = translate.replace(find, replace)
		self.bot.reply(translate)
