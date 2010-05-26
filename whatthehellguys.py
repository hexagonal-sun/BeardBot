################################################################################
# WARNING: This file has regexes which may be NSFW!                            #
#          Scroll down at your own risk/perversion                             #
################################################################################
















































































from base_module import *
import shelve, time, re
import threading
import urllib2

RECOVERY_RATE_PER_SECOND = 0.05 / 60
RECOVERY_RATE_PER_MESSAGE = 1 / 30

# Immature and disturbing list
rules = {
	".*rape.*" : 0.7,
	".*(?:pr[0o]n|p[o0]rn).*" : 0.8,
	".*(?:fap|jizz|shag|dogging|masturbate|anal|oral|bdsm|fisting).*" : 0.7,
	".*(?:fuck|cunt).*" : 0.8,
	".*(?:shit|wanker|dick|penis|cock|tits|fun bags).*" : 0.9,
	".*condom.*" : 0.9,
	".*tentacle porn.*" : 0.3,
	".*pi[cx]s ?pls.*" : 0.5,
	".*(?:goatse|tub girl|2g1c|two girls one cup|loli|yaoi|yuri).*" : 0.5,
	".*4chan.*" : 0.3,
	".*(?:racism|racist).*" : 0.9,
	".*rule ?34.*" : 0.3,
	".*/b/.*" : 0.2,
	".*disectchan.*" : 0.1,
	".*James Sandford.*" : 0.1,
	".*(?:necrophilia|bestiality).*" : 0.5,
	".*lol.*" : 0.95,
	".*!!!+.*" : 0.95,
	".*nigger.*" : 0.5,
	".*insert (?:disturbing|worrying|illigal) sexual act here.*" : 0.2,
}

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	def __init__(self, newBot):
		ModuleBase.__init__(self, newBot)
		self.shelf = shelve.open(self.bot.channel + "_whatthehellguys.db")
		if "last_message" not in self.shelf:
			self.shelf["last_message"] = time.time()
		
		self.graph = GraphUpdaterThread(self.bot.channel)
		self.graph.start()
		
	def get_level(self):
		if "level" not in self.shelf:
			self.shelf["level"] = 1
		return self.shelf["level"]
	def set_level(self, new_level):
		self.shelf["level"] = new_level if new_level <= 1 else 1
	level = property(fget=get_level, fset=set_level)
		
	def get_auto_comment(self):
		if "auto_comment" not in self.shelf:
			self.shelf["auto_comment"] = False
		return self.shelf["auto_comment"]
	def set_auto_comment(self, new_auto_comment):
		self.shelf["auto_comment"] = new_auto_comment
	auto_comment = property(fget=get_auto_comment, fset=set_auto_comment)
	
	def on_channel_message(self, source_name, source_host, message):
		old_level = self.level
		if self.innapropriate(message):
			if self.level <= old_level*0.5 and self.auto_comment:
				self.on_level_request(source_name, source_host, message)
		else:
			time_since_last_message = time.time() - self.shelf["last_message"]
			self.level += time_since_last_message * RECOVERY_RATE_PER_SECOND
			self.level += RECOVERY_RATE_PER_MESSAGE
		
		self.graph.update(self.level * 100)
		
		self.shelf["last_message"] = time.time()
	
	def innapropriate(self, message):
		is_innapropriate = False
		
		for rule in rules:
			if re.match(rule, message, re.I):
				self.level *= rules[rule]
				is_innapropriate = True
		
		return is_innapropriate
	
	@on_addressed_match("don'?t judge me!?", re.I)
	def on_stfu(self, source_name, source_host, message):
		self.bot.say("Sorry! I'll shut up.")
		self.auto_comment = False
	
	#           Sorry but you have to take these people into account |
	@on_addressed_match("tell (?:me|us) if (?:this|we) (?:gets (?:too? )bad|goes too? far)", re.I)
	def on_tell_me_if_this_gets_bad(self, source_name, source_host, message):
		self.bot.say("I'll do what I can.")
		self.auto_comment = True
	
	@on_addressed_match("what the hell(?: guys)?.*", re.I)
	def on_level_request(self, source_name, source_host, message):
		if self.level == 1:
			self.bot.say("The tone of conversation is oddly 100% healthy.")
		elif self.level > 0.9:
			self.bot.say("The level of conversation is a decent %1.0f%%"%(self.level*100,))
		elif self.level > 0.5:
			self.bot.say("Keep it classy, guys, (Conversation tone at %1.0f%%)"%(self.level*100,))
		elif self.level > 0.2:
			self.bot.say("Please! Come on! %1.0f%% tone wtf?!"%(self.level*100,))
		elif self.level > 0:
			self.bot.say("Conversation tone is at %1.0f%%. Really?"%(self.level*100,))
		elif self.level == 0:
			self.bot.say("The geneva conventions kick in at this point: Conversational tone at 0%")
	def die(self):
		self.shelf.close()
		self.graph.stop()



class GraphUpdaterThread(threading.Thread):
	
	update_url = "http://tnutils.appspot.com/graphs/wthg_%s/set"
	
	def __init__(self, channel):
		threading.Thread.__init__(self)
		
		# The 'set' url
		self.url = self.update_url % channel.lstrip('#')
		self.title = channel
		
		self.condition = threading.Condition()
		self.new_value = False
		self.value = None
		self.running = True
		self._notify = False
		
		
	def stop(self):
		with self.condition:
			self.running = False
			self.notify()
		
		self.join()
		
		
	def update(self, value):
		with self.condition:
			self.new_value = True
			self.value = value
			self.notify()
		
		
	def notify(self):
		self._notify = True
		self.condition.notify()
		
		
	def run_update(self, value):
		urllib2.urlopen(self.url, "value=%i" % value)
		with self.condition:
			self.new_value = False
		
		
	def run(self):
		# set the graph title
		urllib2.urlopen(self.url, "title=%s" % self.title)
		
		while self.running:
			# Update if there's a new value.
			with self.condition:
				new_value = self.new_value
				value = self.value
			if new_value:
				self.run_update(value)
		
			# Repeat if there's a new value, otherwise wait.
			with self.condition:
				if self._notify:
					self._notify = False
					continue
				else:
					self.condition.wait()
