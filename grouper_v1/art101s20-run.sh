# reminders:
# Before you can run this, you will have to do a few things to the data:
#   * Change the column counts below to match your data

# number of groups (has to be a power of 2)
numgroups=16

filebase="art101s20"

# the file containing the raw data
file="data/$filebase.csv"
# an internal file to prep the csv
fileprep="data/$filebase-prep.csv"

# These are students who don't want to work together
#	If no conflicts, use empty string.
#	If you have a pref file, add it here: data/cst236s20-pref.csv
#	Format is: Dominic Jones,Hannah McAllister,-100
pref=""
#pref="data/$filebase-pref.csv"

prefweight=-100
prefmatchweight=100

sched_weight="-10"      # match 10
expert_weight="10"      # diff 10
commit_weight="-15"      # match 5
lead_weight="5"         # diff 5
group_weight="-5"       # match 5
bigpic_weight="5"       # diff 5
social_weight="3"       # diff 3
interest_weight="-3"    # match 3

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

#
# Fix the data
#
# Remove the timestamp column (:%s/^[^,]*,//)
sed1="s/^[^,]*,//"
# Join the name and email columns (:%s/,/ - /)
sed2="s/,/ - /"
# Remove " - Hella" and " - Meh" from the data (:%s/ - \(Meh\|Hella\)//g)
sed3="s/ - Meh//g;s/ - Hella//g"
# Remove " - Best" and " - Worst" from the data (:%s/ - \(Best\|Worst\)//g))
sed4="s/ - Best//g;s/ - Worst//g"
# Remove " - Little" and " - Lots" from the data (:%s/ - \(Little\|Lots\)//g))
sed5="s/ - Little//g;s/ - Lots//g"
# Check for the unlikely event of blank fields (:%s/,,/,1,/g)
sed6="s/,,,,/,1,1,1,/g;s/,,,/,1,1,/g;s/,,/,1,/g"
echo "## PREPARING DATA"
sed "$sed1;$sed2;$sed3;$sed4;$sed5;$sed6;" $file > $fileprep

#python gatorgrouper_cli.py --help

# echo "python gatorgrouper_cli.py"
# echo "--file $fileprep:"
# echo "--num-group $numgroups"
# echo "--method graph"
# echo "--objective-measures $measure"
# echo "--objective-weights $weight"

if [ "" == "$pref" ]
then
    command="python gatorgrouper_cli.py --file $fileprep --num-group $numgroups --method graph --objective-measures $measure --objective-weights $weight"
else
    command="python gatorgrouper_cli.py --file $fileprep --num-group $numgroups --method graph --objective-measures $measure --objective-weights $weight --preferences $pref --preferences-weight $prefweight --preferences-weight-match $prefmatchweight"
fi

echo "## COMMAND"
echo $command
echo "## GROUPING"
exec $command

# python gatorgrouper_cli.py --file $fileprep --num-group $numgroups --method graph --objective-measures $measure --objective-weights $weight --preferences $pref --preferences-weight -100 --preferences-weight-match 100