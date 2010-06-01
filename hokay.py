from base_module import *
import shelve, datetime

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	def __init__(self, newBot):
		ModuleBase.__init__(self, newBot)
	
	@on_channel_match("^hokay$", re.I)
	def on_hokay(self, source_name, source_host, message):
		self.bot.say("So here's the earth")
	
	@on_channel_match("^(?:hokay )?So here'?s the earth$", re.I)
	def on_heres_the_earth(self, source_name, source_host, message):
		self.bot.say("just chillin'")
	
	@on_channel_match("^just chillin'?$", re.I)
	def on_chillin(self, source_name, source_host, message):
		self.bot.say("\"Damn, that is a sweet earth\", you might say.")
	
	@on_channel_match("^[\"']?(?:Damn,? )?that(?: is|s) a sweet earth[\"']?,?(?: you might say)?$", re.I)
	def on_sweet_earth(self, source_name, source_host, message):
		self.bot.say("WRONG!")
	
	@on_channel_match("But I am le tired!?", re.I)
	def on_le_tired(self, source_name, source_host, message):
		self.bot.say("OK, then have a nap, ZEN FIRE ZE MISSILES!")
	
	@on_channel_match("[a']?bout that time,? eh,? chaps[?]?", re.I)
	def on_right_o(self, source_name, source_host, message):
		self.bot.say("*putt* Right-o")
