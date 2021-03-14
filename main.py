from flask import Flask,render_template,request
from Steam import steam
from Bitskins import bitskins
from Skinport import skinport
import json
import concurrent.futures

app = Flask(__name__)



@app.route("/")
def search():
    return render_template("home.html")

@app.route("/search",methods=['GET','POST'])
def home():
    if request.method == 'POST':
        input_name = request.form.get("skin_name")
        print(f"skin name {input_name}")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            f1 = executor.submit(steam,name=input_name)
            f2 = executor.submit(bitskins,name=input_name)
            f3 = executor.submit(skinport,name=input_name)
            res1 = json.loads(f1.result())
            res2 = json.loads(f2.result())
            res3 = json.loads(f3.result())
            print(res3)
            temp = [res1,res2,res3]
            out = []
            for d in range(len(temp)):
                out.append([temp[d]['source']])
                for k,v in temp[d]['conditions'].items():
                    out[d].append((v['price'],))


            print(out)
    return render_template("search.html",data = out)
    



if __name__ == '__main__':
    app.run(debug=True)
    