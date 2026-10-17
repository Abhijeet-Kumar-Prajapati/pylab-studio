import json, os

FILE = "contacts.json"

def load():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save(contacts):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)

def ask(prompt):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        raise SystemExit

if __name__ == "__main__":
    contacts = load()
    while True:
        print("\n1) List  2) Add  3) Search  4) Delete  0) Back")
        c = ask("Choice: ")
        if c == "0":
            break
        if c == "1":
            for ct in contacts:
                print(f"{ct['name']} - {ct['phone']} - {ct.get('email','')}")
            if not contacts:
                print("(no contacts)")
        elif c == "2":
            name = ask("Name: ")
            phone = ask("Phone: ")
            email = ask("Email: ")
            if name:
                contacts.append({"name": name, "phone": phone, "email": email})
                save(contacts)
                print("Added.")
        elif c == "3":
            q = ask("Search name: ").lower()
            for ct in contacts:
                if q in ct["name"].lower():
                    print(f"{ct['name']} - {ct['phone']} - {ct.get('email','')}")
        elif c == "4":
            name = ask("Name to delete: ").lower()
            before = len(contacts)
            contacts = [ct for ct in contacts if ct["name"].lower() != name]
            if len(contacts) < before:
                save(contacts)
                print("Deleted.")
            else:
                print("Not found.")
        else:
            print("Invalid.")