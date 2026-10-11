import json
import os
from datetime import date

FILE = "data.json"

def load_data():
    if not os.path.exists(FILE):
        return {"topics": [], "coding_problems": {"solved": 0, "log": []}, "internships": []}
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("data.json is corrupted. Starting fresh.")
        return {"topics": [], "coding_problems": {"solved": 0, "log": []}, "internships": []}

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_topic(data):
    name = input("Topic name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    if any(t["name"].lower() == name.lower() for t in data["topics"]):
        print("Topic already exists.")
        return
    data["topics"].append({"name": name, "status": "pending"})
    save_data(data)
    print("Topic added.")

def mark_topic_done(data):
    name = input("Topic to mark done: ").strip().lower()
    for t in data["topics"]:
        if t["name"].lower() == name:
            t["status"] = "done"
            save_data(data)
            print("Marked as done.")
            return
    print("Topic not found.")

def log_problems(data):
    try:
        count = int(input("Problems solved today: "))
    except ValueError:
        print("Enter a number.")
        return
    data["coding_problems"]["solved"] += count
    data["coding_problems"]["log"].append({"date": str(date.today()), "count": count})
    save_data(data)
    print("Progress saved.")

def add_internship(data):
    company = input("Company: ").strip()
    role = input("Role: ").strip()
    if not company or not role:
        print("Fields cannot be empty.")
        return
    data["internships"].append({"company": company, "role": role, "status": "applied"})
    save_data(data)
    print("Internship added.")

def view_progress(data):
    topics = data["topics"]
    done = sum(1 for t in topics if t["status"] == "done")
    print("\n--- Progress ---")
    print(f"Topics done: {done}/{len(topics)}")
    print(f"Problems solved: {data['coding_problems']['solved']}")
    print(f"Internship applications: {len(data['internships'])}")

def main():
    data = load_data()
    while True:
        print("\n1. Add topic\n2. Mark topic done\n3. Log problems\n4. Add internship\n5. View progress\n6. Exit")
        choice = input("Choose: ").strip()
        if choice == "1": add_topic(data)
        elif choice == "2": mark_topic_done(data)
        elif choice == "3": log_problems(data)
        elif choice == "4": add_internship(data)
        elif choice == "5": view_progress(data)
        elif choice == "6": break
        else: print("Invalid choice.")

main()