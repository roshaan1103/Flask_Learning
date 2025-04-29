from flask import Flask,render_template,request,url_for
from flask_mysqldb import MySQL
from datetime import *
from jira import JIRA

api_key= "#Your Jira API key"
app = Flask(__name__)

app.config['MYSQL_HOST'] = '192.168.18.246'
app.config['MYSQL_USER'] = 'roshaan'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'alnafi'
mysql= MySQL(app)

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

		if not fname_data or not lname_data or not design_data or not course_data:
			error_message = "All fields are required!"
			return render_template("trainer_details.html", error=error_message)

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

@app.route("/trainerdata", methods=['POST', 'GET'])
def trainer_data():
	cursor = mysql.connection.cursor()
	sql = "select * from trainer_details"
	cursor.execute(sql)
	row = cursor.fetchall()

	return render_template("trainer_display.html", output_data=row)

# @app.route("/ticket", methods=['POST', 'GET'])
# def Jira_ticket_creation():
#
#
# 	if request.method == "POST":
# 		project_data = request.form['project']
# 		issuetype_data=request.form['issuetype']
# 		reporter_data = request.form['reporter']
# 		summary_data = request.form['summary']
# 		description_data = request.form['Description']
# 		priority_data = request.form['priority']
#
# 		if not project_data or not issuetype_data or not reporter_data or not summary_data or not description_data or not priority_data:
# 			error_message = "All fields are required!"
#
# 	server = 'https://roshaanjiralearn.atlassian.net'
# 	user = "roshaanwork03@gmail.com"
# 	jira =JIRA(server,basic_auth=(user,api_key))
# 	issue= jira.create_issue(project_data='project',issuetype_data='issuetype',reporter_data='reporter',summary_data='summary',description_data='description',priority_data='priority')
# 	print(issue)
# 	return render_template("Jira_ticket_creation.html")
@app.route("/ticket", methods=['POST', 'GET'])
def Jira_ticket_creation():
	if request.method == "POST":
		project_data = request.form.get('project')
		issuetype_data = request.form.get('issuetype')
		reporter_data = request.form.get('reporter')  # Usually this is set via authentication, not manually
		summary_data = request.form.get('summary')
		description_data = request.form.get('Description')
		priority_data = request.form.get('priority')

		# Check required fields
		if not all([project_data, issuetype_data, summary_data, description_data, priority_data]):
			error_message = "All fields are required!"
			return render_template("Jira_ticket_creation.html", error=error_message)

		# Jira setup
		server = 'https://roshaanjiralearn.atlassian.net'
		user = "roshaanwork03@gmail.com"
		jira = JIRA(server=server, basic_auth=(user, api_key))

		issue_dict = {
			'project': {'key': project_data},
			'summary': summary_data,
			'description': description_data,
			'issuetype': {'name': issuetype_data},
			'priority': {'name': priority_data},
		}

		try:
			new_issue = jira.create_issue(fields=issue_dict)
			success_message = f"Issue {new_issue.key} created successfully!"
			return render_template("Jira_ticket_creation.html", success=success_message)
		except Exception as e:
			error_message = f"Failed to create issue: {str(e)}"
			return render_template("Jira_ticket_creation.html", error=error_message)

	# For GET requests
	return render_template("Jira_ticket_creation.html")

if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0') #Debug=True to make sure you can edit while its running and host=0.0.0.0 means that any ip with same type can access it and port= can be used to set a desired port
	# You have to restart the code if you make changes to config file (this function) even if there is debug=True


