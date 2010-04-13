import beardy
from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower

class BeardBot(SingleServerIRCBot):
		def __init__(self, channel, server, port=6667):
			SingleServerIRCBot.__init__(self, [(server, port)],
			                            "beardbot",
			                            "The Beardy-Based Botulator")
			# The channel the bot is a member of
			self.channel = channel
			
			# The loaded modules
			self.modules = {}
		
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
			print "---"
			print e.eventtype()
			print e.source()
			print e.target()
			print e.arguments()
			person = nm_to_n(e.source())
			message = e.arguments()[0]
		
		def load_module(self, module_name):
			module = __import__(module_name)
			if module_name in self.modules:
				unload_module(module_name)
			
			# Try to load the module with a refrence to this bot
			self.modules[module_name](module.BeardBotPlugin(self))
		
		def unload_module(self, module_name):
			self.modules[module_name].die()
			del self.modules[module_name]

def main():
	bot = BeardBot("#uhc", "irc.quakenet.org")
	bot.load_module("log")
	#bot.start()
	bot.die()

if __name__ == "__main__":
	main()
