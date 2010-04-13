#!/usr/bin/python
# Beardy: Uses Markov chains to generate random sentences given a particular
# piece of test data. Fun stuff.
#
# Create a Beard object 

import sys, random

def weightedPick(d):
	"""
	Pick a random item from a dictionary containing item : weight pairs, assumming
	the weights are normalized. Raises an exception if no element could be
	piecked.
	"""
	rand = random.random()
	s = 0
	for key, weight in d.iteritems():
		s += weight
		if rand <= s:
			return key
	raise Exception("No element picked")

class Word(object):
	"""
	A chain of words which also contains references to word chains which follow
	it along with the number of occurrences of each. It is also able to output a
	normalized version.
	"""
	def __init__(self, word):
		# The word-chain this object represents
		self.word = word
		# The dictionary containing Word : frequency for all words this is related
		# to.
		self.rawRelations = {}
		
		# A cached dictionary which is a normalized version of the above
		self._relations = {}
	
	def __hash__(self):
		"""
		Hash this word chain -- note that the relations are irelevent
		"""
		return self.word.__hash__()
	
	def followedBy(self, otherWord):
		"""
		Count the fact that this worchain is followed by the passed wordchain.
		"""
		if self.rawRelations.has_key(otherWord):
			self.rawRelations[otherWord] += 1
		else:
			self.rawRelations[otherWord] = 1
	
	@property
	def relations(self):
		"""
		A normalized version of the dictionary of the wordschains which can follow
		this one.
		"""
		if len(self._relations) != len(self.rawRelations):
			normalizedRelations = {}
			
			sumOfFrequencies = float(sum(self.rawRelations.itervalues()))
			for word, frequency in self.rawRelations.iteritems():
				normalizedRelations[word] = float(frequency) / sumOfFrequencies
			self._relations = normalizedRelations
		return self._relations
	
	def __str__(self):
		return str(self.word)
	__repr__=__str__

class Beard(object):
	"""
	A markov process which can be trained and then generate sentences.
	"""
	def __init__(self, order = 2):
		"""
		Create a beard. Specify the order of the chain.
		"""
		# A list of words found by the system
		self.words = {}
		
		# The oder of the process to use. Must be 1 or greater
		self.order = order
	
	def getWord(self, word):
		"""
		For internal use...
		Return a refrence to a Word object which represents the provided wordchain.
		If one does not exist, create it.
		"""
		if not self.words.has_key(word):
			self.words[word] = Word(word)
		return self.words[word]
	
	def train(self, *trainingData):
		"""
		Supply a sentence as a string and nodes will be made out of each word and
		used as training information. This function is incremental (i.e. subsiquent
		calls add to training data).
		"""
		for sentence in trainingData:
			# If this sentence isn't empty
			words = sentence.strip().split()
			if len(words) != 0:
				# Append an ending word of "." which is used to signal the end of a
				# chain
				words.append(False)
				
				# Strip out any empty words (e.g. double spaces etc.)
				words = filter((lambda x : x != ""), words)
				
				# Generate a moving grouping of words apropriate for the current order
				# size. E.g. a b c d becomes ab bc cd for order 2.
				wordGroups = [
					tuple([ word for word in words[offset : offset + self.order] ])
					for offset in range (len(words) - self.order + 1)
				]
				
				# The "start" of any chain is the empty word
				lastWord = self.getWord(tuple([True]))
				
				# Loop through all the words, each time adding it to the previous word's
				# refrence list.
				for wordGroup in wordGroups:
					thisWord = self.getWord(wordGroup)
					lastWord.followedBy(thisWord)
					lastWord = thisWord
	
	def generate(self):
		"""
		Generate a random sentence using this chain.
		"""
		if len(self.words) == 0:
			return None
		
		output = ""
		word = self.getWord(tuple([True]))
		endWord = self.getWord(tuple([False]))
		while word.__hash__() != endWord.__hash__():
			if len(word.relations) != 0:
				if word.word[0] != True:
					output += word.word[0] + " "
				word = weightedPick(word.relations)
			else:
				output += " ".join(word.word)
				break
		return output

if __name__=="__main__":
	if len(sys.argv) == 3:
		inFile = open(sys.argv[1], "r")
		trainingData = inFile.read().split("\n")
		
		beard = Beard(int(sys.argv[2]))
		beard.train(*trainingData)
		
		while True:
			print beard.generate()
			raw_input()
	else:
		print "usage: trainingfile order"
