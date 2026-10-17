import json, os

NOTES_FILE = "notes.json"

def load():
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)

def ask(prompt):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        raise SystemExit

if __name__ == "__main__":
    notes = load()
    while True:
        print("\n1) List notes  2) Add note  3) Delete note  0) Back")
        c = ask("Choice: ")
        if c == "0":
            break
        if c == "1":
            for i, n in enumerate(notes, 1):
                print(f"{i}. {n}")
            if not notes:
                print("(no notes)")
        elif c == "2":
            text = ask("Note: ")
            if text:
                notes.append(text)
                save(notes)
                print("Added.")
        elif c == "3":
            if not notes:
                print("No notes.")
                continue
            for i, n in enumerate(notes, 1):
                print(f"{i}. {n}")
            idx_s = ask("Delete number: ")
            if idx_s.lower() == "q":
                continue
            try:
                idx = int(idx_s) - 1
                if 0 <= idx < len(notes):
                    del notes[idx]
                    save(notes)
                    print("Deleted.")
                else:
                    print("Invalid.")
            except ValueError:
                print("Invalid.")
        else:
            print("Invalid.")