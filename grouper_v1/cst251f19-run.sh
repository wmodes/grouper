# reminders:
# Before you can run this, you will have to do a few things to the data:
#   * Remove the timestamp column (student identifiers have to be the first col)
#   * Join the name and email columns (:%s/,/ - /)
#   * Change the column counts below to match your data
#   * Remove " - hella" and " - meh" from the data (:%s/ - \(Meh\|Hella\)//g)
#   * Check for the unlikely event of a blank field (:%s/,,/,1,/g)

# number of groups (has to be a power of 2)
numgroups=8

file="data/cst251f19-2.csv"

# These are students who don't want to work together
# pref="data/cst251f19-pref.csv"
# prefweight=-100
# prefmatchweight=100

sched_weight="-10"
expert_weight="10"
commit_weight="-5"
lead_weight="5"
group_weight="-5"
bigpic_weight="5"
social_weight="3"
interest_weight="-3"

# sched_weight="0"
# expert_weight="0"
# commit_weight="0"
# lead_weight="0"
# group_weight="0"
# bigpic_weight="0"
# social_weight="0"
# interest_weight="0"

# make columns
# columns 1-16 schedule
for i in $(seq 1 16); do 
    measure+="diff "
    weight+="$sched_weight "
done
# columns 17-20 expertise
for i in $(seq 17 20); do 
    measure+="diff "
    weight+="$expert_weight "
done
# column 21 committment
measure+="diff "
weight+="$commit_weight "
# column 22 leadership role
measure+="diff "
weight+="$leader_weight "
# column 23 group org
measure+="diff "
weight+="$group_weight "
# column 24 big pic v detail
measure+="diff "
weight+="$bigpic_weight "
# column 25 social
measure+="diff "
weight+="$social_weight "
# columns 26-39 interests
for i in $(seq 26 39); do 
    measure+="diff "
    weight+="$interest_weight "
done

python gatorgrouper_cli.py --help

# echo "python gatorgrouper_cli.py"
# echo "--file $file"
# echo "--num-group $numgroups"
# echo "--method graph"
# echo "--objective-measures $measure"
# echo "--objective-weights $weight"

if [ "" == "$pref" ]
then
    command="python gatorgrouper_cli.py --file $file --num-group $numgroups --method graph --objective-measures $measure --objective-weights $weight"
else
    command="python gatorgrouper_cli.py --file $file --num-group $numgroups --method graph --objective-measures $measure --objective-weights $weight --preferences $pref --preferences-weight $prefweight --preferences-weight-match $prefmatchweight"
fi

echo "## COMMAND"
echo $command
echo "## GROUPING"
exec $command

# python gatorgrouper_cli.py --file $file --num-group $numgroups --method graph --objective-measures $measure --objective-weights $weight --preferences $pref --preferences-weight -100 --preferences-weight-match 100