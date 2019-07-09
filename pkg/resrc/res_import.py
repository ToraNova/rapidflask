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
from collections import OrderedDict
import datetime
#-----------------and the forms--this as well!--------------------------------
from flask_admin.form.widgets import DatePickerWidget
from flask_wtf import FlaskForm
from flask_wtf import Form
from flask_wtf.file import FileField
from werkzeug import secure_filename
from wtforms import Field
from wtforms import StringField, PasswordField, BooleanField
from wtforms import SelectField, IntegerField, RadioField
from wtforms import SubmitField, SelectMultipleField
from wtforms import TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Email, Length, NumberRange
###############################################################################

from pkg.resrc.rstruct import rlin_nullk

from pkg.msgapi.proc import proctab_sel

boolchoice = [('1','True'),('0','False')]

#useful function for checking on null selections
def checkNull(list,colName):
    if(list.get(colName) == rlin_nullk):
        return None
    else:
        return list.get(colName)

class NonValidatingSelectField(SelectField):
    """
    Attempt to make an open ended select multiple
    field that can accept dynamic
    choices added by the browser.
    """
    def pre_validate(self, form): #Override the validation
        pass

class LenientDateTimeField(Field):
    """
    Attempt to allow the DateField to accept
    input from the datepicker widgets
    """

    def __init__(self, label=None, validators=None, formats=None, **kwargs):
        super(LenientDateTimeField, self).__init__(label, validators, **kwargs)
        if formats is None:
            self.formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%m/%d/%Y']
        else:
            self.formats = formats
        self.format = None

    def _value(self):
        if self.raw_data:
            return ' '.join(self.raw_data)
        else:
            return self.data and self.data.strftime(self.format) or ''

    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist)
            for fmt in self.formats:
                try:
                    self.data = datetime.datetime.strptime(date_str, fmt)
                    # If a datetime.date is required, do:
                    # datetime.datetime.strptime(date_str, fmt).date()
                    self.format = format
                except ValueError:
                    self.data = None
                else:
                    break
            if self.data is None:
                message = 'Value did not match any of these formats: {}'.format(', '.join(self.formats))
                raise ValueError(self.gettext(message))


