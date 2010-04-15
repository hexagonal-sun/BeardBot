import re


class ModuleBase(object):
	"""
	The superclass of all BeardBot modules.
	At least one of on_channel_message, on_addressed_message and on_private_message
	should be overridden by module implementations.
	"""
	def __init__(self, bot):
		self.bot = bot


	def test_for_matches(self, match_type, source_name, source_host, message):
		"""
		Call 'call_if_match'on each attribute of type 'match type'.
		"""
		for attribute in (getattr(self, attr_name) for attr_name in dir(self)):
			if isinstance(attribute, match_type):
				attribute.call_if_match(self, source_name, source_host, message)


	def handle_channel_message(self, source_name, source_host, message):
		"""
		Called on every channel message not addressed to the bot.
		"""
		self.test_for_matches(on_channel_match, 
		                      source_name, source_host, message)
		self.on_channel_message(source_name, source_host, message)

	def handle_addressed_message(self, source_name, source_host, message):
		"""
		Called on every channel message addressed to the bot.
		"""
		self.test_for_matches(on_addressed_match, 
		                      source_name, source_host, message)
		self.on_addressed_message(source_name, source_host, message)

	def handle_private_message(self, source_name, source_host, message):
		"""
		Called on every private message addressed to the bot.
		"""
		self.test_for_matches(on_private_match, 
		                      source_name, source_host, message)
		self.on_private_message(source_name, source_host, message)


	def on_channel_message(self, source_name, source_host, message):
		"""
		Called by handle_channel_message on every 
		channel message not addressed to the bot.
		This should be overridden in module implementations. 
		"""
		pass

	def on_addressed_message(self, source_name, source_host, message):
		"""
		Called by handle_addressed_message on every 
		channel message addressed to the bot.
		This should be overridden in module implementations. 
		"""
		pass

	def on_private_message(self, source_name, source_host, message):
		"""
		Called by handle_private_message on every 
		private message addressed to the bot.
		This should be overridden in module implementations. 
		"""
		pass


	def die(self):
		"""Called Before the module is removed."""
		pass


	
class on_match(object):
	"""
	A decorator for module functions, that cause the function 
	to be called when the passed regular expression matches a message.
	This should not be used directly - use one of on_*_match defined below.
	"""
	def __init__(self, expression, flags=0, search=False):
		"""
		expression - The regular expression to be matched.
		flags      - The flags to be passed to the re matcher.
		search     - If True, use re.search to match, otherwise re.match
		"""
		self.re = re.compile(expression, flags)
		self.search = False
		
		
	def __call__(self, *args, **kwargs):
		# The first time this is called, store the function to be decorated 
		if not hasattr(self, "func"):
			self.func = args[0]
			return self
		# Next time, call the function to make it look like the original function.
		else:
			return self.func(*args, **kwargs)


	def call_if_match(self, parent, source_name, source_host, message):
		"""
		Call the enclosed function if the re matches message.
		'parent' is the object that it should be called from (ie, the module)
		The enclosed function is called with the groups from the 
		regular expression argument appended to the argument list.
		"""
		if self.search: 
			match = self.re.search(message)
		else:
			match = self.re.match(message)
		if match:
			self.func(parent,
			          source_name, source_host, message,
			          *match.groups())



class on_channel_match(on_match):
	pass

class on_addressed_match(on_match):
	pass

class on_private_match(on_match):
	pass


