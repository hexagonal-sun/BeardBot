from base_module import *
import difflib, shelve

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	def __init__(self, *args, **kwargs):
		ModuleBase.__init__(self, *args, **kwargs)
		self.messages = shelve.open(self.bot.channel + "_astersed.db")
	
	def on_channel_message(self, source_name, source_host, message):
		self.messages[source_name] = message
	
	@on_channel_match("^\*([^\s*]+)$")
	def on_aster_change(self, source_name, source_host, message, change):
		last_message = self.messages[source_name].split(' ')
		likely_changes = difflib.get_close_matches(change, last_message, 5, 0.5)
		
		# Don't match an exact version of the word
		likely_changes = filter((lambda x: x != change), likely_changes)
		
		if len(likely_changes) != 0:
			target = likely_changes[0]
			
			# Dirty hack -- please sanitise
			self.bot.say(" ".join([change if x == target else x for x in last_message]))
	
	def die(self):
		self.messages.close()
		ModuleBase.die(self)
