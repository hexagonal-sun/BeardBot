from base_module import *
import time, datetime, re

hasUserSaid = re.compile("(has|did) ([^\s]+) (said|say) (.*)",
                         re.IGNORECASE)

hasSomeoneSaid = re.compile("(who said|(has|did)( someone| somebody| anyone)?( say)?) (.*)",
                            re.IGNORECASE)

requiredBeardBotVersion = 0.1
class BeardBotModule(ModuleBase):
	def __init__(self, bot):
		self.bot = bot
		self.logger = Logger(self.bot.channel)
	
	def on_channel_message(self, source_name, source_host, message):
		self.logger.log(source_name, message)
	
	def on_addressed_message(self, source_name, source_host, message):
		hasSaidMatch = hasUserSaid.match(message)
		hadMatch = hasSomeoneSaid.match(message)
		
		if hasSaidMatch:
			user = hasSaidMatch.groups()[1]
			query = hasSaidMatch.groups()[3]
			self.has_user_said(user, query)
		elif hadMatch:
			query = hadMatch.groups()[-1]
			self.who_said(query)
		else:
			self.logger.log(source_name, message, 1)
	
	def who_said(self, query):
		"""
		Find out who said the given string last and when
		"""
		try:
			if query.startswith("/"):
				query = query[1:]
			else:
				query = ".*%s.*"%(query,)
			user, message, date_time = self.logger.who_said(query)
			date_time = datetime.datetime.fromtimestamp(date_time)
			date_time = date_time.strftime("%H:%M:%S on %A %d %B %Y")
			self.bot.say("%s last said \"%s\" at %s."%(user, message, date_time))
		except TypeError:
			self.bot.say("I can't remember anyone saying that...")
	
	def has_user_said(self, user, query):
		"""
		Find out if a user has said something and report when and how many times.
		"""
		try:
			if query.startswith("/"):
				query = query[1:]
			else:
				query = ".*%s.*"%(query,)
			message, date_time = self.logger.has_user_said(user, query)
			date_time = datetime.datetime.fromtimestamp(date_time)
			date_time = date_time.strftime("%H:%M:%S on %A %d %B %Y")
			self.bot.say("Yep. The last time was: \"%s\" at %s."%(message, date_time))
			
			how_often = self.logger.how_often_does_user_say(user, query)
			if how_often > 1:
				self.bot.say("Infact %s says it quite a bit: %i times today!"%(user, how_often))
		except TypeError:
			self.bot.say("Nope.")
	
	def die(self):
		self.logger.close()

import sqlite3
class Logger(object):
	def __init__(self, filename="logs"):
		self.db = sqlite3.connect(filename + "_log.db")
		self.initialise_db()
		
	def initialise_db(self):
		c = self.db.cursor()
		c.execute("""
			CREATE TABLE IF NOT EXISTS
				ChatLog (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					dateTime INTEGER,
					user VARCHAR(9),
					message TEXT,
					addressed BOOLEAN
				)
		""")
		self.db.commit()
		
		def regexp(search, string):
			if re.match(search, string, re.IGNORECASE):
				return 1
		
		self.db.create_function("regexp", 2, regexp)
	
	def log(self, user, message, addressed=0):
		user = user.lower()
		c = self.db.cursor()
		c.execute("""
			INSERT INTO ChatLog ( dateTime, user, message, addressed)
			VALUES ( ?, ?, ? , ?)
		""", (time.time(), user, message, addressed))
		self.db.commit()
	
	def get_user_log(self, user, addressed=None):
		user = user.lower()
		c = self.db.cursor()
		extraSQL = ""
		query = [user,]
		if addressed != None:
			extraSQL = "AND addressed = ?"
			query.append(addressed)
		c.execute("""
			SELECT dateTime, message FROM ChatLog
			WHERE user = ? """ + extraSQL, query)
		for row in c:
			yield row
		return
	
	def who_said(self, query):
		c = self.db.cursor()
		c.execute("""
			SELECT user, message, dateTime FROM ChatLog
			WHERE
				message REGEXP ?
			ORDER BY dateTime DESC
			LIMIT 1""", (query,))
		result = c.fetchall()
		if len(result) == 1:
			return result[0]
		else:
			return None
	
	def has_user_said(self, user, query):
		c = self.db.cursor()
		c.execute("""
			SELECT message, dateTime FROM ChatLog
			WHERE
				user = ? AND
				message REGEXP ?
			ORDER BY dateTime DESC
			LIMIT 1""", (user, query))
		result = c.fetchall()
		if len(result) == 1:
			return result[0]
		else:
			return None
	
	def how_often_does_user_say(self, user, query):
		c = self.db.cursor()
		c.execute("""
			SELECT count(*) FROM ChatLog
			WHERE
				user = ? AND
				message REGEXP ? AND
				datetime >= ?
			""", (user, query, time.mktime(datetime.date.today().timetuple())))
		result = c.fetchall()
		if len(result) == 1:
			return result[0][0]
		else:
			return 0
	
	def close(self):
		self.db.close()

if __name__=="__main__":
	l = Logger("test")
	l.log("heathcj9", "Hi there")
	l.close()
	
