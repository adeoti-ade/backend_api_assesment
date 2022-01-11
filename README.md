# backend_api_assesment

# Installation

1. clone the application from this repository
2. make sure you have python installed on your computer. if not, download python for your machine
3. change directory to the application root
4. create a postgresql database with your choice for name, user and password
5. create a `.env` file in your root directory with similar parameter as found in the `env.example`
6. run the following command `pip install -r requirements.txt`
7. run the following to create the database schema `python manage.py migrate`
8. seed the database with data in `account.json` and `phone_number.json`. please run `account.json` first to avoid problems
9. run the application with the following command `python manage.py runserver`

#### Note: The error message structure was changed from the specified structure. Reason is that the error structure didn't consider the case where 
* There are multiple errors from one data field
* There are one/multiple errors from multiple data field

#### please find the deployed application at https://djangoassessmentapp.herokuapp.com/api/v1/

#### The following endpoins are available

1. Tokenization (`/token`)

    pass a username and auth_id as parameters to the endpoint to receive an access token.

2. Inbound Sms (`/inbound/sms`)

    pass a `_to`, `_from` and `_text` as body to this endpoint

3. Inbound Sms (`/outbound/sms`)

    pass a `_to`, `_from` and `_text` as body to this endpoint