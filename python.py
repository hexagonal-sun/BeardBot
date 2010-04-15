from base_module import *
import re
import __builtin__
import multiprocessing, time


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
default_locals["sleep"] = time.sleep


def truncate(msg):
	return msg if len(msg) < 200 else msg[:200] + "..."


requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	def __init__(self, *args, **kwargs):		
		bot.BeardBotModule.__init__(self, *args, **kwargs)
		self.locals = default_locals


	def on_addressed_message(self, source_name, source_host, message):		
		eval_found = evalFinder.search(message)
		equal_found = equalFinder.search(message)
		try:
			if eval_found:
				source = eval_found.group(1)
				result = self.eval_timed(source)
				self.locals['_'] = result
				self.bot.say(truncate(repr(result)))
			elif equal_found:
				dest = equal_found.group(1)
				source = equal_found.group(2)
				self.locals[dest] = self.eval_timed(source)
				self.bot.say(truncate("%s = %s" % (dest, self.locals[dest])))
		except Exception, e:
			self.bot.say("I'm afraid I can't let you do that, Dave.")
			print dir(e)


	def eval(self, source):
		return eval(source, self.locals, self.locals)


	def eval_timed(self, source):
		def target(self, source, conn, done):
			conn.send(self.eval(source))
			conn.close()
			done.set()
			
		parent_conn, child_conn = multiprocessing.Pipe()
		done = multiprocessing.Event()
		p = multiprocessing.Process(target=target, args=(self, source, child_conn, done))
		p.start()
		done.wait(0.5)
		p.terminate()

		if done.is_set():
			return parent_conn.recv()
		else:
			raise Exception()
		
	
