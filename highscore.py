from base_module import *
import shelve, datetime

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	def __init__(self, newBot):
		ModuleBase.__init__(self, newBot)
		self.last_highscore = datetime.date.today()
		self.scores = shelve.open(self.bot.channel + "_highscore.db")
	
	def on_channel_message(self, source_name, source_host, message):
		# Expire old scores/reset on "we are all sad"
		if self.last_highscore != datetime.date.today() or message == "we are all sad":
			for person in self.scores.keys():
				del self.scores[person]
		
		if message.count(":D") > 2:
			if source_name not in self.scores:
				self.scores[source_name] = 2
			if message.count(":D") > self.scores[source_name]:
				self.scores[source_name] = message.count(":D")
				if message.count(":D") > 20:
					self.bot.say("Now you're just pissing me off: %i :Ds"%(message.count(":D"), ))
				else:
					self.bot.say("High score! %i :Ds"%(message.count(":D"), ))
				
				best = True
				for person in self.scores:
					if person != source_name and self.scores[person] > self.scores[source_name]:
						best = False
						break
				if best:
					self.bot.say("%s is the channel leader!"%(source_name, ))
			score = self.scores[source_name]
			
	def on_addressed_message(self, source_name, source_host, message):
		if message == "who is happiest of them all?":
			for person in self.scores:
				self.bot.say("%s: %s"%(person, ":D"*(self.scores[person])))
	
	def die(self):
		self.scores.close()
