from waitress import serve
from fxyoutube import app

serve(app, listen='*:1111')
