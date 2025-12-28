import os.path
import smtplib
import random
import string
import pandas as pd

CREDENTIAL_FILE = "credentials"
PARTICIPANTS_FILE = "participants.csv"

# -----------------------------
# PARTICIPANTS
# -----------------------------


def get_new_participant_info() -> list[tuple[str, str]]:
    num_participants = int(input("Enter the number of participants: "))
    participants = []

    for i in range(num_participants):
        name = input(f"Enter {i + 1}. participant's name: ").strip()
        email = input(f"Enter {i + 1}. participant's email: ").strip()

        if name.lower() in [p[0].lower() for p in participants]:
            print("Name already taken. Restarting selection.\n")
            return get_new_participant_info()

        if email.lower() in [p[1].lower() for p in participants]:
            print("Email already taken. Restarting selection.\n")
            return get_new_participant_info()

        participants.append((name, email))

    return participants


def get_participant_info() -> list:
    """
    Function to get all participant info.
    :return: Returns a list of pairs:
    (name, email)
    """

    # check whether old config exist, if yes, ask user if he wants to load it
    if os.path.isfile(PARTICIPANTS_FILE):
        yes_no = input("Would you like to read the current list of participants? (y/n) ")
        if yes_no == "y" or yes_no == "Y":
            df = pd.read_csv(PARTICIPANTS_FILE)
            participants = list(df.itertuples(index=False, name=None))
        else:
            participants = get_new_participant_info()
    else:
        participants = get_new_participant_info()

    # Print participants
    print(f"\nThere are {len(participants)} participants.")
    for p in participants:
        print(f"Name: {p[0]}, Email: {p[1]}")

    yes_no = input("Is this correct? (y/n) ")
    if yes_no == "y" or yes_no == "Y":
        data_frame = pd.DataFrame(participants, columns=["name", "email"])
        data_frame.to_csv(PARTICIPANTS_FILE, index=False)
        return participants
    else:
        return get_participant_info()


def assign_participants(participants) -> dict:
    """
    Assign each participant to a different participant.
    :param participants: list of pairs (name, email)
    :return: dict with key "name" and value being the assigned "name"
    """
    names = [p[0] for p in participants]
    assignments = {}

    # create a copy of all names
    shuffled_names = names[:]

    # shuffle all names and use that shuffled entity as baseline
    for i in range(50):
        random.shuffle(shuffled_names)

    for i, name in enumerate(shuffled_names):
        # get the index for the assigned name
        assigned_i = (i+1) % len(shuffled_names)

        # use the assigned_i index to fetch the to be assigned name from the shuffled names
        assigned_name = shuffled_names[assigned_i]

        # assign the assigned_name to the current name
        assignments[name] = assigned_name

    # return the final assignments
    return assignments


def assure_no_self_assignment(participants: list, assignments: dict) -> bool:
    """
    Checks whether all participants have a different assigned name than their own one.
    :param participants: list of pairs (name, email)
    :param assignments: dict with key "name" and value being the assigned "name"
    :return: True if the participants have a different assigned name, False otherwise
    """
    check = True

    names = [p[0] for p in participants]
    for name in names:
        if assignments[name] == name:
            check = False
            break

    return check


def remove_first_last_char(s):
    # Check if string is long enough to remove first and last characters
    if len(s) > 1:
        return s[1:-1]
    else:
        # If string length is 1 or less, return an empty string
        return ''


def send_emails(participants, assignments, year):
    # get credentials (email, password)
    with open(CREDENTIAL_FILE) as f:
        email, password = f.read().strip().splitlines()

    email = remove_first_last_char(email)
    password = remove_first_last_char(password)

    # send assignments over email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email, password)
        for name, participant_email in participants:
            assigned_name = assignments[name]
            message = f"Subject: Family Wichteln {year}\n\nHallo {name},\n\nDu hast einen Wichtel bekommen:\n--> {assigned_name}.\n\nViel Spass!"
            server.sendmail(email, participant_email, message)
            print(f"Email sent to {name} ({participant_email})")


def main():
    participants = get_participant_info()

    assignments = {}
    check = False
    limit = 50
    i = 0
    while not check and i < limit:
        assignments = assign_participants(participants)
        check = assure_no_self_assignment(participants, assignments)
        i += 1

    if i == limit:
        print(f"Could not assign participants to each other. Final assignment: {assignments}")
        print(f"Not sending E-Mails! Please rerun the application")
        return

    # assignment succeeded, so send emails
    year = input("Enter the year for the Secret-Santa event: ")
    send_emails(participants, assignments, year)


def generate_random_participants(n: int) -> list[tuple[str, str]]:
    participants = []
    used_names = set()
    used_emails = set()

    while len(participants) < n:
        name = ''.join(random.choices(string.ascii_letters, k=8))
        email = f"{name.lower()}@test.com"

        if name not in used_names and email not in used_emails:
            participants.append((name, email))
            used_names.add(name)
            used_emails.add(email)

    return participants


def test_assignment_process(iterations: int = 100, participants_count: int = 10):
    print("\nRunning assignment unit tests...")

    for iteration in range(iterations):
        participants = generate_random_participants(participants_count)
        assignments = assign_participants(participants)

        names = [p[0] for p in participants]

        # 1. Everyone has an assignment
        assert set(assignments.keys()) == set(names), \
            f"Iteration {iteration}: Missing assignments"

        # 2. No self-assignments
        for name in names:
            assert assignments[name] != name, \
                f"Iteration {iteration}: Self-assignment detected for {name}"

        # 3. Assigned person exists
        for assigned in assignments.values():
            assert assigned in names, \
                f"Iteration {iteration}: Assigned unknown participant {assigned}"

    print(f"All {iterations} assignment tests passed successfully!\n")


if __name__ == "__main__":
    test_assignment_process()
    main()
