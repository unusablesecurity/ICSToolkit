#Author: Logan Gleason
#Generate a list of randomized users and passwords, and store them in a hashtable

from HashMap import HashMap

def generate_passwords(users):
    usernames = []
    with open(users, 'r') as f:
        for line in f:
            usernames.append([line.strip(),"".join(reversed(line.strip()))])
    return usernames

def __main__():
    usernames = generate_passwords("Names.txt")
    password_map = HashMap(len(usernames))
    for item in usernames:
        password_map.assign(item[0], item[1])
    print(password_map)


if __name__ == "__main__":
    __main__()