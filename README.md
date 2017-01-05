## Overview

Growth Street is building a platform to allow growing businesses to borrow money at affordable rates. Our ability to make the entire process efficient on our web platform will be critical in offering the lowest rates to our customers. 

#### The Task

Build a Django app for borrowers to register and request a loan. You will need to collect the following information:

* The borrower's name, email, and telephone number.
* The borrower's business' name, address, registered company number (8 digit number), and business sector (pick from Retail, Professional Services, Food & Drink, or Entertainment).
* The amount the borrower wishes to borrow in GBP (between £10000 and £100000), for how long (number of days), and a reason for the loan (text description).
* This information should be stored in the database via appropriate models, and accessible to an admin in the standard Django Admin tool.

#### Notes

You are encouraged to use 3rd party libraries and the built-in framework tools when it makes sense (for example "django-registration-redux" or "django-allauth" to help handle registering a new user)
While the final product should have an interface via a web browser, there is no need for styles or anything beyond functional HTML

#### Delivery

Fork this repository, make your additions, and then submit a pull request with your submission. If you haven't previously, please contact us with your CV at jobs@growthstreet.co.uk as well.

#### My (Rollo's) Solution

This is a rather simple task, but I wanted to brush up on some new features
within Django.

This submission uses Django-AllAuth for the accounts. Twillo for Mobile Phone
verification, combined with a Celery queue and Django channels to communicate
progress with the user.  The Companies House API is used for the fetching of 
additional company data.

Apologies for the lack of tests, I was a bit strapped for time coming back from
Ireland.

To deploy

```
$ docker-compose run web python manage.py migrate
$ docker-compose run web python manage.py loaddata growthstreet/fixtures/initial_data.json
$ docker-compose up -d
```

Navigate to lvh.me:8000
