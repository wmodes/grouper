# Grouper - Add students to groups based on preference

The Kernighan-Lin algorithm creates a k-way graph partition that determines the grouping of students based on their preferences for working with other students and compatibility with other classmates. The graph recognizes student compatibility through numerical weights (indicators of student positional relationship on the graph). This grouping method allows for a systematic approach and balanced number of student groups capable of tackling different types of work. Students should enter student name, number of groups, objective weights (optional), objective_measures(optional), students preferred to work with (optional), preference weight(optional), and preferences_weight_match(optional). Note that number of groups must be at least 2 and be a power of 2, i.e. 2, 4, 8, etc.

The program relies on the graph function of [GatorGrouper](https://github.com/GatorIncubator/gatorgrouper).

## Usage

Usage: group.py classname term groups [pref]
where:
   classname: class name, e.g., art101
   term: current term, e.g., f21, s22
   groups: number of groups (has to be a power of 2)
   pref: any value indicates a pref file has been written in data dir, e.g., art101-pref.csv
      Pref file format is: Dominic Jones,Hannah McAllister,-100
Requirements:
   * A survey file exists in the data dir corresponding to the term, e.g., art101s22
   * A pref file exists in the data dir for this term, e.g., art101s22-pref
