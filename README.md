## To Do:
###### Social Authentication
  - Put my version of social_django in its own repo and add that to requirements.txt 
  - fix username on recurse authentication
  - set up two authentication apps for github, one for local and one for prod

###### Environments
  - remove .env from repo (all the way, meaning delete repo and rebuild it)
  - set environment variables in heroku
  - only call load_dotenv once, in settings.py

###### Automated Email
  - find out why three are being sent instead of just 1...

###### Security
  - Add CSP... see django-csp