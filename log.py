import bot, time

requiredBeardBotVersion = 0.1
class BeardBotModule(bot.BeardBotModule):
	def __init__(self, bot):
		self.bot = bot
		self.logger = Logger(self.bot.channel)
	
	def on_channel_message(self, source_name, source_host, message):
		self.logger.log(source_name, message)
	
	def on_addressed_message(self, source_name, source_host, message):
		self.logger.log(source_name, message, 1)
		# Check for commands...
	
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
	
	def log(self, user, message, addressed=0):
		c = self.db.cursor()
		c.execute("""
			INSERT INTO ChatLog ( dateTime, user, message, addressed)
			VALUES ( ?, ?, ? , ?)
		""", (time.time(), user, message, addressed))
		self.db.commit()
	
	def get_user_log(self, user, addressed=None):
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
	
	def close(self):
		self.db.close()

if __name__=="__main__":
	l = Logger("test")
	l.log("heathcj9", "Hi there")
	l.close()
	
