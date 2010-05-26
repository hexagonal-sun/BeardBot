#!/usr/bin/env python
__version__ = 0.1
__author__ = "Jonathan Heathcote"

import sys
import traceback
import pickle
from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower
from optparse import OptionParser

class IncompatibleModuleError(Exception):
	"""
	For raising when a module too new for this server is loaded
	"""
	pass

class BeardBot(SingleServerIRCBot):
		def __init__(self, channel, server, port=6667, name="beardbot"):
			SingleServerIRCBot.__init__(self, [(server, port)],
			                            name,
			                            "The Beardy-Based Botulator")
			# The channel the bot is a member of
			self.channel = channel
			
			# The last place a message was recieved from (used by "reply")
			self.last_message_sender = self.channel
			
			# The loaded modules
			self.modules = {}
			
			# Try to load previously loaded modules
			try:
				old_modules = pickle.load(open(self.channel + "_modules.db", "r"))
				for module in old_modules:
					try:
						self.load_module(module)
					except Exception, e:
						traceback.print_exc(file=sys.stdout)
			except:
				# Otherwise just start the admin
				try:
					self.load_module("admin")
				except Exception, e:
					print e
		
		def get_nick(self):
			"""Get the bot's nickname"""
			return self.connection.get_nickname()
		def set_nick(self, nick):
			"""Set the bot's nickname"""
			self.connection.nick(nick)
		nick = property(fget=get_nick, fset=set_nick)
		
		def say(self, message):
			"""Send a message to the channel"""
			self.pm(self.channel, message)
		
		def reply(self, message):
			"""Send a message to the last person to speak"""
			self.pm(self.last_message_sender, message)
		
		def pm(self, user, message):
			"""Send a message to a user"""
			message = message.replace("\r","\n")
			for part in message.split("\n"):
				self.connection.privmsg(user, part.encode("UTF8"))
		
		def on_nicknameinuse(self, c, e):
			c.nick(c.get_nickname() + "_")
		
		def on_welcome(self, c, e):
			c.join(self.channel)
			#c.privmsg(self.channel, "Hi there, I'm beardy. If I'm annoying, tell me to die.")
		
		def on_privmsg(self, c, e):
			# Handle a message recieved from the channel
			source_name = nm_to_n(e.source()).lower()
			source_host = nm_to_h(e.source())
			message = e.arguments()[0].decode("UTF8")
			self.last_message_sender = source_name
			
			for module in self.modules.values():
				try:
					module.handle_private_message(source_name, source_host, message)
				except Exception, e:
					traceback.print_exc(file=sys.stdout)
			
			if message == "die":
				# Force the bot to die
				self.die("Someone killed me... It was you, " + nm_to_n(e.source()))
			elif message == "panic:reloadadmin":
				# Restart the admin module if something is going wrong
				try:
					self.load_module("admin")
				except Exception, e:
					print e
		
		def on_pubmsg(self, c, e):
			# Handle a message recieved from the channel
			source_name = nm_to_n(e.source()).lower()
			source_host = nm_to_h(e.source())
			message = e.arguments()[0]
			self.last_message_sender = self.channel
			
			# If a message was addressed specifically to the bot, note this and strip
			# this from the message
			addressed_to_BeardBot = irc_lower(message).startswith("%s: " % self.nick.lower())
			if addressed_to_BeardBot:
				message = message.split(": ", 1)[-1]
			
			# Alert each module that a message has arrived
			for module in self.modules.values():
				try:
					if addressed_to_BeardBot:
						module.handle_addressed_message(source_name, source_host, message.decode("UTF8"))
					else:
						module.handle_channel_message(source_name, source_host, message.decode("UTF8"))
				except Exception, e:
					traceback.print_exc(file=sys.stdout)
		
		def load_module(self, module_name):
			"""
			Try to (re)load the named module.
			"""
			module = __import__(module_name)
			reload(module)
			if module_name in self.modules:
				self.unload_module(module_name)
			
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
			# Store a list of loaded modules before going down
			pickle.dump(self.modules.keys(), open(self.channel + "_modules.db", "w"))
			
			# Kill all the modules
			for module in self.modules.values():
				module.die()
			
			# Disconnect and quit
			SingleServerIRCBot.die(self, *args, **kwargs)

def main():
	# Parse command line arguments.
	parser = OptionParser()

	parser.add_option("-r", "--room",   dest="room",   default="#uhc")
	parser.add_option("-s", "--server", dest="server", default="irc.quakenet.org")
	parser.add_option("-n", "--name",   dest="name",   default="beardbot")

	(options, args) = parser.parse_args()

	#prepend a '#' to the room if there isn't one.
	room = options.room if options.room.startswith('#') else ("#" + options.room)
	server = options.server
	name = options.name

	print "Starting '%s' in room '%s' on '%s'..." % (name, room, server)
	
	# Run the bot.
	bot = BeardBot(room, server, name=name)
	
	try:
		bot.start()
	except KeyboardInterrupt:
		bot.die()

if __name__ == "__main__":
	main()
