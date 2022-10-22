Chroma is a advance production ready ecommerce site built with ``Django`` with ``Esewa`` &amp; ``Khalti`` payment integration.


## Advance Features
* OTP verrification with ``Sparrow SMS API``
* Full Text search using ``PostgreSQL`` with search ranking
* Coupon code or discount box on a checkout page.
* Product Wishlists
* User reviews and rating after product purchase
* Multiple Options for Payments ``Esewa`` &amp; ``Khalti``
* Order Tracking to check the current order status 

## Quick Start

Clone this repository to your local machine and create a `.env` file and update the environment variables accordingly. Then you can start the project using Docker or manually using virtual environment.

Using Docker:

```
$ docker-compose up
$ docker-compose exec web python manage.py migrate
$ docker-compose exec web python manage.py createsuperuser
```

or, manually:

1. Create a Python virtual environment and activate it.
2. Open up your terminal and run the following command to install the packages used in this project.

```
$ pip install -r requirements.txt
```

3. Set up a Postgres database for the project.
4. Run the following commands to setup the database tables and create a superuser.

```
$ python manage.py migrate
$ python manage.py createsuperuser
```

5. Run the development server using:

```
$ python manage.py runserver
```
