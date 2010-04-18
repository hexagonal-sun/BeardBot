from base_module import *
import re
import string

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	"""help [module_name]
	"""
	@on_addressed_match("help (?:me )?(?:on |with )?(\S+)", re.I)
	def help(self, source_name, source_host, message, module_name):
		if module_name in self.bot.modules:
			module = self.bot.modules[module_name].__class__
			if hasattr(module, "__doc__") and module.__doc__:
				doc = module.__doc__
				for line in filter(len, map(string.rstrip, doc.split("\n"))):
					self.bot.reply(line)
			else:
				self.bot.reply("An undocumented module? Your guess is as good as mine!")
		else:
			self.bot.reply("That's not a module! You need to see a psychiatrist, not an irc bot.")
	
	@on_private_match("help (?:me )?(?:on |with )?(\S+)", re.I)
	def _help(self, *args, **kwargs):
		self.help(self, *args, **kwargs)
