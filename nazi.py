from base_module import *
import re
from enchant.checker import SpellChecker

is_a_word = re.compile("(\S+) is a word!?")
yes_i_do = re.compile("yes i (.*)do", re.IGNORECASE)
requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	def __init__(self, *args, **kwargs):
		ModuleBase.__init__(self, *args, **kwargs)
		self.spell_checker = SpellChecker("en_UK")
		self.last_word = None

	def on_channel_message(self, source_name, source_host, message):
		self.spell_checker.set_text(message)
		for error in self.spell_checker:
			self.bot.say("%s? You call that a word?" % error.word)
			self.last_word = error.word

	def on_addressed_message(self, source_name, source_host, message):
		is_a_word_match = is_a_word.search(message)
		yes_i_do_match = yes_i_do.search(message)
		if is_a_word_match:
			word = match.group(1)
			self.bot.say("You're right, %s is a word :(" % word)
			self.spell_checker.add(word)
		elif yes_i_do_match and self.last_word:
			self.spell_checker.add(self.last_word)
			self.bot.say("Yes Master...")
		
