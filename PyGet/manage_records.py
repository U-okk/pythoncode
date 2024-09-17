import json
import datetime

# Function to create an alias by reversing the name
def create_alias(name):
    return name[::-1]

# Function to calculate age from birthday
def calculate_age(birthday):
    today = datetime.date.today()
    birth_date = datetime.datetime.strptime(birthday, '%m/%d/%Y').date()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

# Function to convert amount to words
def amount_in_words(amount):
    units = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    tens = ["Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    
    def convert_number_to_words(num):
        if num == 0:
            return "Zero"
        elif num < 10:
            return units[num]
        elif num < 20:
            return teens[num - 10]
        elif num < 100:
            return tens[num // 10 - 2] + ('' if num % 10 == 0 else ' ' + units[num % 10])
        elif num < 1000:
            return units[num // 100] + ' Hundred' + ('' if num % 100 == 0 else ' ' + convert_number_to_words(num % 100))
        elif num < 10000:
            return convert_number_to_words(num // 1000) + ' Thousand' + ('' if num % 1000 == 0 else ' ' + convert_number_to_words(num % 1000))
        else:
            return "Amount too large"
    
    return convert_number_to_words(int(amount)) + " Pesos"

# Function to add a new record
def add_record(records):
    name = input("Enter Name: ")
    birthday = input("Enter Birthday (MM/DD/YYYY): ")
    allowance = float(input("Enter Weekly Allowance: "))
    skills = input("Enter Skills (comma-separated): ").split(',')
    
    # Creating the record
    record = {
        'name': name,
        'birthday': birthday,
        'allowance': allowance,
        'skills': skills
    }
    records.append(record)

    # Save records to JSON file
    with open('records.json', 'w') as file:
        json.dump(records, file, indent=4)

# Function to load records from JSON file
def load_records():
    try:
        with open('records.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to display records with additional information
def display_records(records):
    if not records:
        print("No records found.")
        return
    
    for record in records:
        name = record['name']
        birthday = record['birthday']
        allowance = record['allowance']
        skills = record['skills']
        
        alias = create_alias(name)
        age = calculate_age(birthday)
        allowance_words = amount_in_words(allowance)
        first_two_skills = skills[:2]

        print(f"\nNAME: {name}")
        print(f"ALIAS: {alias}")
        print(f"BIRTHDAY: {birthday}")
        print(f"AGE: {age} years old")
        print(f"ALLOWANCE: {allowance}")
        print(f"AMOUNT IN WORDS: {allowance_words}")
        print(f"SKILLS: {', '.join(first_two_skills)}")
        print(f"NUMBER OF SKILLS: {len(skills)}")
    
    # Display total number of records
    print(f"\nNumber of Record(s): {len(records)}")

# Main program
def main():
    records = load_records()
    
    while True:
        choice = input("\nChoose an option:\n1. Add Record\n2. Display Records\n3. Exit\n")
        
        if choice == '1':
            add_record(records)
        elif choice == '2':
            display_records(records)
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid option, please choose again.")

if __name__ == '__main__':
    main()
