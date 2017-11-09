
repo='D:\Python\Python2.7\bios-toolbox'
output='D:\Python\Python3.5\Rabbit\Output'

# Remove output directory to ensure that files in it are correct.
#rm -r $output

# Create output directory for checkout solution.
mkdir -p $output

cd $repo
diff_file=$(git diff --name-only)

for file_path in $diff_file
  do
    file_name=${file_path##*/}
    if [ ${file_path%/*} == $file_name ]; then
      file_dir=""
    else
      file_dir=${file_path%/*}
    fi
    mkdir -p $output/$file_dir
    cp -R $file_path $output/$file_path
  done

# Pause for the result
#read -rsn 1 key
