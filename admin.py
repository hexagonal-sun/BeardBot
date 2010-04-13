import bot

requiredBeardBotVersion = 0.1
class BeardBotModule(bot.BeardBotModule):
	def on_private_message(self, source_name, source_host, message):
		try:
			if self.user_is_admin(source_name):
				if message.startswith("modprobe"):
					module = message.split(" ", 1)[1]
					try:
						self.bot.load_module(module)
						self.bot.pm(source_name, "Done!")
					except bot.IncompatibleModuleError:
						self.bot.pm(source_name, "That module is not compatible with me. :(")
					except ImportError:
						self.bot.pm(source_name, "What are you talking about? That doesn't even exist!")
				elif message.startswith("rmmod"):
					module = message.split(" ", 1)[1]
					try:
						self.bot.unload_module(module)
						self.bot.pm(source_name, "That bitch is *DEAD*!")
					except KeyError:
						self.bot.pm(source_name, "How am I supposed to unload something that isn't loaded?")
		except Exception, e:
			self.bot.pm(source_name, "Eh? What does that mean? Take a look at help.")
			print e
	
	def user_is_admin(self, user):
		return True # Todo...
