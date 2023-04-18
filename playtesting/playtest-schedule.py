# playtest scheduler
# like speed dating for games playtesting
#
# Wes Modes <wmodes@ucsc.edu>
# April 2023

import random
import pprint

# Set the number of groups, faculty, days, and periods
num_groups = 38
team_nums = list(range(1, num_groups+1))
all_groups = [f"Team {str(team).zfill(2)}" for team in team_nums]
bad_luck_threshold = 100
bad_luck_text = """
While choosing the last few playtesters in a session, it can happen that
the only playtesters left, since they are randomly selected, are ones that
were previously matched to a host.

I could probably make it redo the whole session automatically, but for now..

BAD LUCK! Rerun the script
"""

all_faculty = [
    "Tamara",
    "Graeme",
    "Wes"
]
# if we have an odd number of total groups + faculty
if num_groups + len(all_faculty) % 2 != 0:
    all_faculty.append("Group Work")
num_faculty = len(all_faculty)

num_days = 1
num_periods = 6

def print_sorted_schedule(schedule):
    # sort the schedule
    schedule_list = []
    for session in schedule:
        period = session["Period"]
        host = session["Host"]
        playtester = session["Playtester"]
        row = f"Host: {host}, Playtester: {playtester}"
        schedule_list.append(row)
    schedule_list.sort()

    # Print the schedule
    for row in schedule_list:
        print(row)

# Assign each session to a hosting and playtesting group
schedule = []
for day in range(1, num_days+1):

    # shuffle the groups
    random.shuffle(all_groups)

    # create a record of who gets paired during the day
    # to prevent rematching
    day_record_of_pairs = {}

    # FIRST HALF

    # Assign the first half of the groups, to hosting duties
    hosting_groups = all_groups[:(num_groups + num_faculty)//2]

    # Assign the second half of the groups, along with the faculty to playtesting duties
    playtesting_groups = all_groups[(num_groups + num_faculty)//2:] + all_faculty

    if num_days == 1:
        day_str = f"PLAYTESTING DAY (first half)"
    else:
        day_str = f"DAY {day} (first half)"
    underline = "=" * len(day_str)
    print(f"\n{day_str}\n{underline}")
        # print("hosting:", f"({len(hosting_groups)} groups)", hosting_groups)
        # print("playtesting:", f"({len(playtesting_groups)} groups)", playtesting_groups)

    # Assign a host and playtester for each session of each period during the first half
    for period in range(1, num_periods//2 + 1):
        # create an empty schedule
        schedule = []
        # make a copy of the list of playtesters from which to pick
        playtester_pool = playtesting_groups[:]
        print(f"\nSession {period}")
        for session in range(1, len(hosting_groups) + 1):
            host = hosting_groups[session - 1]
            # check to make sure host and playtester not already paired
            iterations = 0
            while True:
                playtester = random.choice(playtester_pool)
                if host not in day_record_of_pairs or playtester not in day_record_of_pairs[host]:
                    break
                # it can happen that the only playtester left 
                # (since they are randomly selected)
                # is that the only playtester left is a previous pair
                iterations += 1
                if iterations > bad_luck_threshold:
                    print(bad_luck_text)
                    exit(1)
            # remove playtester if already assigned
            playtester_pool.remove(playtester) 
            schedule.append({
                "Day": day,
                "Period": period,
                "Session": session,
                "Host": host,
                "Playtester": playtester,
            })
            # record who got paired with whom that day
            if host not in day_record_of_pairs:
                day_record_of_pairs[host] = [playtester]
            else:
                day_record_of_pairs[host].append(playtester)
        print_sorted_schedule(schedule)
        # pprint.pprint(day_record_of_pairs)

    # SECOND HALF

    # Reverse the list so playtesters become hosts and vice versa
    all_groups.reverse()

    # Assign the first half of the groups, to hosting duties
    hosting_groups = all_groups[:(num_groups + num_faculty)//2]

    # Assign the second half of the groups, along with the faculty to playtesting duties
    playtesting_groups = all_groups[(num_groups + num_faculty)//2:] + all_faculty

    if num_days == 1:
        day_str = f"PLAYTESTING DAY (second half)"
    else:
        day_str = f"DAY {day} (second half)"
    underline = "=" * len(day_str)
    print(f"\n{day_str}\n{underline}")
    # print("hosting:", f"({len(hosting_groups)} groups)", hosting_groups)
    # print("playtesting:", f"({len(playtesting_groups)} groups)", playtesting_groups)

    # Assign a host and playtester for each session of each period during the first half
    for period in range(num_periods//2 + 1, num_periods + 1):
        # create an empty schedule
        schedule = []
        # make a copy of the list of playtesters from which to pick
        playtester_pool = playtesting_groups[:]
        print(f"\nSession {period}")
        for session in range(1, len(hosting_groups) + 1):
            host = hosting_groups[session - 1]
            # check to make sure host and playtester not already paired
            iterations = 0
            while True:
                playtester = random.choice(playtester_pool)
                if host not in day_record_of_pairs or playtester not in day_record_of_pairs[host]:
                    break
                # it can happen that the only playtester left 
                # (since they are randomly selected)
                # is that the only playtester left is a previous pair
                iterations += 1
                if iterations > bad_luck_threshold:
                    print(bad_luck_text)
                    exit(1)
            # remove playtester once assigned
            playtester_pool.remove(playtester) 
            schedule.append({
                "Day": day,
                "Period": period,
                "Session": session,
                "Host": host,
                "Playtester": playtester,
            })      
            # record who got paired with whom that day
            if host not in day_record_of_pairs:
                day_record_of_pairs[host] = [playtester]
            else:
                day_record_of_pairs[host].append(playtester)
        print_sorted_schedule(schedule)
        # pprint.pprint(day_record_of_pairs)