# course_proj_hse

## How to run parsers

Copy text below, clone this repository and paste in terminal in the directory where repository was cloned.

```env config
pip install virtualenv
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Then comment in /src/parsers/main.py functions that are not needed to be parsed
Then run /src/parsers/main.py

At the end you should get .json file(s) in the '/parsed' directory
