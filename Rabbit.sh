
repo='D:\Python\Python2.7\Pratice'
output='D:\Python\Python3.5\Rabbit\Output'

# Remove output directory to ensure that files in it are correct.
#rm -r $output

# Create output directory for checkout solution.


cd $repo
diff_file=$(git diff --name-only)

for file in $diff_file
  do
    cp -r $file $output\\$file
  done
