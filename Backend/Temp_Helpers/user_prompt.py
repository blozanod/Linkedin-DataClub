# Script simulates what main.py (the script that recieves data from frontend) would send to helper scripts
# Gives command line prompts to allow custom filters/sort-by/select resume
# Additionally, contains example filters/sort-by for quick access

from Backend.Helper_Scripts.classes import Posting, Resume
import random
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session

# Database Filepaths
RESUME_DB = "../Databases/resumes.db"
POSTINGS_DB = "../Databases/postings.db"

# Prompts user for a set of filters & calls helper function
def getFilter():
    print("\n-- Construct Filter --")
    print("Enter filters in form: field operator value")
    print("Example: max_salary >= 150000")
    print("Type 'done' to finish.\n")

    filters = []

    # Valid operators that we support
    ops = {
        "=": lambda col, val: col == val,
        "==": lambda col, val: col == val,
        ">=": lambda col, val: col >= val,
        "<=": lambda col, val: col <= val,
        ">": lambda col, val: col > val,
        "<": lambda col, val: col < val,
        "like": lambda col, val: col.ilike(f"%{val}%"),
        "contains": lambda col, val: col.ilike(f"%{val}%"),
        "in": lambda col, val: col.in_(val.split(","))
    }

    # Allowed fields
    columns = Posting.__table__.columns.keys()

    while True:
        user = input("Filter: ")

        if user.lower() == "done":
            break

        # Parse the input
        parts = user.strip().split(" ", 2)
        if len(parts) != 3:
            print("Format must be: field operator value")
            continue

        field, operator, value = parts

        if field not in columns:
            print(f"Invalid field. Valid fields: {', '.join(columns)}")
            continue
        if operator not in ops:
            print(f"Invalid operator. Valid operators: {', '.join(ops.keys())}")
            continue

        # Convert value type based on column type
        col = getattr(Posting, field)
        python_type = col.type.python_type

        try:
            if operator == "in":
                # pass raw string list to "in" lambda
                pass
            else:
                value = python_type(value)
        except:
            # keep string value for like/contains
            pass

        # Build SQLAlchemy filter expression
        filt = ops[operator](col, value)
        filters.append(filt)

        print("Filter added.")

    return filters

# Prompts user for sorting params & calls helper function
def getSort():
    return 0

# Randomly selects resume & calls helper function
def getResume():
    engine = create_engine(f"sqlite:///{RESUME_DB}")
    session = Session(engine)

    try:
        ids = session.scalars(select(Resume.ID)).all()
        random_id = random.choice(ids)
        resume_obj = session.get(Resume, random_id)
        return resume_obj.Resume_str

    finally:
        session.close()

# Directs user to helper functions
def main():
    print("--Get Filter/Sort/Resume Helper Script--")
    print("Generates and returns a set of filters, sort instructions, or a resume")
    print("Usage: Enter 1 for filter, 2 for sort instructions, 3 for a resume")
    choice = -1
    while choice not in [1, 2, 3]:
        choice = int(input("Enter whether you want a filter, sort, or resume: "))
    {1:getFilter, 2:getSort, 3:getResume}[choice]()

main()