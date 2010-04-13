__version__ = 0.1
__author__ = "Jonathan Heathcote"

from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower

class BeardBotModule(object):
	def __init__(self, bot):
		self.bot = bot
	def on_channel_message(self, source_name, source_host, message):
		pass
	def on_addressed_message(self, source_name, source_host, message):
		pass
	def die(self):
		pass

class IncompatibleModuleError(Exception):
	"""
	For raising when a module too new for this server is loaded
	"""
	pass

class BeardBot(SingleServerIRCBot):
		def __init__(self, channel, server, port=6667):
			SingleServerIRCBot.__init__(self, [(server, port)],
			                            "beardbot",
			                            "The Beardy-Based Botulator")
			# The channel the bot is a member of
			self.channel = channel
			
			# The loaded modules
			self.modules = {}
		
		def get_nick(self):
			"""Get the bot's nickname"""
			return self.connection.get_nickname()
		def set_nick(self, nick):
			"""Set the bot's nickname"""
			self.connection.nick(nick)
		nick = property(fget=get_nick, fset=set_nick)
		
		def say(self, message):
			"""Send a message to the channel"""
			self.connection.privmsg(self.channel, message)
		
		def on_nicknameinuse(self, c, e):
			c.nick(c.get_nickname() + "_")
		
		def on_welcome(self, c, e):
			c.join(self.channel)
			#c.privmsg(self.channel, "Hi there, I'm beardy. If I'm annoying, tell me to die.")
		def on_privmsg(self, c, e):
			print "---"
			print e.eventtype()
			print e.source()
			print e.target()
			print e.arguments()
			if e.arguments()[0] == "die":
				self.die("Someone killed me... It was you, " + nm_to_n(e.source()))
		
		def on_pubmsg(self, c, e):
			# Handle a message recieved from the channel
			source_name = nm_to_n(e.source()).lower()
			source_host = nm_to_h(e.source())
			message = e.arguments()[0]
			
			# If a message was addressed specifically to the bot, note this and strip
			# this from the message
			addressed_to_BeardBot = irc_lower(message).startswith("%s: "%(self.nick,))
			if addressed_to_BeardBot:
				message = message.split(": ", 1)[-1]
			
			# Alert each module that a message has arrived
			for module in self.modules.itervalues():
				if addressed_to_BeardBot:
					module.on_addressed_message(source_name, source_host, message)
				else:
					module.on_channel_message(source_name, source_host, message)
		
		def load_module(self, module_name):
			module = __import__(module_name)
			if module_name in self.modules:
				unload_module(module_name)
			
			if module.requiredBeardBotVersion > __version__:
				raise IncompatibleModuleError("%s requires BeardBot version %s"%(
				                              module_name,
				                              module.requiredBeardBotVersion))
			
			# Try to load the module with a refrence to this bot
			self.modules[module_name] = module.BeardBotModule(self)
		
		def unload_module(self, module_name):
			self.modules[module_name].die()
			del self.modules[module_name]
		
		def die(self, *args, **kwargs):
			SingleServerIRCBot.die(self, *args, **kwargs)
			for module in self.modules.itervalues():
				module.die()

def main():
	bot = BeardBot("#uhc", "irc.quakenet.org")
	bot.load_module("log")
	bot.load_module("beardy")
	bot.start()

if __name__ == "__main__":
	main()
