<p align="center"><h1>Chiron - Online Doctor's office platform</h1></p>


<p align="center">
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<br>
<small>Software Engineering Course project - Fall 2021</small>
</p>


## Dev run
In a `python3.9+` envioronment, do as follows:
```bash
pip install -r requirements.txt
python manage.py makemigrations users
python manage.py migrate
python manage.py runserver
```

## Contribute
This codebase uses the [black](https://github.com/psf/black) formatter.
It will automatically format your code, such that the whole codebase stay consistent.
Install [pre-commit](https://pre-commit.com/) with `pip install pre-commit` and then in this repository folder run `pre-commit install`.
Your code will be formatted before you commit and push.
