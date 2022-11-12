
import sys
import csv
from pathlib import Path
from importlib import import_module
import pprint
import re
import os

# Read raw CSV data file
# Make basic edits to raw data
#   Remove the timestamp column (:%s/^[^,]*,//)
#   Join the name and email columns (:%s/,/ - /)
#   Remove " - Hella" and " - Meh" from the data (:%s/ - \(Meh\|Hella\)//g)
#   Remove " - Best" and " - Worst" from the data (:%s/ - \(Best\|Worst\)//g))
#   Remove " - Little" and " - Lots" from the data (:%s/ - \(Little\|Lots\)//g))
#   Check for the unlikely event of blank fields (:%s/,,/,1,/g)
#   Delete human readable notes fields
# Read config file
# Read conflicts file
# Build GG command options
# Run GG

DATADIR = "data"
GG = "../gatorgrouper/gatorgrouper_cli.py"

class Grouper(object):
    """
    """
    def __init__(self, args):
        # Check for command line options
        # print(f"DEBUG: args: {len(args)}")
        if len(args) < 4:
            self.usage()
            exit(1)
        self.classname = args[1]
        self.term = args[2]
        self.numgroups = args[3]
        if (len(args) > 4):
            self.prefopt = args[4]
        else:
            self.prefopt = ""
        # print ("DEBUG: opts processed:", self.classname, self.term, self.numgroups, self.prefopt)
        self.conf_filename = f"{self.classname}_conf.py"
        self.conf_modname = f"{self.classname}_conf"
        self.datafile = f"{DATADIR}/{self.classname}-{self.term}.csv"
        self.prepfile = f"{DATADIR}/tmp-prep.csv"
        self.preffile = f"{DATADIR}/tmp-pref.csv"
        self.received_fields = []
        self.target_fields = []
        self.class_data = []
        self.cli_opts = ''

    def read_class_config(self):
        """
        """
        print("* Reading class config")
        conf_file = Path(self.conf_filename)
        if not conf_file.is_file():
            print(f"ERROR: configuration file not found: {self.conf_filename}")
            print("param 1 must be classname")
            print()
            usage()
            exit(1)
            # file exists
        self.config = import_module(self.conf_modname)
        # config = __import__(conf_filename)
        # pprint.pprint(self.config.OBJECTIVES)

    def prep_fields(self):
        """
        Example:
        DATA_FIELDS = ['timestamp', 'email', 'name', 'schedule1', 'schedule2', 'exertise1', 'expertise1']
        """
        self.received_fields = ['timestamp', 'email', 'name']
        self.target_fields = ['name']
        for i in range(len(self.config.OBJECTIVES)):
            field = self.config.OBJECTIVES[i]["field"]
            self.received_fields.append(field)
            self.target_fields.append(field)
        # print(f"DEBUG: data_fields: {self.data_fields}")

    def read_class_data(self):
        """
        """
        print ('* Reading class data')
        with open(self.datafile, newline='') as csvfile:
            reader = csv.DictReader(csvfile, self.received_fields, restkey='extras', skipinitialspace=True)
            # skips the header line
            # next(reader)
            for row in reader:
                if row['name'] != '':
                    self.class_data.append(dict(row))
        # pprint.pprint(self.class_data)

    def prep_data(self):
        for i in range(len(self.class_data)):
            # remove timestamp col
            self.class_data[i].pop('timestamp', None)
            # combine name and Email in name col
            self.class_data[i]['name'] = f"{self.class_data[i]['name']} <{self.class_data[i]['email']}>"
            # remove weird characters from names
            self.class_data[i]['name'] = re.sub(r'[^,-.@<>\w\s]','', self.class_data[i]['name'])
            # remove email column
            self.class_data[i].pop('email', None)
            # remove Extras
            self.class_data[i].pop('extras', None)
            # iterate over fields and remove -hella, -meh, etc
            remove = [' -Meh', ' - Hella', ' - Best', ' - Worst', ' - Little', ' - Lots']
            for key in self.class_data[i]:
                if key == 'name':
                    continue
                str = self.class_data[i][key]
                # print(f"DEBUG: {key}: {str}")
                # Remove " - Hella" and " - Meh" from the data (:%s/ - \(Meh\|Hella\)//g)
                extract_num = re.findall(r'\d+', str)
                if extract_num:
                    self.class_data[i][key] = int(extract_num[0])
                else:
                    self.class_data[i][key] = 1
                # Check for the unlikely event of blank fields (:%s/,,/,1,/g)
                if self.class_data[i][key] == '':
                    self.class_data[i][key] = 1
        # print(f"DEBUG: {pprint.pformat(self.class_data)}")

    def write_prepfile(self):
        """
        """
        with open(self.prepfile, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, quotechar='"', delimiter=',',
            quoting=csv.QUOTE_NONNUMERIC,
            fieldnames=self.target_fields)
            writer.writeheader()
            for i in range(1,len(self.class_data)):
                writer.writerow(self.class_data[i])

    def build_cl_opt(self):
        """
        Build GatorGrouper command line options.

        Sample command line for gatorgrouper:

        python gatorgrouper_cli.py --file data/test-prep.csv --num-group 4 --method graph --objective-measures diff diff diff diff diff diff diff diff diff diff diff diff diff diff diff diff diff diff diff diff diff diff diff diff diff diff diff diff diff diff diff diff diff --objective-weights -10 -10 -10 -10 -10 -10 -10 -10 -10 -10 -10 -10 -10 -10 -10 -10 10 10 10 -15 5 -5 5 3 -3 -3 -3 -3 -3 -3 -3 -3 -3--preferences data/test-pref.csv --preferences-weight -100 --preferences-weight-match 100"
        """
        cli_file = f"--file {self.prepfile}"
        cli_groups = f"--num-group {self.numgroups}"
        cli_method = "--method graph"
        cli_obj_measures = "--objective-measures"
        cli_obj_weights = "--objective-weights"
        for i in range(len(self.config.OBJECTIVES)):
            cli_obj_measures += " diff"
            measure = self.config.OBJECTIVES[i]["measure"]
            weight = self.config.OBJECTIVES[i]["weight"]
            if measure == "similar":
                cli_obj_weights += f" -{weight}"
            elif measure == "diverse":
                cli_obj_weights += f" {weight}"
            else:
                print(f"ERROR: config file unrecognized measure: {measure}")
                exit(1)
        if (self.prefopt):
            cli_pref = f"--preferences {self.preffile} --preferences-weight {self.config.PREFERENCES['weight']} --preferences-weight-match {self.config.PREFERENCES['matchweight']}"
        else:
            cli_pref = ""
        self.cli_opts = f"{cli_file} {cli_groups} {cli_method} {cli_obj_measures} {cli_obj_weights} {cli_pref}"
        # print(f"DEBUG: CLI OPTS: {cli_opts}")

    def usage(self):
        print (f"Usage: {sys.argv[0]} classname term groups [pref]")
        print ("where:")
        print ("   classname: class name, e.g., art101")
        print ("   term: current term, e.g., f21, s22")
        print ("   groups: number of groups (has to be a power of 2)")
        print ("   pref: any value indicates a pref file has been written in data dir, e.g., art101-pref.csv")
        print ("      Pref file format is: Dominic Jones,Hannah McAllister,-100")
        print ("Requirements:")
        print ("   * A survey file exists in the data dir corresponding to the term, e.g., art101s22")
        print ("   * A pref file exists in the data dir for this term, e.g., art101s22-pref")

    def run_gatorgrouper(self):
        print("* Generating groups")
        command = f"python3 {GG} {self.cli_opts}"
        os.system(command)

    def main(self):
        print("\nCreating a k-way graph partition with the Kernighan-Lin algorithm to determine the grouping of students based on their preferences for working with other students and compatibility with other classmates. (Ref: https://github.com/GatorIncubator/gatorgrouper)\n")
        self.read_class_config()
        self.prep_fields()
        self.read_class_data()
        self.prep_data()
        self.write_prepfile()
        self.build_cl_opt()
        self.run_gatorgrouper()


if __name__ == "__main__":
    # print(f"DEBUG: argv: {sys.argv}")
    grouper = Grouper(sys.argv)
    grouper.main()
