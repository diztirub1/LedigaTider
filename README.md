# LedigaTider
Sends you an email if there is an available time in either March or April to get a new passport or ID-card in Sweden.
The email will also have an attachment with a screenshot of the timetable.

Example attachment:

<img src="lediga_tider.png" width="350" height="300">

# Installation
Create a file named .env
```
# environment variables
MY_EMAILS=mail@sending.from
PASSWORDS=MY_EMAILS_password123
MOTTAGARES=["mail@sending.to","mail2@sending.to"]
```
