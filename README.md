# course_proj_hse

## How to run parsers

Copy text below, clone this repository and paste in terminal in the directory where repository was cloned.

```bash
pip install virtualenv
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Then comment in /src/parsers/main.py functions that are not needed to be parsed
Then run /src/parsers/main.py

At the end you should get .json file(s) in the '/parsed' directory

## How to run docker locally

Do everything in main project directory, where you clone this repo

1. Check if docker is installed on your computer

    ```bash
    docker --version
    ```

2. If docker is not installed (for MacOS)

    2.1. Install homebrew (if needed)

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

    2.2 Install docker app

    ```bash
    brew install --cask docker
    open /Applications/Docker.app
    ```

    2.3 Check needed libraries

    ```bash
    docker --version
    docker-compose --version
    ```

3. Add .env file to main proj directory

4. Build and run Docker db

    ```bash
    docker-compose -f docker-compose.yaml up db -d --build
    ```

    This should make a container in Docker desktop and run db image

5. Run /parsing/src/main.py
6. Run /parsing/src/parsers/db_fill.py
7. Finally build web image and run it

    ```bash
    docker-compose -f docker-compose.yaml up web -d --build
    ```

Now local webpage should be accessed at [this link](http://localhost:8000)
