activate_this = 'C:/Users/tinu4/documents/homework/Scripts/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
exec(open(activate_this).read(),dict(__file__=activate_this))

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('C:/Users/tinu4/documents/homework/Lib/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('C:/Users/tinu4/documents/homework/Homework-Manager')
sys.path.append('C:/Users/tinu4/documents/homework/Homework-Manager/homework_manager')

os.environ['DJANGO_SETTINGS_MODULE'] = 'homework_manager.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homework_manager.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
