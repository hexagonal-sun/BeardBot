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
		eval_found = evalFinder.search(message)
		equal_found = equalFinder.search(message)
		try:
			if eval_found:
				source = eval_found.group(1)
				result = self.eval(source)
				self.locals['_'] = result
				self.bot.say(repr(result)[:200])
			elif equal_found:
				dest = equal_found.group(1)
				source = equal_found.group(2)
				self.locals[dest] = self.eval(source)
				self.bot.say("%s = %s" % (dest, self.locals[dest]))
		except Exception, e:
			self.bot.say("I'm afraid I can't let you do that, Dave.")

	def eval(self, source):
		return eval(source, self.locals, self.locals)
	
