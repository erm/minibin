from minibin import db


if __name__ == "__main__":
    print("Creating database...")
    db.create_all()
    print("Success!")
