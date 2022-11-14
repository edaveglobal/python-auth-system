# Gathpay Auth System Backend


### Local Setup

- Clone the repository with `git@github.com:gathpay/auth-system.git`
- Navigate to `auth-system` dir and activate virtual environment based on your os using command below
- Run `python3 -m venv venv` Then activate the environment
- If windows? Run `source venv/Scripts/activate`
- If Mac/Linux Run `source venv/bin/activate`.
- Run `pip install -r ./auth_system/requirements.dev.txt` for installing requirements.
- Run `python manage.py ./auth_system/migrate` to migrate model to db.
- Run `pytest` for tests.
- Lastly, Run `python ./auth_system/manage.py runserver` to spin up server locally.


#### Do not hesitate to reach out by creatung an issue if there is any problem.

### Happy Coding
