from flask import Flask, request, render_template
from src import email_flask_db
import requests
import app_config
from src.EmailHandler import EmailHandler



app =  Flask(__name__)

app.config.from_object(app_config.ProductionConfig)

email_handler = EmailHandler()




@app.route('/', methods=['GET','POST'])
def test_send_email():
    if request.method == 'POST':
        msg_unicode = request.get_json()
   
        response = email_handler.send_message(msg_unicode)
        if type(response) is requests.Response:    
            response = response.text
            email_flask_db.insert(app.config['DATABASE_URI'], msg_unicode, response)
        return response
        
    return render_template('email_form.html')


if __name__ == "__main__":
    app.run()
