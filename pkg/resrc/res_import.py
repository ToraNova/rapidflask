#--------------------------------------------------
# res_import.py
# This file serves to reduce the code size of each res
# one can simply import this file and it imports the
# required modules for res model and form defines
# introduced in u3
# ToraNova
#--------------------------------------------------

#SAMPLE USAGE
# type the following in your resource file
# from pkg.resource import res_import as r
# then to use Column, it is just r.Column

###############################################################################
# STANDARD MODEL USAGE IMPORTS (COPY PASTA THIS!)-----------------------------
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float

from pkg.system.database import dbms
Base = dbms.deploy.base #re-export the deployment Base1 as Base

from pkg import limits as lim     #lim dependency
from pkg import const
from flask_login import current_user
import datetime,os
#-----------------and the forms--this as well!--------------------------------
from flask_admin.form.widgets import DatePickerWidget
from flask_wtf import FlaskForm
from flask_wtf import Form
from flask_wtf.file import FileField
from werkzeug import secure_filename
from wtforms import StringField, PasswordField, BooleanField
from wtforms import SelectField, IntegerField, RadioField
from wtforms import SubmitField, SelectMultipleField, DateField
from wtforms import TextAreaField
from wtforms.validators import InputRequired, Email, Length, NumberRange
###############################################################################

from pkg.resrc.rstruct import rlin_nullk

#useful function for checking on null selections
def checkNull(list,colName):
    if(list.get(colName) == rlin_nullk):
        return None
    else:
        return list.get(colName)

class NonValidatingSelectField(SelectField):
    """
    Attempt to make an open ended select multiple field that can accept dynamic
    choices added by the browser.
    """
    def pre_validate(self, form): #Override the validation
        pass
