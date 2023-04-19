# Grouper Playtest Scheduler

The situation: You have some number of game design groups (or artists groups, etc) and you want them to playtest each other's games (or critique each other's work). Add to that a number of faculty who will also be offering feedback in the mix. 

Playtesting is a vital part of the development of any game or product that requires user interaction. It involves testing the product with real users to get feedback and suggestions for improvement.

## Overview

This script is a scheduling tool for playtesting sessions in which a set of groups are matched to each other for playtesting, with each group having a chance to both host a playtest session and be a playtester in a session hosted by another group. This can be useful in game development or user experience research, where playtesting is an important part of the process.

## How it works

The script assigns each group to a session (i.e., a specific period in a day), during which they either host or participate in a playtesting session. It uses a "speed dating" algorithm in which each group hosts one session and participates as a playtester in another session. The algorithm ensures that no group is paired with another group it has already hosted or been a playtester with.

The script has parameters that can be adjusted, including the number of groups, the number of faculty members who will be participating, the number of days and periods in a day for which the scheduling will take place, and the bad luck threshold that determines when the script should terminate if it is unable to match groups due to limited options.

## Example

To run the script, you can simply execute the Python script in your command line or IDE. There are several parameters that can be adjusted within the script itself, such as the number of groups, faculty members, and days.

The script will output the schedule for each session, showing which group is hosting and which group or faculty are playtesting.

Here is an example of how to run the script:

```
python playtest_scheduler.py
```

Thanks to my pal and programming partner [ChatGPT](https://chat.openai.com/) (who also wrote this README).
