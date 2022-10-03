# Grouper - Add students to groups based on preference

The Kernighan-Lin algorithm creates a k-way graph partition that determines the grouping of students based on their preferences for working with other students and compatibility with other classmates. The graph recognizes student compatibility through numerical weights (indicators of student positional relationship on the graph). This grouping method allows for a systematic approach and balanced number of student groups capable of tackling different types of work. Students should enter student name, number of groups, objective weights (optional), objective_measures(optional), students preferred to work with (optional), preference weight(optional), and preferences_weight_match(optional). Note that number of groups must be at least 2 and be a power of 2, i.e. 2, 4, 8, etc.

The program relies on the graph function of [GatorGrouper|https://github.com/GatorIncubator/gatorgrouper].
