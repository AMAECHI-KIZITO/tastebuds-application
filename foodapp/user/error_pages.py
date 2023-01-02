""""Error pages"""
from flask import render_template
from . import userobj
from foodapp.models import *


## 404 Error
@userobj.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html',error=error),404

## 500 Error
@userobj.app_errorhandler(500)
def internal_server_error(error):
    return render_template('500.html',error=error),500