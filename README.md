# Group4 Team5
## End-user search queries on datasets (NoSQL)
### Team Members :
1. Somya Lalwani (2020201092)
2. Ayush Khasgiwala (2020201088)
3. Naman Jain (2020201080)

### Upload requirements
The upload requirements for input database for project is :
- `<database_name>.zip` file
- zip file containing `<tablename>.json` files and corresponding metafiles `<tablename>_meta.txt`

### How to run?
`python3 app.py`

### Overview
- Quierra is a fast and simple Browser tool to query our NoSQL data by uploading your JSON file on our website.
- The output will be provided to the user in multiple formats, such as via HTML page, CSV/JSON format.

### Tech-Stack Used
- Developed responsive website with the help of HTML, CSS, JavaScript, Ajax
- Connected front end i.e. the web pages, with backend where the query processing is done using Flask web framework
- For executing the queries, we have used MongoDB (a NoSQL database).

### Design

* Front-end of the application:
    * The user will be provided with 2 interfaces: the simple query UI & the complex query UI.
    * In simple query UI : User will be given drop down menus which will change according to the previous choice. This will be a simplified interface version of simple queries. 
    * The complex query UI will directly provide the query and the output will be provided. 
* Back-end of the application: Different databases containing different tables will be provided as input to the application. The queries provided by the user will be processed (in real-time)in the backend on the dataset provided. Then the filtered data from the query i.e., the output will be displayed to the user. 

* Input format of the database is a zip file with name as 'databasename>.zip'. The zip files contains multiple files <table_name>.json files, and each such file will have a corresponding metadata file.
* Output of the query can be provided in 3 formats - displaying on the page itself, CSV file (download option provided), JSON file (download option provided)


### Steps to run Simple Query Page
* Upload the database zip file first.
* At first Table name is selected from the drop-down, accordingly the column names come. Next 3 values to be selected for the query on the table are : Column name, options like >,<, =, etc. and the last a text-field for input value.
* On clicking ‘Run Query’, the query will be executed and page will be redirected to result page.

### Steps to run Complex Query Page
* Upload the database zip file first.
* We can enter the query that we want to run in the black textbox.
* On clicking ‘Run Query’, the query will be executed and page will be redirected to result page.

