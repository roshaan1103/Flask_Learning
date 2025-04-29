from flask import Flask,render_template,request,url_for
from flask_mysqldb import MySQL
from datetime import *
import mysql.connector


app = Flask(__name__)

app.config['MYSQL_HOST'] = '#Mysql ipaddress'
app.config['MYSQL_USER'] = '#mysql user'
app.config['MYSQL_PASSWORD'] = '#Mysql user's password'
app.config['MYSQL_DB'] = '#database name '
mysql= MySQL(app)

mydata = "HOME PAGE"
mycontact = "Contact Us"


@app.get("/")
def get_Home():
	return mydata

@app.get("/contact")
def get_contact():
	return mycontact

@app.get("/trainer")
def trainer():
	return render_template("trainer_details.html")

@app.route("/trainer_create",methods=['POST','GET'])
def trainer_create():
	if request.method == "POST":
		fname_data=request.form['fname']
		lname_data = request.form['lname']
		design_data = request.form['design']
		course_data = request.form['course']
		cdate= date.today()
		sql = "INSERT INTO trainer_details (fname,lname,design,course,datetime) VALUES (%s,%s,%s,%s,%s)"
		val= (fname_data,lname_data,design_data,course_data,cdate)

		#Connection:
		cursor = mysql.connection.cursor()


		#execute SQL Query:
		cursor.execute(sql,val)

		#commit:
		mysql.connection.commit()
		#conn.commit()


		#close:
		cursor.close()
		#conn.close()
		return render_template("trainer_details.html")

if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0') #Debug=True to make sure you can edit while its running and host=0.0.0.0 means that any ip with same type can access it and port= can be used to set a desired port
	# You have to restart the code if you make changes to config file (this function) even if there is debug=True


