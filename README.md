FreeStore
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