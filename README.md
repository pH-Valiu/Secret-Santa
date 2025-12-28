# Secret Santa (E-Mail)

A simple Python script that randomly assigns Secret-Santa partners and sends each participant their assignment via email.

Features:
* Stores participants in a CSV file
* Sends E-Mails automatically via Gmail
* Includes built-in unit tests to verify assignment correctness before execution

Currently, the E-Mail Text is in German. Adapt as wished (line _138_):
```python
message = f"Subject: Family Wichteln {year}\n\nHallo {name},\n\nDu hast einen Wichtel bekommen:\n-->{assigned_name}.\n\nViel Spass!"

```

## Requirements

* Python **3.9+**
* GMail account with **App Passwords** enabled

### Python dependencies

Install required packages using:

```bash
pip install pandas
```




## Credentials File (E-Mail account access)
For the Python script to be able to automatically send E-Mails via an GMail account, the account must have **App Passwords** enabled.

Create a `credentials` file parallel to the python script (see [Project Structure](#project-structure)) and add the following two lines. The information must be inside parenthesis:
* the GMail E-Mail 
* the App Password (this is different to the actual GMail account password)

Example file:
```
(your_email@gmail.com)
(your_app_password)
```


### How to create a Gmail App Password

1. Go to **Google Account -> Security**
2. Enable **2-Step Verification**
3. Use the search bar and search for **App Password**
4. Add a new entry:
   * App-Name: Secret-Santa-Mail
5. Copy the generated password into the `credentials` file

---

##  Project Structure

```
.
├── secret_santa.py       # main script
├── participants.csv      # auto-generated participants list
├── credentials           # email login (YOU must create this)
└── README.md
```

##  Participants

Participants consist of:

* **Name**
* **Email address**

### First run

* You will be prompted to enter all participants manually
* The list is saved automatically as `participants.csv`

### Subsequent runs

* You can reuse the saved participant list
* Or create a new one

Each participant:

* Must have a **unique name**
* Must have a **unique email address**

---

## How to Run

```bash
python secret_santa.py
```

---
## License
This project is provided as-is for personal use.
Use responsibly and never share credentials.
