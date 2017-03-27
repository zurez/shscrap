import sqlite3

#Variables
DB="hasher.db"
TABLE="imagehash"
conn = sqlite3.connect(DB)
print "Connected to "+DB
try:
	conn.execute('''CREATE TABLE imagehash
       (ID INTEGER PRIMARY KEY   AUTOINCREMENT ,
       HASH           TEXT    NOT NULL
       );''')
except Exception as e:
	# raise e
	pass

print "Connected to table "+TABLE
def insert(hashValue,conn=conn,table=TABLE):
	cursor=conn.cursor()
	cursor.execute('INSERT INTO '+table+'(HASH) VALUES(?)',(hashValue,))
	conn.commit()		
def select(hashValue,conn=conn,table=TABLE):
	cursor=conn.cursor()
	query=cursor.execute('SELECT HASH FROM '+table+' WHERE HASH = ?',(hashValue,))
	conn.commit()
	return query.fetchall()
def createInsertQuery(hashValue,table=TABLE):
	query="",
	return query
def createSelectQuery(hashValue,table=TABLE):
	query="SELECT HASH from "+table+" where HASH='"+hashValue+"'"
	return query
def runQuery(query,conn=conn):
	ret=conn.execute(query)
	conn.commit()
	conn.close()
	return ret
# query=insert("test123")
# print query
if __name__ == '__main__':
	# main()
	print select('test123')
# runQuery(query)
# query=createSelectQuery("test123")
# print query