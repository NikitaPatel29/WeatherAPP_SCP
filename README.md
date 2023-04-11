## Flask Weather App

A simple web application to display the current weather in various cities using Python, Flask and sqllite3 database.

### 1. Installation and Setup Instructions

Clone this repository. You will need `python`, `virtualenv` installed on your machine.

### 2. Install [Pipenv](https://pipenv.pypa.io/en/latest/)

### 3. Create and activate the virtualenv

```bash
## run following command from current working directory
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
virtualenv myprojectenv
source myprojectenv/bin/activate
```

### 4. Install python packages

```bash
pip install -r requirements.txt
```

### 5. Run the database migration

`flask --app weather init-db`

### 6. To Start Server:

`flask run`