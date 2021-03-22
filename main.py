from flask import Flask,render_template,request
from Steam import steam
from Bitskins import bitskins
from Skinport_new import skinport
import json
import concurrent.futures
import mysql.connector


app = Flask(__name__)


config = {
  'user': 'root',
  'password': 'prajwal1234',
  'host': '127.0.0.1',
  'database': 'newdb',
  'raise_on_warnings': True
}

cursor = None
cnx = None

try:
  cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

  


@app.route("/")
def search():
    return render_template("home.html")


@app.route("/fetchsuggestions",methods=['GET','POST'])
def sugg_res():
    global cursor
    cursor = cnx.cursor()
    requested_name = request.get_json()['skin_name']
    if requested_name:  #perform checks
      query = "(select name from awp where name like %s limit 6)"
      cursor.execute(query,(requested_name,))
      
      return render_template("suggestions.html",data=cursor)
    return "useless"



@app.route("/search",methods=['GET','POST'])
def home():
    out = []
    if request.method == 'POST':
        input_name = request.form.get("skin_name")
        print(f"skin name {input_name}")
        futures = []
        temp = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for f in [steam,bitskins,skinport]:
                f = executor.submit(f,name=input_name)
                futures.append(f)
            for future in concurrent.futures.as_completed(futures):
                temp.append(json.loads(future.result()))
            for d in range(len(temp)):
                out.append([temp[d]['source']])
                for k,v in temp[d]['conditions'].items():
                    out[d].append((v['price'],))


            print(out)
    return render_template("search.html",data = out)
    



if __name__ == '__main__':
    app.run(debug=True)
    