Abstract

This email service implements the following Functionality:
Tttp round trip between both client and email service provider
Validate input data including html validation
Dynamically select provider based on response from the provider.
Use lightweight query-able storage to keep records of emails passing through the service
It is deployed at HeroKu and can be accessed via a simple test ui:
http://obscure-springs-9663.herokuapp.com/
This is also the url which accepts http json post.
Framework

This project is developed using Flask micro web framework.  The reason to choose Flask is first, because it is python which has a good community. And second, it is really easy to learn and is good at developing small web application within limited time. In Flask, every application is a single process and a web server can have several processes running the same application code. Such design is not good for complicated web service but makes small web service easy to develop.

Functionality and Internal Flow

1.	This email service receives email sending request from client with json data
2.	It validates data and immediately returns bad response to client if data fails validation  
3.	It finds one service providers on its list, converts the data to a format that is accepted this provider, and then sends the request to that provider. If it gets bad response from the service provider, a request timeout, it will turn to the next provider on its provider list to try to post the data again. 
4.	It will not stop until it either sends the data successfully or goes through all the providers but cannot get the data sent. 
5.	It sends a http response to notify client about the result.


Service provider

3 files handle the interaction with services providers. An abstract class, EmailService.py defines apis that all providers need to have.  It has two subclasses MailGunEmailServiceHttp and MandrillEmailServiceHttp. Each implements the apis.  
Engine
Email_Handler is the service engine. It is created before service starts to accept request. When it is created, it finds all the providers from a config file and put them in a list.  So every provider has to have one configuration entry in the config file in order to register. When engine reads the config file at the run time, it dynamically imports each provider’s api class. Such design pattern makes adding new service provider without changing the existing code.  Adding new provider only has 3 requirements.  First, new class needs to inherit abstract service class. Second, add an entry in the config file for new class needs. And the last, new class needs to be placed in the same directory where all other existing service apis sit so engine knows where to import it.
When concrete provider class object is initialized, it will ping its provider to check its configuration.  If it finds some error which is not self recoverable, for example, the service url is wrong or api_key is not correct.  It will not be placed into the provider list.
Email_Handler is also designed to be stateless and singleton in the application. This ensures each request can call it without a lock.  
Default service provider can be specified in the config file so that engine will always try default provider first. 
 
Whenever a request arrives, engine tries to send the request to providers and stops if either sending is successful or it goes through the list and finds no provider accepts the request. 

Validation

Data validation is implemented in email_message.py not in service providers’ api. Because data validations are the same for all the providers. So it should be done by service broker, which is our service. Engine performs validation before calling providers api.  Here is the validation detail on each input form. 
Email validation uses regular expression.  The actual expression imitates Django email check. One decision here is not using other web service to check email address.  Because often one email can have a huge recipient list, including to, cc, bcc.  If everyone email address needs a http round trip to validate, performance can be really bad.  Also using webhook to get delivery feedback is a better solution.
Name and subject validation only check if payload is printable text. 
Body validation uses a html validation. Because both MailGun and Mandrill support plain text body and html body in the same request.  So for every request data, a plain text is always included. A html body will be included if it passes the html validation.  A python package called py_w3c is used to validate html. It actually calls w3c html validation service to do the work.  A little story about this python package is that because it is not officially distributed, Heroku is not able to download it during the git push. It’s a Heroku known issue. The final workaround is to include this package in my project as source code and add its path to sys.path. That explains the py_w3c directory. 

Input Data Form

Input data form is exactly the same as described in the specification. It accepts:
To : recipient’s email address
To_name: recipient’s name
From:  sender’s email
From_name: sender’s name:
Subject: email title
Body: html body of email
This service processes all the string data as Unicode. This is because python json module by default transfers json data to python built-in dictionary holding Unicode string. So treating all string data as Unicode avoids extra data type conversion.
Due to the time limitation, currently input data doesn’t accept multiple recipients and multiple receiving type. Also no attachment is supported. All of them can be further developed. 

Database and Log

This application has a lightweight sqlite3 db. This db file is under db directory. A db_shema.py can be also found in the same directory. You need to run the script once to generate the db file and create table. 
So far there are two tables:
Table: email(id integer primary key, from_address text, from_name text, subject text, body text, state text, time text);
Table: recipient_email (email_id integer, to_address text, to_name text, to_type text, time text);
  
First table is the email table. Id is the primary key. The second table stores all the recipients of one email The primary key for recipient_email table is email_id and to_address. As you can see two tables are one-to-many relationship. Email Id value is generated using sqlite3 auto-increment integer in the email table. Then it gets passed to recipient email table.  Current Schema mainly supports data logging.  The logging happens whenever application gets a http response from providers. In addition to the input data, the response message is stored to state column in email table.  Db schema can be further developed to support attachments. 
Configuration

Configuration file is in the src/emailservice directory, named config.py. It is a list of python dict type keeping the configuration for service provider. Each configuration dict follows the naming standard <class_name>_config.  Engine uses this name to find the corresponding class.

Testing

All the testing code is in test directory. Every <name>.py has a related test_<name>.py test. Every test files are self-runable. You can run test_all.py to run all of tests. 
A testing ui page is also provided in templates which shares the same url of the service. It uses Jquery to change the behavior of submit button and renders response on the bottom of the response.
Things to remember before test: There are several config files in the test config directory, populate any field marked as “?” with your personal settings before you run the test.
  
Installation

This service is deployed at http://obscure-springs-9663.herokuapp.com/
The deployment steps is here https://devcenter.heroku.com/articles/getting-started-with-python#visit-your-application
Things to remember before deployment:
Open config.py in src/emailservice directory, populate any field marked as “?” with your personal settings before you run the test.
Run db_schema.py in db directory to generate email_flask.db file.


You reach the end of the document. I am glad you read it all. Thank you for your time.

Alex
