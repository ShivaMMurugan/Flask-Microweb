from datetime import datetime
import smtplib
import os
from flask import Flask, render_template, request
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email
from flask_pymongo import PyMongo


# DOMAIN_PASSWORD.

'''Email ID and Passwords are stored in 
   enviorment variable'''

EMAIL_ADDRESS = os.environ.get('DOMAIN_NAME')
EMAIL_PASSWORD = os.environ.get('DOMAIN_PASS')

class ContactMeForm(FlaskForm):

	Firstname = StringField('Firstname',
				validators=[DataRequired(), Length(min=2, max=20)])
	Email     = StringField('Email',
				validators=[DataRequired(), Email()])
	Subject   = StringField('Subject')
	Message   = TextAreaField('Message')

	send_message = SubmitField('Send Message')

app = Flask(__name__)
app.config['SECRET_KEY'] = '6c6958bc19ee93f0596085fae014ed9a'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/users'
mongo = PyMongo(app)

@app.route('/', methods=['GET', 'POST'])
def flaskBlog():
	form = ContactMeForm()
	if request.method == 'POST':
		fname = request.form.get('Firstname')
		email = request.form.get('Email')
		subject = request.form.get('Subject')
		msg = request.form.get('Message')
		message = request.form.get('Send Message')
		date_recieved = datetime.today()
		smtp = smtplib.SMTP('smtp.gmail.com', 587)

		smtp.ehlo()
		smtp.starttls()
		smtp.ehlo()

		smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
		message_to_visitor = "Thank you for submitting the form, will get back to you soon."
		smtp.sendmail(EMAIL_ADDRESS, email, message_to_visitor)
		
		online_users = mongo.db.info.insert({"firstname": fname, 
						"email": email, "subject": subject, 'message': msg,
						"date_recieved": date_recieved})

	return render_template('home.html', form=form)


if __name__ == '__main__':

	app.run(debug=True)
