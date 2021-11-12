
# Send SMS with React and Twilio: A Basic Web interface

This is an example of sending SMS using React and Twilio. It consists of a Form component that communicates with a flask server endpoint to [send SMS messages via the Twilio REST API](https://www.twilio.com/docs/sms/send-messages).


## Running the project

To run the project you will need a Twilio account and a Twilio phone number that can send SMS messages. Gather your Twilio Account Sid and Auth Token from the [Twilio console](https://www.twilio.com/console) and the phone number.

Then, clone the project, change into the directory and install the dependencies.


### Pre-Req
- Have Python 3.6.3+
- Have Docker Installed
- 

```bash
git clone git@github.com:davidfu92/basic_chat.git
cd basic_chat
make init
```

Export your Credentials to ENV_VARS on your machine 

```bash
   export TWILIO_ACCOUNT_SID=*****
   export TWILIO_AUTH_TOKEN=*****
   export TWILIO_API_KEY_SID=*****
   export TWILIO_API_KEY_SECRET=*****
```

Start the local Mongo database within a self contain Docker:

```bash
make run-db
```

Start the local back-end application on its own with the command:

```bash
make run-flask
```

Start the local front-end application on its own with the command:

```bash
make run-react
```

To containerize all three pieces of the application

```bash
make docker
```

Open the app at [localhost:3000](http://localhost:8080). You can now use the form to send SMS messages via your Twilio number.