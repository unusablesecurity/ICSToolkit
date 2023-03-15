#Author: Logan Gleason
#Hash Map class implementing LinkedList as underlying structure

from LinkedList import Node, LinkedList

class HashMap:
    
    def __init__(self, size):
        self.array_size = size
        self.array = [LinkedList for i in range(self.array_size)]

    def hash(self, key):
        hash_code = sum(key.encode())
        return hash_code
    
    def compress(self, hash_code):
        return hash_code % self.array_size
    
    def assign(self, key, value):
        array_index = self.compress(self.hash(key))
        payload = Node([key,value])
        list_at_array = self.array[array_index]

        for item in list_at_array:
            if key == item[0]:
                item[1] = value

        list_at_array.insert(payload)

    def retrieve(self, key):
        array_index = self.compress(self.hash(key))
        list_at_index = self.array[array_index]
        for item in list_at_index:
            if item[0] == key:
                return item[1]
            else: 
                return None
    
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