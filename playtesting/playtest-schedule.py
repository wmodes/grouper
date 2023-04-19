# playtest scheduler
# like speed dating for games playtesting
#
# Wes Modes <wmodes@ucsc.edu>
# April 2023

import random
# import pprint

class PlaytestScheduler:

    def __init__(self, num_groups, num_days, num_periods, faculty_list):
        self.num_groups = num_groups
        self.num_days = num_days
        self.num_periods = num_periods
        self.faculty_list = faculty_list
        self.num_faculty = len(faculty_list)

        # Set the number of groups, faculty, days, and periods
        team_nums = list(range(1, num_groups+1))
        self.all_groups = [f"Team {str(team).zfill(2)}" for team in team_nums]
        self.bad_luck_threshold = 100
        self.bad_luck_text = "While choosing the last few playtesters in a session, it can happen that\nthe only playtesters left (since they are randomly selected) are ones that\nwere previously matched to a host.\n\nI could probably make it redo the whole session automatically, but for now..\n\nBAD LUCK! Rerun the script\n"
        self.bad_luck_text = "(Bad luck: Rescheduling)"

        # if we have an odd number of total groups + faculty
        if num_groups + len(self.faculty_list) % 2 != 0:
            self.faculty_list.append("Group Work")
        self.num_faculty = len(self.faculty_list)

        # create a record of who gets paired during the day
        # to prevent rematching
        self.day_record_of_pairs = {}

    def print_sorted_schedule(self, schedule):
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

    def sched_session(self, day, period):
        bad_luck_flag = True
        while bad_luck_flag is True:
            # later, bad_luck_flag will only be set if we have bad luck
            bad_luck_flag = False
            # create an empty schedule
            schedule = []
            # make a copy of the list of playtesters from which to pick
            playtester_pool = self.playtesting_groups[:]
            # schedule every session during the period
            # one for each hosting_group
            for session in range(1, len(self.hosting_groups) + 1):
                host = self.hosting_groups[session - 1]
                # check to make sure host and playtester not already paired
                # while keeping track of iteractions to account for bad luck
                iterations = 0
                while True:
                    playtester = random.choice(playtester_pool)
                    if host not in self.day_record_of_pairs or playtester not in self.day_record_of_pairs[host]:
                        break
                    # it can happen that the only playtester left 
                    # (since they are randomly selected)
                    # is that the only playtester left is a previous pair
                    iterations += 1
                    if iterations > self.bad_luck_threshold:
                        # print(self.bad_luck_text)
                        # exit(1)
                        bad_luck_flag = True
                        break
                # if we break out of the while, break out of the for-loop
                if bad_luck_flag:
                    break
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
                if host not in self.day_record_of_pairs:
                    self.day_record_of_pairs[host] = [playtester]
                else:
                    self.day_record_of_pairs[host].append(playtester)
        return(schedule)
    
    def sched_day(self, day):
        # shuffle the groups
        random.shuffle(self.all_groups)

        # FIRST HALF

        # Assign the first half of the groups, to hosting duties
        self.hosting_groups = self.all_groups[:(self.num_groups + self.num_faculty)//2]

        # Assign the second half of the groups, along with the faculty to playtesting duties
        self.playtesting_groups = self.all_groups[(self.num_groups + self.num_faculty)//2:] + self.faculty_list

        if self.num_days == 1:
            day_str = f"PLAYTESTING DAY (first half)"
        else:
            day_str = f"DAY {day} (first half)"
        underline = "=" * len(day_str)
        print(f"\n{day_str}\n{underline}")
        # print("hosting:", f"({len(hosting_groups)} groups)", hosting_groups)
        # print("playtesting:", f"({len(playtesting_groups)} groups)", playtesting_groups)

        # Assign a host and playtester for each session of each period during the first half
        for period in range(1, self.num_periods//2 + 1):
            print(f"\nSession {period}")
            schedule = self.sched_session(day, period)
            self.print_sorted_schedule(schedule)
            # pprint.pprint(self.day_record_of_pairs)

        # SECOND HALF

        # Reverse the list so playtesters become hosts and vice versa
        self.all_groups.reverse()

        # Assign the first half of the groups, to hosting duties
        self.hosting_groups = self.all_groups[:(self.num_groups + self.num_faculty)//2]

        # Assign the second half of the groups, along with the faculty to playtesting duties
        self.playtesting_groups = self.all_groups[(self.num_groups + self.num_faculty)//2:] + self.faculty_list

        if self.num_days == 1:
            day_str = f"PLAYTESTING DAY (second half)"
        else:
            day_str = f"DAY {day} (second half)"
        underline = "=" * len(day_str)
        print(f"\n{day_str}\n{underline}")
        # print("hosting:", f"({len(hosting_groups)} groups)", hosting_groups)
        # print("playtesting:", f"({len(playtesting_groups)} groups)", playtesting_groups)

        # Assign a host and playtester for each session of each period during the first half
        for period in range(self.num_periods//2 + 1, self.num_periods + 1):
            print(f"\nSession {period}")
            schedule = self.sched_session(day, period)
            self.print_sorted_schedule(schedule)
            # pprint.pprint(self.day_record_of_pairs)

    def sched_several_days(self):
        # Assign each session to a hosting and playtesting group
        for day in range(1, self.num_days+1):
            self.sched_day(day)

    def main(self):
        self.sched_several_days()

if __name__ == '__main__':
    # Set the number of groups, faculty, days, and periods
    num_groups = 38
    num_faculty = 3
    num_days = 1
    num_periods = 6        
    faculty_list = [
        "Tamara",
        "Graeme",
        "Wes"
    ]

    # Create a PlaytestScheduler object
    scheduler = PlaytestScheduler(num_groups, num_days, num_periods, faculty_list)

    # Run the scheduler
    scheduler.main()