from flask import request, render_template, redirect, url_for
from . import forms
import sqlalchemy as db
import pandas as pd
import pickle
from flask import current_app as app

filename = "D://Pyl//GitHubRepo//FlaskApp//FlaskApp//model//RandomForest.pkl"
model = pickle.load(open(filename, 'rb'))

@app.route('/', methods=["GET", "POST"])
def index():
    t_form = forms.TimeLineForm(csrf_enabled=False)
    if t_form.validate_on_submit():
        min_temp = t_form.Min_temp.data
        max_temp = t_form.Max_temp.data
        hf_lag = t_form.HF_lag.data
        wf_lag = t_form.Wf_lag.data
        ma_day = t_form.ma_day.data
        ma_mon = t_form.ma_mon.data
        return redirect(url_for("data", day=ma_day, mon=ma_mon, mtemp=min_temp, matemp=max_temp, h=hf_lag, w=wf_lag))
    return render_template('index.html', template_form=t_form)


@app.route('/data/<int:day>/<int:mon>/<float:mtemp>/<float:matemp>/<int:h>/<int:w>"', methods=["GET", "POST"])
def data(day, mon, mtemp, matemp, h, w):
    df = pd.DataFrame([[mtemp, matemp, h, w]], columns=['MAX_TEMP', 'MIN_TEMP', 'Holiday_Flag', 'Weekened_Flag'])
    pred = model.predict(df)
    engine = db.create_engine('sqlite:///C://Users//raman//master.db')
    connection = engine.connect()
    try:
        sql_query = pd.read_sql_query(
            "SELECT DEMAND, MAX_TEMP, MIN_TEMP, YEAR FROM data where DAY=(?) and MONTH=(?) and STATE='VIC'", engine,
            params=(day, mon))
        result = pd.DataFrame.to_html(sql_query)
        connection.close()
    except:
        result = "TRY AGAIN! DID YOU SELECT ALL THE OPTIONS. DO SELECT ALL THE OPTIONS"
    return render_template('data.html', template_res=result, template_pred=pred[0])


@app.route('/about', methods=["GET", "POST"])
def predict():
    return render_template('about.html')
