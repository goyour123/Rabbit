
repo='D:\Python\Python2.7\bios-toolbox'
output='D:\Python\Python3.5\Rabbit\Output'

# Remove output directory to ensure that files in it are correct.
#rm -r $output

# Create output directory for checkout solution.
mkdir -p $output

mod='Modified'
org='Original'

cd $repo
#diff_file=$(git diff --name-only)
status_file=$(git status -s)

ifs_org=$IFS
IFS=$'\n'
for status_file_path in $status_file
  do
    # Check if this file is a deleted file then skip copy to Modified folder
    status=${status_file_path% *}
    if [ $status == $' D' ]; then
      continue
    fi

    file_path=${status_file_path##* }

    # Extract the file name from file path
    file_name=${file_path##*/}

    # Extract the directory of file from file path
    if [ ${file_path%/*} == $file_name ]; then
      file_dir=""
    else
      file_dir=${file_path%/*}
    fi

    mkdir -p $output/$mod/$file_dir
    mkdir -p $output/$org/$file_dir

    cp -R $file_path $output/$mod/$file_path
  done
IFS=ifs_org

# Pause for the result
#read -rsn 1 key
