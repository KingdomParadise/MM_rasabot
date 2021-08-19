# tester app to exercised Flask

from flask import Flask, render_template, request
import sqlite3 as sql
from string import Template
from OpenSSL import SSL
import pickle
from rasa.nlu.model import Interpreter
import requests
import json

API_ENDPOINT = "http://localhost:5005/webhook"
data_id = 0
messagePayload = ''
selected_item = ''
selected_category = ''
#connect to qa_database.sq(database will be created, if not exist)
#con = sql.connect('qa.database.db')
#con.execute('CREATE TABLE IF NOT EXISTS tbl_QA (ID INTEGER PROMARY KEY ,'+' program TEXT,first_name TEXT,last_name TEXT,middle_name TEXT,second_last_name TEXT,suffix TEXT,date TEXT,last_four_social TEXT,residential_address TEXT,shipping_address TEXT,apt_unit1 TEXT,apt_unit2 TEXT,address_nature TEXT,form_filled BOOL,form_zip_code TEXT)')
#con.close


app = Flask(__name__,template_folder='template')


# @app.route('/animals', methods=['GET', 'POST'])
# @app.route('/')
@app.route('/')
def homepage():   
    return render_template('root/index.html')

@app.route('/start')
def iehStart():
    return render_template('root/start.html')
@app.route('/submit_form',methods = ['POST'])
def iehStart():
    return render_template('root/thank.html')
@app.route('/multi',methods = ['POST'])
def multiwebform():
        program_value = request.form['program_value']
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        second_last_name = request.form['second_last_name']
        suffix = request.form['suffix']
       # toggleaddress = 'toggleaddress' in request.form.keys()
        apt_unit1 = request.form['apt_unit1']
        apt_unit2 = request.form['apt_unit2']
        address_nature = request.form['address_nature']
        shipping_address = request.form['shipping_address']
        residence_address = request.form['residence_address']
        zipcode = request.form['zipcode']
        last_four_social = request.form['last_four_social']
        month = request.form['month']
        day = request.form['day']
        year = request.form['year']
        date = month+"-"+day+"-"+year
        form_filled = True
       # try:
       #     con = sql.connect('qa_database.db')
       #     c =  con.cursor() # cursor
            # insert data
       #     c.execute("INSERT INTO tbl_QA (program,first_name,last_name,middle_name,second_last_name,suffix,date,last_four_social,residential_address,shipping_address,apt_unit1,apt_unit2,address_nature,form_filled,form_zip_code) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(program_value,first_name,last_name,middle_name,second_last_name,suffix,date,last_four_social,residence_address,shipping_address,apt_unit1,apt_unit2,address_nature,form_filled,zipcode))
       #     con.commit() # apply changes
       # finally:
       #     con.close()
       # print(program_value,first_name,middle_name,last_name,second_last_name,suffix,apt_unit1,address_nature,last_four_social,month,day,year,date)
        
        return ":) Submitted!"
@app.route('/getmultiinfo',methods=['GET'])
def getMultiInfo():
   # try:
   #     con = sql.connect('qa_database.db')
   #     c = con.cursor()
   #     id = c.execute("Select count(table.id) from table")
   #     query ="Select answer FROM tbl_QA where id = {0}".format(id)
   #     c.execute(query)
   #     response = c.fetchone()[0] # fetch and store tuple-value (see [0])
   #     con.commit() 
    #finally:    
    #    con.close()
    # then display the error in 'database_error.html' page
    #print(response)
    #return response
    return
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')