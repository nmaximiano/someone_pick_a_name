def get_status_from_file(file_path= "people.txt"):
    try:
        with open(file_path, 'r') as f:
            content = f.read().strip()
            count = int(content)

        if 0 <= count <= 40:
            return "Not Busy"
        elif 41 <= count <= 80:
            return "Kinda Busy"
        else:
            return "Busy"

    except FileNotFoundError:
        return "Error: File not found."
    except ValueError:
        return "Error: Invalid number in file."


if __name__ == "__main__":
    status = get_status_from_file("people.txt")
    print("How Busy?:", status)
