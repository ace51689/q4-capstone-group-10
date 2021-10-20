# REDDIfy

A Reddit like site where users are able to create communities, have fun and share music.

#### **Your Task**

After cloning down the repository, start by running the poetry environment.
then run migrations using the command below to create the database.
>`python manage.py migrate`

Next you will run the command below to generate environment variables. (this is added to make site useful for grader while grading since they wouldn't have a .env file locally after cloning repo)
>`python manage.py generate_envfile`

Last but not least run command below to start server then enjoy site.
>`python manage.py runserver`