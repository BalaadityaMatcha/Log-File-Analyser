from flask import Flask, request, render_template, redirect, url_for, session, send_file
import subprocess, os, io, base64

resp = Flask(__name__)
resp.secret_key = "debba_debba"

@resp.route('/', methods=['GET', 'POST'])
@resp.route('/upload.html', methods=['GET', 'POST'])
def conv():
    if request.method == 'POST':
        file = request.files['drop']
        filepath = os.path.join('/tmp', file.filename)
        file.save(filepath)

        output = subprocess.run(["bash", "parse.sh", filepath], text=True, capture_output=True)
        out = output.stdout.strip()
        if out == "File not eligible for converting into csv":
            session['msg'] = "The file that you have provided is not eligible for converting into csv file!.<br>Please use apache log files only."
        elif out == "Empty file!":
            session['msg'] = "Empty file!<br>Cannot parse."
        else:
            x=["final.csv","userplot.png","sorted.csv","Orgsorted.csv"]
            for f in x:
                try:
                    if os.path.exists(f):
                        os.remove(f)
                except:
                    pass
            session['uploaded'] = 1
            session['msg'] = "Parsing succesful!<br>You can now visit the other pages to get your results."
        return redirect(url_for('conv'))

    if 'uploaded' not in session:
        session['uploaded'] = 0
    msg = session.pop('msg', '')
    return render_template('upload.html', msg=msg)


@resp.route('/logdisplay.html',methods=['GET', 'POST']) 
def table():
    if not session.get('uploaded'):
        return render_template('logdisplay.html', table_body="")
    dir = os.path.dirname(os.path.abspath(__file__))
    pathoffile = os.path.join(dir, "final.csv")
    if request.method == 'GET':
        if os.path.isfile(dir, "Orgsorted.csv"):
            subprocess.run(["bash", "filter.sh", pathoffile, "0", "0"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        table = subprocess.run(["bash","table.sh","Orgsorted.csv"],text=True,capture_output=True)
        return render_template('logdisplay.html',table_body=table.stdout.strip())
    else:
        date1 = request.form.get('start_time')
        date2 = request.form.get('end_time')
        output = subprocess.run(["bash", "filter.sh", pathoffile,date1,date2],text=True,capture_output=True)
        if output.stdout.strip() == "Done filtering":
            table = subprocess.run(["bash","table.sh"],text=True,capture_output=True)
            return render_template('logdisplay.html',table_body=table.stdout.strip())
        else:
            return render_template('logdisplay.html',table_body="")

@resp.route('/plots.html',methods=['GET','POST'])
def graphs():
    if not session.get('uploaded'):
        return render_template('plots.html',imgs="nah")
    
    from plots import g

    dir = os.path.dirname(os.path.abspath(__file__))
    pathoffile = os.path.join(dir, "final.csv")
    if request.method == 'GET':
        if not os.path.isfile("sorted.csv"):
            if not os.path.isfile("Orgsorted.csv"):
                subprocess.run(["bash", "filter.sh", pathoffile, "0", "0"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        img_data=g()
    else:
        date1 = request.form.get('start_time')
        date2 = request.form.get('end_time')
        output = subprocess.run(["bash", "filter.sh", pathoffile,date1,date2],text=True,capture_output=True)
        if output.stdout.strip() == "Done filtering":
            if os.stat("sorted.csv").st_size != 0:
                img_data=g()
            else:
                img_data="empty"
        else:
            img_data="nah"
    return render_template('plots.html',imgs=img_data)

@resp.route('/pyeditor.html',methods=['GET','POST'])
def editor():
    if not session.get('uploaded'):
        return render_template('pyeditor.html',visuals="nah")
    
    dir = os.path.dirname(os.path.abspath(__file__))
    pathoffile = os.path.join(dir, "final.csv")
    if request.method == 'GET':
        if not os.path.isfile("sorted.csv"):
            if not os.path.isfile("Orgsorted.csv"):
                subprocess.run(["bash", "filter.sh", pathoffile, "0", "0"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        instructions='''
##### Please make only one image at a time to get results. #####

# g_1st -> A dictionary instance with 'Timestamps' as keys
# g_2nd -> A dictionary instance with 'Levels' as keys
# g_3rd -> A dictionary instance with 'EventIDs' as keys
# All the values of the respective keys of the dictionaries are the no.of occurences of them.

# Use them wisely to get your plot ☺️ and do not change anything apart from "dpi".

# Write your code here(pyplot and numpy are already imported as plt and np respectively 🫠)

# End of input.
plt.tight_layout()
plt.savefig('userplot.png',dpi=300)
'''
        return render_template('pyeditor.html',instruction=instructions)
    else:
        code=request.form.get('pycode')
        snippet='''
import matplotlib,os
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
g_1st, g_2nd, g_3rd = {},{},{}
if os.path.isfile("sorted.csv"):
    file="sorted.csv"
else:
    file="Orgsorted.csv"
with open(file, "r") as f:
    global g_1st, g_2nd, g_3rd
    for line in f:
        loline=line.strip().split(",")
        g_1st[loline[0]] = g_1st.get(loline[0], 0) + 1
        g_2nd[loline[1]] = g_2nd.get(loline[1], 0) + 1
        g_3rd[loline[3]] = g_3rd.get(loline[3], 0) + 1
    g_3rd = dict(sorted(g_3rd.items(), key=lambda item: item[0]))                  
'''
        date1 = request.form.get('start_time')
        date2 = request.form.get('end_time')
        if date1 and date2:
            if code==None:
                output = subprocess.run(["bash", "filter.sh", pathoffile,date1,date2],text=True,capture_output=True)

        if code=='''
##### Please make only one image at a time to get results. #####

# g_1st -> A dictionary instance with 'Timestamps' as keys
# g_2nd -> A dictionary instance with 'Levels' as keys
# g_3rd -> A dictionary instance with 'EventIDs' as keys
# All the values of the respective keys of the dictionaries are the no.of occurences of them.

# Use them wisely to get your plot ☺️ and do not change anything apart from "dpi".

# Write your code here(pyplot and numpy are already imported as plt and np respectively 🫠)

# End of input.
plt.tight_layout()
plt.savefig('userplot.png',dpi=300)
''':
            msg="Please write your code first."
        else:
            with open("script.py", "w") as f:
                f.write(snippet)
            with open("script.py", "a") as f:
                f.write(code)
            try:
                output=subprocess.run(["python3","script.py"],capture_output=True,text=True,timeout=120)
                print(output.stderr)
                print(output.stdout)
                if output.returncode == 0:
                    msg="Success!"
                else:
                    msg="Error, code didn't run as expected."
            except subprocess.TimeoutExpired:
                msg="Error, Script timed out"
        return render_template('pyeditor.html', response=msg,instruction=code)
        

@resp.route('/download/<var>')
def download_file(var):
    if var=='csv':
        return send_file("sorted.csv",as_attachment=True)
    else:
        from plots import g
        img_data=g()
        if var=='1':
            return send_file(io.BytesIO(base64.b64decode(img_data[0])),as_attachment=True,download_name='events_time.png')
        elif var=='2':
            return send_file(io.BytesIO(base64.b64decode(img_data[1])),as_attachment=True,download_name='level_dstr.png')
        elif var=='3':
            return send_file(io.BytesIO(base64.b64decode(img_data[2])),as_attachment=True,download_name='eventcode_dstr.png')
        else:
            return send_file("userplot.png",as_attachment=True)
 
@resp.route('/userplot.png')
def userplot():
    return send_file('userplot.png', mimetype='image/png')

if __name__ == "__main__":
    resp.run(host="0.0.0.0",debug=True, use_reloader=False)