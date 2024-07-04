import csv
import random

def stumper(args):
    [first_csv_path, second_csv_path, output_csv_path] = [args.previous_duo, args.current_list, "STUMPER_output.csv"]
    # Load the list of valid logins from the registered student csv (second) CSV
    with open(second_csv_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, delimiter=';')
        valid_logins = set(row['login'] for row in reader)

    valid_groups = []

    with open(first_csv_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            # Extract members from the row, filtering out empty values
            members = [row.get(column) for column in ['master', 'member0', 'member1'] if row.get(column)]
            # If all members are in the valid logins, add the group
            if all(member in valid_logins for member in members):
                valid_groups.append(members)
                valid_logins.remove(members[0])
                valid_logins.remove(members[1])
                valid_logins.remove(members[2]) if len(members) == 3 else None
            
    # Randomly pair any ungrouped members
    leftovers = [login for login in valid_logins if login]
    leftovers_stk = leftovers.copy()
    random.shuffle(leftovers)
    while len(leftovers) > 1:
        valid_groups.append(leftovers[:2] + [''])
        leftovers = leftovers[2:]

    # If there's one member left, add them to an existing pair to make it a trio
    if leftovers:
        for group in valid_groups:
            if len(group) == 2:  # Find an existing pair
                group.append(leftovers.pop())
                break
        else:
            # If no existing pair is found, create a new single-member group
            valid_groups.append([''] + leftovers + [''])

    valid_groups.sort(key=lambda group: group[0]) # Sort by master login

    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['master', 'member0', 'member1', 'comment'])
        for group in valid_groups:
            # Fill any missing columns to ensure three columns in total
            while len(group) < 3:
                group.append('')
            if group[0] in leftovers_stk or group[1] in leftovers_stk or group[2] in leftovers_stk:
                group.append('New Group')
            else:
                group.append('')
            writer.writerow(group)

    print(f"Output written to {output_csv_path}")