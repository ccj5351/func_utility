from datetime import datetime
from collections import defaultdict

def get_early_day(date1_str, date2_str, is_verbose=False):
    # Convert the string dates to datetime objects
    date1 = datetime.strptime(date1_str, '%Y-%m-%d')
    date2 = datetime.strptime(date2_str, '%Y-%m-%d')
    
    # Compare the two dates
    if date1 >= date2:
        if is_verbose:
            print(f"{date2_str} is early than {date1_str}.")
        return date2_str
    else:
        if is_verbose:
            print(f"{date1_str} is early than {date2_str}.")
        return date1_str

def get_late_day(date1_str, date2_str, is_verbose = False):
    # Convert the string dates to datetime objects
    date1 = datetime.strptime(date1_str, '%Y-%m-%d')
    date2 = datetime.strptime(date2_str, '%Y-%m-%d')
    
    # Compare the two dates
    if date2 >= date1:
        if is_verbose:
            print(f"{date2_str} is later than {date1_str}.")
        return date2_str
    else:
        if is_verbose:
            print(f"{date1_str} is later than {date2_str}.")
        return date1_str


def get_days(start_date_str, end_date_str, is_verbose=False):
    # Convert the string dates to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    # Calculate the difference between the two dates
    difference = end_date - start_date

    # Print the number of days between the two dates
    if is_verbose:
        print(f"The number of days between {start_date_str} and {end_date_str} is {difference.days} days.")
    return difference.days

if __name__ == "__main__":
    # Define your starting and ending dates as strings
    
    # ----- Your Input ----
    # ----- Your Input ----
    # ----- Your Input ----
    star_end_days = {
        # '%Y-%m-%d'
        'cc':   ['2024-01-26', '2024-03-31'],
        'amy':  ['2024-01-26', '2024-02-29'],
        'mai':  ['2024-01-26', '2024-03-31'],
        'wan':  ['2024-01-26', '2024-03-31'],
        'zhan': ['2024-03-01', '2024-03-31'],
    }
    
    bill_sum_info = defaultdict(float)

    bill_info = {
        "water": {
            'amount': 280.40,
            'period': ['2024-01-26', '2024-03-22'],
            },
        "internet (WiFi)": {
            'amount': 65.0,
            'period': ['2024-03-01', '2024-03-31'],
            },
        "electric-gas": {
            'amount': 159.26,
            'period': ['2024-03-01', '2024-03-31'],
        },
    }
    # ----- Your Input ----
    # ----- Your Input ----
    # ----- Your Input ----
    
    
    updated_star_end_days = {
        'water': {},
        "internet (WiFi)": {},
        "electric-gas": {},
    }

    days_info = {
        'water': defaultdict(int),
        "internet (WiFi)": defaultdict(int),
        "electric-gas": defaultdict(int),
    }
    
    per_person_bill_info = {
        'water': defaultdict(int),
        "internet (WiFi)": defaultdict(int),
        "electric-gas": defaultdict(int),
    }

    for bill_type in bill_info.keys(): 
        print ("\n\n")
        bill_amount = bill_info[bill_type]['amount']
        bill_period = bill_info[bill_type]['period']
        bill_days = get_days(bill_period[0], bill_period[1])
        days_sum = 0
        for k, v in star_end_days.items():
            start_day = get_late_day(v[0], bill_period[0])
            end_day = get_early_day(v[1], bill_period[1])
            days = max(get_days(start_day, end_day), 0)
            updated_star_end_days[bill_type][k] = [start_day, end_day]
            days_info[bill_type][k] = days
            days_sum += days

        print (f"Total {bill_type} bill = ${bill_amount}, between {bill_period[0]}-{bill_period[1]}, i.e., {bill_days} days")
        print ("Calculate bill per person, accorinding to living days within this bill time ")
        bill_sum = 0
        for k, v in days_info[bill_type].items():
            bil = v/days_sum*bill_amount
            bil = float(f"{bil:.2f}")
            per_person_bill_info[bill_type][k] = bil
            bill_sum += bil
            print (f"\t{k}: between {updated_star_end_days[bill_type][k][0]}-{updated_star_end_days[bill_type][k][1]}, i.e., {v} days, ==> avg bill = ${bil}")
            bill_sum_info[k] += bil
        print (f"Total {bill_type} bill = {bill_sum:.3f}")

    print (bill_sum_info)
