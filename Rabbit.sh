
repo='D:\Python\Python2.7\Pratice'
output='D:\Python\Python3.5\Rabbit\Output'

#rm -r $output

cd $repo
diff_file=$(git diff --name-only)

for file in $diff_file
  do
    cp -r $file $output\\$file
  done
