<!-- SAC Election Portal - DBMS Project submitted by Group 17 (Abhinav, Faseem, Hadif, Hanna, Harimurali) -->
# [SAC Election Portal](https://github.com/heckerfr0d/SACelection)

## About

An intuitive web application to conduct the SAC elections securely.
Hosted at [sac-election.herokuapp.com](https://sac-election.herokuapp.com).

## Running locally

1. Clone the [repository](https://github.com/heckerfr0d/SACelection)

    ```console
    git clone https://github.com/heckerfr0d/SACelection.git
    ```

2. Resolve system dependencies (platform-specific)

   1. [Python](https://www.python.org/downloads)
   2. [PostgreSQL](https://www.postgresql.org/download/)

3. Create a python virtual environment

    ```console
    python3 -m venv path/to/virtualenv
    source path/to/virtualenv/bin/activate
    ```

4. Resolve python dependencies

    ```console
    pip install -r requirements.txt
    ```

5. Set up the local database (Assuming you have postgres service running locally)

    ```console
    createdb test
    psql -U username -d test -a -f testdb.sql
    ```

6. Run the application

    ```console
    python3 wsgi.py     // flask development server or
    gunicorn wsgi:app   // gunicorn production server
    ```

7. Open the browser and navigate to [localhost](http://localhost:5000/) to access the application.
8. Refer user manual for further instructions :p

## Contributors

- [Abhinav Ajithkumar](https://github.com/abhinav-ajith)
- [Faseem Shanavas](https://github.com/faseem619)
- [Hadif Yassin Hameed](https://github.com/heckerfr0d)
- [Hanna Nechikkadan](https://github.com/hanna13n)
- [Harimurali J](https://github.com/randomdeveloper7)
