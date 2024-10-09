import json
import uuid
import random

def generate_new_file(input_file, output_file, firstname, lastname, email, manager):
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Generate new random values
    data['num_employee'] = str(uuid.uuid4())
    data['oracle_id'] = str(uuid.uuid4())
    data['employee_firstname'] = firstname
    data['employee_lastname'] = lastname
    data['role'] = "Developer"
    data['email'] = email
    data['manager'] = manager
    
    for language in data['languages']:
        language['id_language'] = str(uuid.uuid4())

    for skill in data['other_skills']:
        skill['id_other_skills'] = str(uuid.uuid4())
        skill['duration'] = random.randint(1, 100)

    for evolution in data['evolutions']:
        evolution['id_evolution'] = str(uuid.uuid4())
        evolution['experiences'] = random.randint(1, 100)
        evolution['opportunity_time'] = random.randint(1, 100)
        evolution['manager_confidence'] = random.randint(1, 100)

        for education in evolution['ongoing_educations']:
            education['id_ongoing_education'] = str(uuid.uuid4())
            education['duration'] = random.randint(1, 100)
            education['completed'] = random.choice([True, False])
            education['certifying'] = random.choice([True, False])

    for mandate in data['mandates']:
        mandate['id_mandate'] = str(uuid.uuid4())
        mandate['size'] = random.randint(1, 1000)
        mandate['effort'] = random.randint(1, 100)
        mandate['start_date'] = f"{random.randint(2020, 2025)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
        mandate['end_date'] = f"{random.randint(2020, 2025)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"

        for technology in mandate['technologies']:
            technology['technology'] = random.choice(['Java', 'Python', 'C++', 'JavaScript'])

        for tool in mandate['tools']:
            tool['tool'] = random.choice(['Eclipse', 'Visual Studio', 'IntelliJ', 'Sublime Text'])

        for responsibility in mandate['responsibilities']:
            responsibility['responsibility'] = random.choice(['Development', 'Testing', 'Design', 'Deployment'])

    for publication in data.get('publications', []):
        publication['id_publication'] = str(uuid.uuid4())

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

# Example usage:
generate_new_file('./documents/ManuelLegault.json', './documents/output1.json', 'John', 'Doe', 'jdoe@alithya.com', 'manuel.legault@alithya.com')
generate_new_file('./documents/ManuelLegault.json', './documents/output2.json', 'Jane', 'Smith', 'jsmith@alithya.com', 'manuel.legault@alithya.com')
generate_new_file('./documents/ManuelLegault.json', './documents/output3.json', 'Bob', 'Johnson', 'bjohnson@alithya.com', 'manuel.legault@alithya.com')
generate_new_file('./documents/ManuelLegault.json', './documents/output4.json', 'Alice', 'Williams', 'awilliams@alithya.com', 'manuel.legault@alithya.com')
generate_new_file('./documents/ManuelLegault.json', './documents/output5.json', 'Mike', 'Brown', 'mbrown@alithya.com', 'manuel.legault@alithya.com')
generate_new_file('./documents/ManuelLegault.json', './documents/output6.json', 'Emily', 'Davis', 'edavis@alithya.com', 'manuel.legault@alithya.com')
generate_new_file('./documents/ManuelLegault.json', './documents/output7.json', 'Tom', 'Miller', 'tmiller@alithya.com', 'manuel.legault@alithya.com')
generate_new_file('./documents/ManuelLegault.json', './documents/output8.json', 'Sarah', 'Wilson', 'swilson@alithya.com', 'manuel.legault@alithya.com')
generate_new_file('./documents/ManuelLegault.json', './documents/output9.json', 'David', 'Moore', 'dmooore@alithya.com', 'manuel.legault@alithya.com')
generate_new_file('./documents/ManuelLegault.json', './documents/output10.json', 'Lisa', 'Taylor', 'ltaylor@alithya.com', 'manuel.legault@alithya.com')

