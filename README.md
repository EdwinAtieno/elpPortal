## Table of Contents

- [Requirements](#requirements)
- [Local Development](#local-development)
  - [Env Setup](#env-setup)
    - [Environment Variables](#environment-variables)
  - [Project Setup](#project-setup)
    - [Manual Setup](#manual-setup)
  - [Running the app](#running-the-app)

## Requirements

- [Python](https://www.python.org/downloads/) >= 3.10
- [pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today)

## Local Development

### Env Setup
1. Clone the repository:\
    a. Using SSH:

   ```
   git clone git@github.com:EdwinAtieno/elpPortal.git
   ```

   b. Using Http:

   ```
   git clone https://github.com/EdwinAtieno/elpPortal.git
   ```

2. Navigate to the cloned folder:

   ```
   cd elpPortal
   ```

3. In order to create a virtual environment, run:

   ```
   pipenv shell
   ```

   - It will also create Pipfile and Pipfile.lock for package requirements.

4. So as to install the packages in your environment, run:

   ```
   pipenv install
   ```

   - In order to install all packages(including dev packages), run:
     ```
     pipenv install --dev
     ```

5. To install the pre-commit git hooks, run:

   ```
   pre-commit install
   ```

6. Create a .env file
   ```
   touch .env
   ```
   - Add the following environment variables in your `.env` file

#### Environment Variables

| Variable                        | Description                                                                                                                                                                                                                                                                          | Default          |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------- |
| <sup>**SECRET_KEY**</sup>       | <sup>**Required** - String of random characters used to provide cryptographic signing for [Django](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SECRET_KEY) projects.</sup>                                                                                       | <sup></sup>      |
| <sup>**DATABASE_URL**</sup>     | <sup>**Required** - Used by [dj_database_url](https://github.com/kennethreitz/dj-database-url#url-schema) to connect to the database.<br /> Format: postgresql://\<user\>:\<password\>@\<host\>:\<port\>/\<db\>. <br/>If using docker, put the host as: `host.docker.internal`</sup> | <sup></sup>      |
| <sup>**ENVIRONMENT**</sup>      | <sup> **Optional** - Used to load different settings according to the environment selected. Choices: `production`, `staging`, `local`</sup>                                                                                                                                          | <sup>local</sup> |


\
#### Manual Setup

- Create a database and add its url to your project environment. eg <br/>
  `DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<db>`

- Create and activate a virtual environment - we recommend using [pipenv](https://github.com/pypa/pipenv) for this by running:
  ```
  pipenv shell
  ```
- Install the project dependencies stored in [Pipfile](/Pipfile). Run:
  ```
  pipenv install --dev
  ```
- Run migrations:
  ```
  python manage.py migrate
  ```

### Running the app

- To run tests:

  ```
  pytest
  ```

* Run the app:

  ```
  python manage.py runserver
  ```

* You can now use the app locally using the URL: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
