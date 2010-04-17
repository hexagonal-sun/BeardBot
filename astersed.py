from base_module import *
import re, difflib

# Matches a sed-style regex
regexAster = re.compile("\*([^\s]+)")

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	messages = {}
	def on_channel_message(self, source_name, source_host, message):
		regex = regexAster.match(message)
		if regex:
			change = regex.groups()[0]
			self.do_substitution(change, source_name)
		else:
			self.messages[source_name] = message
	
	def do_substitution(self, change, user):
		if user in self.messages:
			last_message = self.messages[user].split()
			likely_changes = difflib.get_close_matches(change, last_message)
			
			# Don't match an exact version of the word
			likely_changes = filter((lambda x: x != change), likely_changes)
			
			if len(likely_changes) != 0:
				target = likely_changes[0]
				
				# Dirty hack -- please sanitise
				def rep(x):
					if x == target: return change
					else: return x
				self.bot.say(" ".join(map(rep, last_message)))
