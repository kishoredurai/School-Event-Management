import MySQLdb.cursors
import mysql.connector
from mysql import connector


import mysql.connector

mydb = mysql.connector.connect(
  host="121.200.55.42",
    port="4063",
  user="cloud",
  password="cloud@123",
database="elearning"
)
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM content_video,course_chapter_content where content_video.chapter_content_id = course_chapter_content.chapter_content_id and course_chapter_content.course_chapter_id =1004 ")

myresult = mycursor.fetchall()
print(myresult)