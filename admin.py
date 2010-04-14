import bot, os

requiredBeardBotVersion = 0.1
class BeardBotModule(bot.BeardBotModule):
	def on_private_message(self, source_name, source_host, message):
		try:
			if self.user_is_admin(source_name):
				if message.startswith("modprobe"):
					self.load_module(source_name, message.split(" ")[1:])
				elif message.startswith("rmmod"):
					self.unload_module(source_name, message.split(" ")[1:])
				elif message == "lsmod":
					self.list_modules(source_name)
		except Exception, e:
			self.bot.pm(source_name, "Eh? What does that mean? Take a look at help.")
			print e
	
	def load_module(self, user, modules):
		for module in modules:
			try:
				self.bot.load_module(module)
				self.bot.pm(user, "I've loaded up %s, if you know what I mean...  ;)"%(module,))
			except bot.IncompatibleModuleError:
				self.bot.pm(user, "%s is not compatible with me. :("%(module,))
			except ImportError:
				self.bot.pm(user, "What are you talking about? That doesn't even exist!")
	
	def unload_module(self, user, modules):
		for module in modules:
			if module == "admin":
					self.bot.pm(user, "I'm afraid I can't let you do that, Dave.")
			else:
				try:
					self.bot.unload_module(module)
					self.bot.pm(user, "%s is *DEAD*!"%(module,))
				except KeyError:
					self.bot.pm(user, "How am I supposed to unload something that isn't loaded?")
	
	def list_modules(self, user):
		self.bot.pm(user, "Available modules:")
		for filename in os.listdir(os.getcwd()):
			if filename.endswith(".py"):
				module_name = filename.partition(".")[0]
				try:
					module = __import__(module_name)
					if module.requiredBeardBotVersion <= bot.__version__:
						postfix = ""
						if module_name in self.bot.modules:
							postfix = " (loaded)"
						self.bot.pm(user, module_name + postfix)
				except AttributeError:
					pass
	
	def user_is_admin(self, user):
		return True # Todo...
