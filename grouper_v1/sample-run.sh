python gatorgrouper_cli.py --help
echo "### Here is our sample data"
cat sample-data.csv
echo "### Some notes"
echo "Ideally, our final grouping should have the following features. Each group should:"
echo "  * have diverse expertise, i.e. mix of expert, novice and newbie (column 2)"
echo "  * group people by their schdule, i.e., 1's, 2's, and 3's together (column 3-5)"
echo "### GatorGrouper run"
python gatorgrouper_cli.py --file sample-data.csv --num-group 4 --method graph --objective-measures diff diff diff diff --objective-weights 10 -10 -10 -10
