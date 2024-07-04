import csv
from collections import defaultdict
import unicodedata

def give_xp(pourcentage, sessions, max_sessions, max_xp):
    if sessions >= (2/3) * max_sessions:
        if pourcentage >= 0.75:
            xp = max_xp
        elif pourcentage >= 0.5:
            xp = (2/3) * max_xp
        elif pourcentage >= 0.25:
            xp = (1/3) * max_xp
        else:
            xp = 0
    elif sessions >= (1/3) * max_sessions and pourcentage >= 0.75:
        xp = (1/3) * max_xp
    else:
        xp = 0
    return round(xp)

def read_organisator_file(file_path):
    organisators = defaultdict(set)
    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            login = row[0].strip()
            activity = normalize_activity_name(row[1].strip())
            organisators[login].add(activity)
    return organisators

def normalize_activity_name(name):
    return ''.join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')

def hub(args):
    [file_path, activity_type, selected_promo, has_result, output_file_path, write_header, organisator_file] = [args.filename, args.act, args.promo, args.has_result, "HUB_output.csv", True, args.organisators_file]
    focus_data = defaultdict(lambda: defaultdict(lambda: {"presences": 0, "absences": 0, "total": 0, "promo": None}))
    activity_columns = {}

    organisators = read_organisator_file(organisator_file)

    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file, delimiter=';')
        headers = next(reader)

        for i, header in enumerate(headers):
            activity = normalize_activity_name(header.split('.')[0])
            if activity_type in ['fg', 'both'] and ('Focus Groupe' in header or 'Focus groupe' in header):
                activity_columns.setdefault(activity, []).append(i)
            elif activity_type in ['fablab', 'both'] and 'FabLab' in header:
                activity_columns.setdefault(activity, []).append(i)

        login_index = headers.index('Login')
        promo_index = headers.index('Promo')

        for row in reader:
            promo = int(row[promo_index])
            if selected_promo is None or promo == selected_promo:
                login = row[login_index]
                focus_data[login]["_promo"] = promo
                for activity, indices in activity_columns.items():
                    for i in indices:
                        focus_data[login][activity]["total"] += 1
                        if row[i].strip().lower() == 'present':
                            focus_data[login][activity]["presences"] += 1
                        elif row[i].strip().lower() == 'absent':
                            focus_data[login][activity]["absences"] += 1
                # Automatically set 100% participation for organizers
                for activity in organisators[login]:
                    focus_data[login][activity]["presences"] = focus_data[login][activity]["total"]

    max_sessions = max(focus_data[login][activity]["total"] for login in focus_data for activity in activity_columns)

    with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(['Login', 'Promo'] + list(activity_columns.keys()) + ['XP'])

        for login in sorted(focus_data):
            promo = focus_data[login]["_promo"]
            total_presences = sum(focus_data[login][activity]["presences"] for activity in activity_columns)
            
            should_write_row = True
            if has_result == 'yes' and total_presences == 0:
                should_write_row = False
            elif has_result == 'no' and total_presences > 0:
                should_write_row = False
            
            if should_write_row:
                row_data = [login, promo if promo is not None else 'All']
                participation_xp_list = []
                for activity in activity_columns:
                    x = focus_data[login][activity]["presences"]
                    abs = focus_data[login][activity]["absences"]
                    y = focus_data[login][activity]["total"]
                    z = f"{x / y:.2%}" if y > 0 else "N/A"
                    row_data.append(f"{x} ({abs} abs) / {y} ({z})")
                    participation_percentage = x / y if y > 0 else 0
                    participation_xp_list.append(give_xp(participation_percentage, y, max_sessions, 15))
                
                participation_xp = max(participation_xp_list)
                organizing_xp = 0
                if any(focus_data[login][activity]["total"] == max_sessions for activity in organisators[login]):
                    organizing_xp = give_xp(1.0, max_sessions, max_sessions, 35)
                
                xp = max(participation_xp, organizing_xp)
                row_data.append(xp)

                writer.writerow(row_data)
