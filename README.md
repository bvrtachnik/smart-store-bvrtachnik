# Project Setup

## Project Initialization

### Create a GitHub Repository
- Create a new repo on GitHub and add a default README.

### Clone the Repository
~~~shell
git clone [your-repo-url]
cd [cloned-repo]
~~~

### Add `.gitignore` and `requirements.txt` Files
- Add `.gitignore` and `requirements.txt` to the project.

### Create and Activate a Virtual Environment
~~~shell
python -m venv .venv
.\.venv\Scripts\Activate
~~~

### Upgrade Pip, Setuptools, and Wheel
~~~shell
py -m pip install --upgrade pip setuptools wheel
~~~

### Install Dependencies
~~~shell
pip install -r requirements.txt
~~~

### Track and Push Changes with Git
~~~shell
git add .
git commit -m "Initial commit"
git push origin main
~~~

### Run the Initial Project Script
~~~shell
py scripts/data_prep.py
~~~