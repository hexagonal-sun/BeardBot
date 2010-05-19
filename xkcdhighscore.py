from base_module import *
import shelve, datetime

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	def __init__(self, newBot):
		ModuleBase.__init__(self, newBot)
		self.scores = shelve.open(self.bot.channel + "_xkcdhighscore.db")
	
	@on_channel_match(".*(?:http://)?(?:www\.)?xkcd\.com/[0-9]+.*", re.I)
	def on_xkcd_refrence(self, source_name, source_host, message):
		if source_name not in self.scores:
			self.scores[source_name] = 1
		else:
			self.scores[source_name] += 1
		
	@on_addressed_match("xkcd(?: highscore)? (?:refrence|leaderboard).*", re.I)
	def on_highscore_request(self, source_name, source_host, message):
		for person in self.scores:
			self.bot.say("%s: %d"%(person, self.scores[person]))
	
	def die(self):
		self.scores.close()
