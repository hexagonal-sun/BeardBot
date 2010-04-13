class BeardBotPlugin(object):
	def __init__(self, bot):
		self.bot = bot
		self.messages = {}
	
	def log(user, message):
		self.messages[user].append(message)
