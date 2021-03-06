# Let's Translate
## About?
Built a simple Django infrastructure to implement two features on Rest Framework.

## Features -

- Email Validation
- Libre Translate - Translate from any language to English!

## Which Email Validation I used?

As stated in the assignment, I was given four choices - 
-        a. Trumail (Ruby)
-        b. Deep Email Validator
-        c. Checkmail (Golang)
-        d. ….any other you find

And I picked the fourth one and searched for a open source libbrary made in Python. The reason is simple, Trumail is made for Ruby, Deep Email Validator is made for Npm packages and lastly Checkmail is made in Golang. Since, we are using a python based framework, why not use as many libraries we can use from Python. So i researched and found out about **py3-validate-email** . 
Its key features are - 
- Format Check
- Blacklist Check (checks for disposable emails)
- Check DNS
- set  DNS timeout
- Check SMTP
- SMTP timeout set
- Set SMTP helo Host
- set SMTP from Address
- SMTP skip TLS
- SMTP TLS context

This has all the features the above libraries and can be easily implemented in Django. This library has an active community and their blacklist is constantly updated.
[Click Here For their Github Repo](https://github.com/karolyi/py3-validate-email)
[Click Here for Pypi Link](https://pypi.org/project/py3-validate-email/)

## How did I implement LibreTranslate? 

For LibreTranslate, I just pip installed into the virtual environment.

`pip install libretranslate`

If in any case the installation fails, use `apt-get install libicu-dev`

and then created an API key to put in our main project. the detect api in libretranslate isn't very accurate and gives most result with 0.0 confidence and en as default language. So,  I used a small python library langdetect with `pip install langdetect` to detect a language and then use normal translate api of libre to translate a text.

## Custom Permissions given to each user.

In this API, there are 4 users currently, the first user is superuser and there are three other users as mentioned in assignment. 

| username       | password           | token |
| ------------- |:-------------:| -----:|
| ekesel | myadmin123 | a4900e30d5259df39d74e775258ee962ab491f41 |
| user1 | myuser@123      |   8c9003121655a48bde14d953643bec85ec754d1f |
| user2 | myuser@123      |   2ca79c3cf2176ab34dad545eb12d9d63ebbfefa1 |
| user3 | myuser@123      |   8aa8df17660dd160fdd95c922f16e69508f2d12b |

## API End Product

The final end API product is on base Index URL only. It takes two parameters(form-data) in POST request.
The parameters are email and text and return the modified version of the input as mentioned in assignment.

### Token Based Authentication In API

I have implemented token based authentication in REST framework to easily identify users. If i wouldn't have used token based authentication, i would have to implement a login screen to login a user and then test api. the token is passed in Headers with Key `Authorization` and Value `Token <token> `. Tokens are automatically created when we add a user. It can be checked through the admin panel. 

## Check it out!

- Run the django server
- Run the libretranslate server alongside
- Check it out on POSTMAN!
- Use POST method and header {'Authorization':'Token <choose any token>'}
- form-data values - 1. email 2. text

## Requirements to Run the Project.

I have added the requirements txt file to run this project. Simply run `pip install -r requirements.txt`
The requirements are - 

- django
- djangorestframework
- langdetect
- libretranslate
- py3-validate-email
- django-environ

## Installation Steps!

- Clone the project
- run `pip install -r reuqirements.txt`
- then do `makemigrations` and `migrate`
- create a .env file in LetsTranslate folder. Add api key and django's secret key
- Open another Terminal and fire up libretranslate through `libretranslate`
- To generate a API key use command `ltmanage keys add 120`
- Simply use on postman

# Thank You!
