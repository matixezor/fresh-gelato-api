# Fresh Gelato API
API created with Django Rest Framework with JWT authentication
## Table of contents
1. [Introduction](#introduction)
1. [Installation](#installation)
1. [API Endpoints](#api-endpoints)
1. [Tests](#tests)
## Introduction
This simple API was created to serve gelato recipes. You can add recipes and ingredients.
The authentication is done via JWT token.
There is an endpoint to allow customers to contact the company via mail.
I wanted to learn DRF and this is the result. There's still some room to improve it 
and it will be done soon.
## Installation
Use ` $ pip install -r requirements.txt ` to install all the required packages. <br/>
Use ` python manage.py makemigrations ` and ` python manage.py migrate ` to setup your database. <br/>
Use ` python manage.py createsuper ` to create your admin account. <br/>
Use ` python manage.py runserver ` to run the server locally. 
## API endpoints
* api/token-auth/ 
  * Methods: 
    * POST
  * Authorization: 
    * POST: Allow any
  * Description: Send login credentials to receive token and user info 
  * Query: 
```javascript 
  { "username": string, "password": string } 
```
  * Response: 200 
 ```javascript
{
    "token": string,
    "user": {
        "username": string,
        "first_name": string,
        "last_name": string,
        "email": string
    }
}
```
* api/recipes/ 
  * Methods: 
    * GET    
    * POST
  * Authorization: 
    * GET: Authenticated only 
    * POST: Staff only 
  * Description: Get all recipes or Create new recipe 
  * Query: 
```javascript
{
  "name": string,
  "image": string, #not required
  "base_amount": int,
  "ingredients": [
    {
      "name": string,
      "price": int,
      "percentage": int
    },
    {
      "name": string,
      "price": int,
      "percentage": int
    }
  ]
}
``` 
  * Response: 
    * POST Code: 201 or 400 if Bad Request 
    * If unauthorized: 401
    * GET Code: 200 
```javascript 
[{
        "id": int,
        "name": string,
        "image": null or string
    }, {
        "id": int,
        "name": string,
        "image": null or string
    },
    ...
}]
``` 
* /api/recipes/{id} 
  * Methods:
    * GET
  * Authorization:
    * GET: Authenticated only
  * Description: Get specified recipe 
  * Response: 
    * If unauthorized: 401
    * GET Code: 200 or 404 if not found
```javascript
{
    "id": int,
    "name": string,
    "base_amount": int,
    "total_price": float,
    "image": string or null,
    "ingredient_count": int,
    "ingredients": [{
            "name": string,
            "amount": int,
            "price": float,
            "cost": float,
            "percentage": float
        },
        ...
    ],
}
```
* /api/send-email/ 
  * Methods: POST 
  * Authorization: 
    * POST: Allow any 
  * Description: Post email to contact the company 
  * Query:
```javascript
{
    "sender_name": string,
    "sender_mail": string,
    "content": string
}
```
  * Response:
    * POST Code: 201 or 400 if bad request
* /api/user/
  * Methods:
    * GET
    * POST
  * Authorization:
    * GET: Authenticated only
    * POST: Allow any
  * Description: Get authenticated user info or Create new user
  * Query:
```javascript
{
  "username": string,
  "password": string,
  "first_name": string,	#not required
  "last_name": string,	#not required
  "email": string	#not required
}
```
  * Response:
    * POST Code: 201 or 400 if bad request
    * If unauthorized: 401
    * GET Code: 200
```javascript
{
    "username": string,
    "first_name": string,
    "last_name": string,
    "email": string
}
```
## Tests
There's some basic unit tests. <br/>
To run them use: ` python manage.py test `
