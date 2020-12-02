from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired


class TimeLineForm(FlaskForm):
    Day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
           20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
    Months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    Holiday_flag = [0, 1]
    Weekend_flag = [0, 1]
    Min_temp = StringField("Minimum Temp", validators=[DataRequired()])
    Max_temp = StringField("Maximum Temp", validators=[DataRequired()])
    HF_lag = RadioField("Holiday_Flag", choices=Holiday_flag, validators=[DataRequired()])
    Wf_lag = RadioField("Weekend_Flag", choices=Weekend_flag, validators=[DataRequired()])
    ma_day = SelectField("Day", choices=[(f, f) for f in Day])
    ma_mon = SelectField("Month", choices=[(f, f) for f in Months])
    submit = SubmitField("Predict")
