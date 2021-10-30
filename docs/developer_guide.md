# Development installation
```{admonition} Note
You should have the following installed and properly configured:
- Python 3.8 or greater
- Pipenv
- Git
- Firefox
- Geckodriver
```
1. Clone the repo
1. Open your terminal/command-line and `cd` into the directory containing the repo
1. Create a `.env` file and add the following environment variables:
    - `DJANGO_EMAIL_HOST_USER`
    - `DJANGO_EMAIL_HOST_PASSWORD`
1. Create a virtual environment and install the **development** dependencies
    ```shell
    $ pipenv shell
    $ pipenv install --dev
    ```

1. Run the tests to check if everything is installed correctly
    ```shell
    # all tests
    $ python manage.py test

    # functional tests
    $ python manage.py test --tag=functional

    # non-functional (unit + integration) tests
    $ python manage.py test --exclude-tag=functional
    ```
