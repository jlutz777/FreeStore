# FreeStore

=========

This is a web application for Rocky River United Methodist's Twice Blessed Free Store in Cleveland, Ohio.  The code is meant to
be general enough that it can be re-used by other free stores in the future, although there are some areas that are specific
at the moment.

The code is primarily in Python and Bottle, with the database being Postgresql. It also uses RactiveJs and Bootstrap on the front end.
Reporting is done using d3.


The application has the following main actions available:
- Register customers and their dependents.
- Check in and check out customers.
- Check in and check out volunteers.

Admins additionally can:
- Create and edit users in the system, including admin versus user rights.
- Run reports for customers, dependents, visits, and more.
- Add shopping categories with item limits per user or per family and per week, month, or year.


## Upgrading the Database
SQLAlchemy is used throughout the server-side python code, and the database is created and updated through [alembic](https://alembic.sqlalchemy.org/).
Running the alembic commands on a database should give you all the tables and fields you need.

The basics are:
- `alembic upgrade head` to upgrade using the current scripts available
- `alembic revisions -m "whatever you are doing"`, followed by editing the py file generated to meet your needs