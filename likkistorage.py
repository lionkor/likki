from tinydb import TinyDB, Query

class LGuild:
    name = None
    users = None
    db = None

    def new_db(self, members):
        for member in members:
            self.users[member] = 0;
        for k, v in self.users.items():
            self.db.insert({"name": k, "msgs": v})

    def load_db(self):
        for entry in self.db.all():
            self.users[entry["name"]] = entry["msgs"]

    def save_db(self):
        User = Query()
        for k, v in self.users.items():
            self.db.upsert({"name": k, "msgs": v}, User.name == k)

    def add_one(self, member: str):
        if member in self.users.keys():
            self.users[member] += 1
        else:
            self.users[member] = 1
        self.save_db()


    def __init__(self, name: str, members: list):
        self.name = name
        self.users = dict()

        self.db = TinyDB(name + ".json")
        if len(self.db) == 0:
            self.new_db(members)
        else:
            self.load_db()
        print(self.users)

    def __str__(self):
        printable = "```Guild: " + self.name + "\n"
        printable += "---\n"
        for name, msgs in self.users.items():
            printable += str(msgs) + "\t" + str(name) + "\n"
        printable += "```"
        return printable
