# Grouper - Add students to groups based on preference

The Kernighan-Lin algorithm creates a k-way graph partition that determines the grouping of students based on their preferences for working with other students and compatibility with other classmates. The graph recognizes student compatibility through numerical weights (indicators of student positional relationship on the graph). This grouping method allows for a systematic approach and balanced number of student groups capable of tackling different types of work. i

Students provide their name, contact info, and an arbitrary number of criteria via a form. The results are represented as a CSV file provided to the algorithm. A configuration file in JSON format specifies whether the criteria are to be be matched heterogeneously or homogeneously, and the weights for each criteria.

A weakness of the Kernighan-Lin algorithm, since it repeatedly bisects the group of students, is that the number of groups must be a power of 2, i.e. 2, 4, 8, etc. 

The program relies on the graph function of [GatorGrouper](https://github.com/GatorIncubator/gatorgrouper).

## Usage

Usage: group.py classname term groups [pref]

* classname: class name, e.g., art101
* term: current term, e.g., f21, s22
* groups: number of groups (has to be a power of 2)
* pref: any value indicates a pref file has been written in data dir

Example:

```
% py group.py art101 f22 true
```
which will expect student data in `data/art101-f22.csv` and student preferences in `data/art101-f22-pref.csv`

The preferences file format is:
```
Dominic Jones,Hannah McAllister,-100
```
indicating these students do not want to work together.

TODO: This can be added automatically from tudent's initial survey form if they have preferences.

## Requirements

   * Config file exists in the grouper dir
   * CSV survey file exists in the data dir corresponding to the term, e.g., art101-s22.
   * I generated the survey from a google form similar to [this one](https://docs.google.com/forms/d/e/1FAIpQLSccIhmCWCQJsJZb9ufQiZGFb8NhfwjdQeqK_26_KfXpaAbeKg/viewform).
   * A pref file exists in the data dir for this term if indicated, e.g., art101s22-pref
   * GatorGrouper is installed

## Config File

The config file describes how fields in the student data are matched, similar or diverse:
```
OBJECTIVES = [
    {
        "field": "schedule 1",
        "measure": "similar",
        "weight": 10,
    },
    .
    .
    .
    {
        "field": "expertise 1",
        "measure": "diverse",
        "weight": 10,
    },
    .
    .
    .
    {
        "field": "interest 1",
        "measure": "similar",
        "weight": 3,
    },
    .
    .
    .
]

PREFERENCES = {
    "weight": -100,
    "matchweight": 100
}
```

## Caveats

I had some problems with GatorGrouper in Python 3.10.

Particularly, CSV files may not be able to be read without a fwe changes to `gatorgrouper/utils/read_student_file.py`.

* Change `read(1024)` to `readline()`
* Change `csv.reader(csvfile)` to `csv.reader(csvfile, quotechar='"', delimiter=',')`

I also had a problem with the Mappings module not being found:

```
ImportError: cannot import name 'Mapping' from 'collections'
```
This is caused by a change in the collections interface starting with Python 3.10. I fixed this by updating all of my installed packages.
