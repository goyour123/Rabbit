
repo='D:\Python\Python2.7\Pratice'
output='D:\Python\Python3.5\Rabbit\Output'

# Remove output directory to ensure that files in it are correct.
#rm -r $output

# Create output directory for checkout solution.
mkdir -p $output

cd $repo
diff_file=$(git diff --name-only)

for file_path in $diff_file
  do
    ifs_org=$IFS
    IFS='/'
    for folder in $file_path
      do
        echo $folder
      done
    IFS=$ifs_org

    #cp -r $file_path $output\\$file_path
  done
