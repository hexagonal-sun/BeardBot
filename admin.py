import bot

requiredBeardBotVersion = 0.1
class BeardBotModule(bot.BeardBotModule):
	def on_private_message(self, source_name, source_host, message):
		try:
			if self.user_is_admin(source_name):
				if message.startswith("modprobe"):
					self.load_module(source_name, message.split(" ", 1)[1])
				elif message.startswith("rmmod"):
					self.unload_module(source_name, message.split(" ", 1)[1])
		except Exception, e:
			self.bot.pm(source_name, "Eh? What does that mean? Take a look at help.")
			print e
	
	def load_module(self, user, module):
		try:
			self.bot.load_module(module)
			self.bot.pm(user, "Done!")
		except bot.IncompatibleModuleError:
			self.bot.pm(user, "That module is not compatible with me. :(")
		except ImportError:
			self.bot.pm(user, "What are you talking about? That doesn't even exist!")
	
	def unload_module(self, user, module):
		if module == "admin":
				self.bot.pm(user, "I'm afraid I can't let you do that, Dave.")
		else:
			try:
				self.bot.unload_module(module)
				self.bot.pm(user, "That bitch is *DEAD*!")
			except KeyError:
				self.bot.pm(user, "How am I supposed to unload something that isn't loaded?")
	
	def user_is_admin(self, user):
		return True # Todo...
