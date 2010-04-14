import bot, re
import __builtin__

evalFinder = re.compile("eval\((.+)\)[^\)]*")
equalFinder = re.compile("(\w*)\s*=\s*(.*)")
allowed_builtins = ['Ellipsis', 'False', 'None', 'True', 'abs', 'all', 'any',
		    'apply', 'basestring', 'bin', 'bool', 'chr', 'cmp',
		    'coerce', 'complex', 'delattr', 'dict', 'dir', 'divmod',
		    'enumerate', 'filter', 'float', 'format', 'frozenset',
		    'getattr', 'hasattr', 'hash', 'hex', 'int', 'isinstance',
		    'issubclass', 'iter', 'len', 'list', 'long', 'map', 'max',
		    'min', 'next', 'object', 'oct', 'ord', 'pow', 'property',
		    'range', 'reduce', 'repr', 'reversed', 'round', 'set',
		    'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum',
		    'tuple', 'type', 'unichr', 'unicode', 'xrange', 'zip']

default_locals = dict((k, v) 
		      for k, v 
		      in vars(__builtin__).iteritems() 
		      if k in allowed_builtins)

default_locals["__builtins__"] = None

requiredBeardBotVersion = 0.1
class BeardBotModule(bot.BeardBotModule):
	def __init__(self, *args, **kwargs):		
		bot.BeardBotModule.__init__(self, *args, **kwargs)
		self.locals = default_locals


	def on_addressed_message(self, source_name, source_host, message):		
		found = evalFinder.search(message)
		if found:
			source = found.group(1)
			try:
				result = self.eval(source)
				self.locals['_'] = result
				self.bot.say(repr(result)[:200])
			except:
				self.bot.say("I'm afraid I can't let you do that, Dave.")

	def eval(self, source):
		return eval(source, self.locals, self.locals)
	
