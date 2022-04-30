from crypt import methods
from distutils.log import error
from inspect import Attribute
from flask import Flask, redirect, url_for, render_template, request, flash, session, jsonify
from pyjsonq import JsonQ
import os
import zipfile
import db_mongodb as db
import csv
import json
from flask import flash


#-------------------------------------flask---------------------------------------------
app = Flask(__name__, template_folder='template') #creating the Flask class object   
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['Files_upload']="./Files_upload"


#--------------------------home-----------------------
@app.route('/') 
def home():  
    flag = [1]
    return render_template('index.html', flag = flag);


#-------------------------------get_table ajax----------------------------------
@app.route('/get_tablename', methods = ['POST', 'GET'])
def get_tablename():
    file_path = session['file_path']
    #print(file_path)

    result = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]

    tables = {}
    i = 0

    for nm in result:
        if 'json' in nm:
            t = nm.split('.')[0]
            tables[i] = t
            i+=1

    #print(tables)

    #return str(tables)
    return jsonify(tables)


#-----------------------------------------sent tablename ajax--------------------------------
@app.route('/send_tablename' , methods = ['POST', 'GET'])
def sent_tablename():
    if request.method == "POST":
        json_tb = request.get_json()
        #print("hello")
        #print(json_tb)
        table_name = json_tb[0]['table']
        session['table_name'] = table_name
    return "Done"




#-----------------------------------------get column ajax--------------------------------
@app.route('/get_colname' , methods = ['POST', 'GET'])
def get_colname():
    file_path = session['file_path']

    result = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]

    table_name = session['table_name']

    temp = table_name + "_meta.txt"

    col = {}
    i=0
    #print("result     ->",result)
    #print("temp    ->",temp)
    for nm in result:
        if nm == temp:
            filepath = file_path + '/' + temp
            #print("dumdgwve")
            columns = db.get_columns(filepath)
            break
    #print("COlumns     ->",columns)
    for c in columns:
        col[i] = c
        i+=1

    #print(col)
    return jsonify(col)



#-----------------------------------------sent column name ajax--------------------------------
@app.route('/send_colname' , methods = ['POST', 'GET'])
def sent_colname():
    #print("goooooooooooo")
    if request.method == "POST":
        json_col = request.get_json()
        #print(json_col)
        col_name = json_col[0]['col']
        #rint(col_name)
        session['col_name'] = col_name
    return "Done"


#-----------------------------------------sent operator ajax--------------------------------
@app.route('/send_op' , methods = ['POST', 'GET'])
def sent_op():
    if request.method == "POST":
        json_op = request.get_json()
        operator = json_op[0]['op']
        session['operator'] = operator

        # print(session['table_name'])
        # print(session['col_name'])
        # print(session['operator'])
    return "Done"



#-----------------------------------------------upload success for simple query------------------------
@app.route('/upload_success1')
def upload_success1():
    flash("The Data has been uploaded successfully!", 'simple_query')
    flag = [1]
    return render_template("index.html", flag = flag)


#-----------------------------------------------upload success for complex query------------------------
@app.route('/upload_success2')
def upload_success2():
    flash("The Data has been uploaded successfully!", 'complex_query')
    flag = [2]
    return render_template("index.html", flag = flag)


#-----------------------------------------------incorrect query for complex query------------------------
@app.route('/incorrect_query')
def incorrect_query():
    flash("The Query is incorrect", 'complex_query')
    return render_template("index.html", flag = [2])


#---------------------------------------------no records found-----------------------------
@app.route('/no_op')
def no_op():
    flash("No Records Found !!", 'complex_query')
    return render_template("index.html", flag = [2])

#---------------------------------------------no records found-----------------------------
@app.route('/no_op_simple')
def no_op_simple():
    flash("No Records Found !!", 'simple_query')
    return render_template("index.html", flag = [1])


#-------------------------------------------Simple Query---------------------------------
@app.route('/simple_query', methods=['POST', 'GET'])
def simple_query():

    if request.method == 'POST':
        #print("Hello123")

        #----------------------------------Choose File button---------------------
        if request.form['action'] == 'go':
            #pass
            fle = request.files['choose_btn']
            #print(fle)

            file_name = fle.filename
            #print(file_name)

            fle.save(os.path.join(app.config["Files_upload"],fle.filename))

            path = app.config['Files_upload'] + "/" + file_name

            # unzip krne ka code
            home = app.config['Files_upload']
            
            path_to_zip_file=path
            with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
                zip_ref.extractall(home)
            
            f_path = file_name.split('.')[0]
            final_path = home + '/' + f_path
            #print(final_path)

            session['db_name'] = f_path
            result = [f for f in os.listdir(final_path) if os.path.isfile(os.path.join(final_path, f))]

            column_dict = {}

            for nm in result:
                if 'txt' in nm:
                    txt_path = final_path + '/' + nm
                    lst = db.get_columns(txt_path)
                    temp = nm.split('.')[0]
                    table_name = temp.split('_')[0]
                    column_dict[table_name] = lst

                elif 'json' in nm:
                    json_path = final_path + '/' + nm
                    table_name = nm.split('.')[0]
                    database_name = f_path
                    # print("The table name = ", table_name)
                    # print("The json path = ", json_path)
                    # print("The db name = ", database_name)

                    db.import_data_to_mongo(table_name, json_path, database_name)

            session['file_path'] = final_path
            
            #return render_template('index.html')
            return redirect(url_for('upload_success1'))

        
        #--------------------------------run query--------------------------------------
        elif request.form['action'] == 'run_query1':
            table_name = session['table_name']
            column_name = session['col_name']
            operator = session['operator']
            value = request.form['value']
            db_name = session['db_name']
            #print(table_name, column_name, operator, value, db_name)

            #get columns
            base_path = session['file_path']
            temp = table_name + "_meta.txt"
            path = base_path + '/' + temp
            cols = db.get_columns(path)

            # simple query ka code
            result = db.query_call_mongodb1(table_name, column_name, operator, value, db_name)

            #cols = ['Facility Name', 'Facility City', 'Facility State', 'Facility Type', 'Rating Overall', 'Rating Mortality', 'Rating Safety', 'Rating Readmission', 'Rating Experience', 'Rating Effectiveness', 'Rating Timeliness', 'Rating Imaging', 'Procedure Heart Attack Cost', 'Procedure Heart Attack Quality', 'Procedure Heart Attack Value', 'Procedure Heart Failure Cost', 'Procedure Heart Failure Quality', 'Procedure Heart Failure Value', 'Procedure Pneumonia Cost', 'Procedure Pneumonia Quality', 'Procedure Pneumonia Value', 'Procedure Hip Knee Cost', 'Procedure Hip Knee Quality', 'Procedure Hip Knee Value']
            #result = [{"Facility Name": "Southeast Alabama Medical Center", "Facility City": "Dothan", "Facility State": "AL", "Facility Type": "Government", "Rating Overall": 2, "Rating Mortality": "Below", "Rating Safety": "Above", "Rating Readmission": "Below", "Rating Experience": "Below", "Rating Effectiveness": "Same", "Rating Timeliness": "Above", "Rating Imaging": "Same", "Procedure Heart Attack Cost": 23394, "Procedure Heart Attack Quality": "Average", "Procedure Heart Attack Value": "Average", "Procedure Heart Failure Cost": 17041, "Procedure Heart Failure Quality": "Average", "Procedure Heart Failure Value": "Average", "Procedure Pneumonia Cost": 18281, "Procedure Pneumonia Quality": "Average", "Procedure Pneumonia Value": "Average", "Procedure Hip Knee Cost": 25812, "Procedure Hip Knee Quality": "Average", "Procedure Hip Knee Value": "Higher"}, {"Facility Name": "Flowers Hospital", "Facility City": "Dothan", "Facility State": "AL", "Facility Type": "Proprietary", "Rating Overall": 3, "Rating Mortality": "Below", "Rating Safety": "Above", "Rating Readmission": "Below", "Rating Experience": "Same", "Rating Effectiveness": "Same", "Rating Timeliness": "Above", "Rating Imaging": "Above", "Procedure Heart Attack Cost": 21779, "Procedure Heart Attack Quality": "Average", "Procedure Heart Attack Value": "Lower", "Procedure Heart Failure Cost": 16007, "Procedure Heart Failure Quality": "Worse", "Procedure Heart Failure Value": "Average", "Procedure Pneumonia Cost": 16796, "Procedure Pneumonia Quality": "Average", "Procedure Pneumonia Value": "Average", "Procedure Hip Knee Cost": 24056, "Procedure Hip Knee Quality": "Average", "Procedure Hip Knee Value": "Higher"}]
            session['result'] = result
            session['cols'] = cols

            if len(result) == 0:
                return redirect(url_for('no_op_simple'))

            return render_template("display.html", result = result, cols = cols)
        
        
    return render_template('index.html', flag = [1])







#-----------------------------------complex query------------------------------
@app.route('/complex_query', methods=["POST", "GET"])
def complex_query():

    if request.method == "POST":

        #print("hii")
        #-----------------------upload database---------------------
        if request.form['action1'] == 'go':
            #pass
            fle = request.files['choose2']
            #print(fle)

            file_name = fle.filename
            #print(file_name)

            fle.save(os.path.join(app.config["Files_upload"],fle.filename))

            path = app.config['Files_upload'] + "/" + file_name

            # unzip krne ka code
            home = app.config['Files_upload']
            
            path_to_zip_file=path
            with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
                zip_ref.extractall(home)
            
            f_path = file_name.split('.')[0]
            final_path = home + '/' + f_path
            #print(final_path)

            session['db_name'] = f_path

            result = [f for f in os.listdir(final_path) if os.path.isfile(os.path.join(final_path, f))]
            #print(result)

            for nm in result:
                if 'json' in nm:
                    #print(nm)
                    json_path = final_path + '/' + nm
                    table_name = nm.split('.')[0]
                    database_name = f_path
                    # print("The table name = ", table_name)
                    # print("The json path = ", json_path)
                    # print("The db name = ", database_name)

                    db.import_data_to_mongo(table_name, json_path, database_name)
            
            #return render_template('index.html', scroll="something")
            return redirect(url_for('upload_success2'))

        
        
        # ---------------------------------------run query 2--------------------------------------------
        elif request.form['action1'] == "run_query2":
            #print("Hello")
            query = request.form['field']
            cluster = session['db_name']
            
            result = db.complex_query_call_mongodb(query, cluster)
            print(result)
            #get columns 
            if result == -1:
                return redirect(url_for('incorrect_query'))
            try:
                temp = result[0]
                cols = temp.keys()
            except:
                return redirect(url_for('no_op'))

            

            #print(result)
            # cols = ['Facility Name', 'Facility City', 'Facility State', 'Facility Type', 'Rating Overall', 'Rating Mortality', 'Rating Safety', 'Rating Readmission', 'Rating Experience', 'Rating Effectiveness', 'Rating Timeliness', 'Rating Imaging', 'Procedure Heart Attack Cost', 'Procedure Heart Attack Quality', 'Procedure Heart Attack Value', 'Procedure Heart Failure Cost', 'Procedure Heart Failure Quality', 'Procedure Heart Failure Value', 'Procedure Pneumonia Cost', 'Procedure Pneumonia Quality', 'Procedure Pneumonia Value', 'Procedure Hip Knee Cost', 'Procedure Hip Knee Quality', 'Procedure Hip Knee Value']
            # result = [{"Facility Name": "Southeast Alabama Medical Center", "Facility City": "Dothan", "Facility State": "AL", "Facility Type": "Government", "Rating Overall": 2, "Rating Mortality": "Below", "Rating Safety": "Above", "Rating Readmission": "Below", "Rating Experience": "Below", "Rating Effectiveness": "Same", "Rating Timeliness": "Above", "Rating Imaging": "Same", "Procedure Heart Attack Cost": 23394, "Procedure Heart Attack Quality": "Average", "Procedure Heart Attack Value": "Average", "Procedure Heart Failure Cost": 17041, "Procedure Heart Failure Quality": "Average", "Procedure Heart Failure Value": "Average", "Procedure Pneumonia Cost": 18281, "Procedure Pneumonia Quality": "Average", "Procedure Pneumonia Value": "Average", "Procedure Hip Knee Cost": 25812, "Procedure Hip Knee Quality": "Average", "Procedure Hip Knee Value": "Higher"}, {"Facility Name": "Flowers Hospital", "Facility City": "Dothan", "Facility State": "AL", "Facility Type": "Proprietary", "Rating Overall": 3, "Rating Mortality": "Below", "Rating Safety": "Above", "Rating Readmission": "Below", "Rating Experience": "Same", "Rating Effectiveness": "Same", "Rating Timeliness": "Above", "Rating Imaging": "Above", "Procedure Heart Attack Cost": 21779, "Procedure Heart Attack Quality": "Average", "Procedure Heart Attack Value": "Lower", "Procedure Heart Failure Cost": 16007, "Procedure Heart Failure Quality": "Worse", "Procedure Heart Failure Value": "Average", "Procedure Pneumonia Cost": 16796, "Procedure Pneumonia Quality": "Average", "Procedure Pneumonia Value": "Average", "Procedure Hip Knee Cost": 24056, "Procedure Hip Knee Quality": "Average", "Procedure Hip Knee Value": "Higher"}]
            session['result'] = result
            #print("dfdahbadfb")
            return render_template("display.html", result = result, cols = cols)


    return render_template('index.html', flag = [2])



#--------------------------------------download json---------------------------------------
@app.route('/download_json', methods = ['POST', 'GET'])
def download_json():
    json_res = request.get_json()
    #print(json_res[0]['res'])
    temp = str(json_res[0]['res'])
    temp = temp.replace('&#39;','"')
    print(temp)
    result = json.loads(temp)
    print(result)
    db.convert_to_json(result)
    return "DOne"


#-----------------------------------------download csv-------------------------------------
@app.route('/download_csv', methods = ['POST', 'GET'])
def download_csv():
    json_res = request.get_json()
    #print(json_res[0]['res'])
    temp = str(json_res[0]['res'])
    temp = temp.replace('&#39;','"')
    print(temp)
    result = json.loads(temp)
    print(result)
    db.convert_to_csv(result)
    return "DOne"



#-------------------------------------------------display result-------------------------------------
@app.route('/display_result', methods=["POST", "GET"])
def display_result():

    if request.method == "POST":

        
        if request.form["action"] == "home":
            #pass
            return render_template("index.html", flag = [1])




#-------------------------------------main--------------------------------------
if __name__ =='__main__':  
    app.run(debug = True)
