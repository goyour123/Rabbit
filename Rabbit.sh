
repo='D:\Project\Chester'
output='D:\Project\Rabbit\Output'

# Remove output directory to ensure that files in it are correct.
#rm -r $output

# Create output directory for checkout solution.
mkdir -p $output

mod='Modified'
org='Original'

mkdir $output/$mod
mkdir $output/$org

cd $repo
#diff_file=$(git diff --name-only)
status_file=$(git status -s)

ifs_org=$IFS
IFS=$'\n'
for status_file_path in $status_file
  do
    status=${status_file_path% *}
    file_path=${status_file_path##* }

    # Extract the file name from file path
    file_name=${file_path##*/}

    # Extract the directory of file from file path
    if [ ${file_path%/*} == $file_name ]; then
      file_dir=""
    else
      file_dir=${file_path%/*}
    fi

    dir_to_del=""
    mkdir -p $output/$org/$file_dir
    if [ $status != $' D' ]; then
      mkdir -p $output/$mod/$file_dir

      if [ $status == $' M' ]; then
        echo "Modified" $file_path
      else
        echo "Added" $file_path
      fi
      # Copy modified/added file to output folder
      cp -r $file_path $output/$mod/$file_dir
    else
      # Decide the directory which should be delete/remain in repository
      dir_to_remain=$file_dir
      until [ -d $dir_to_remain ]
      do
        dir_to_del=$dir_to_remain
        if [ $dir_to_remain != ${dir_to_remain%/*} ]; then
          dir_to_remain=${dir_to_remain%/*}
        else
          break
        fi
      done
    fi

    if [ $status != $'??' ] && [ $status != $'A ' ]; then
      # Copy original file to output folder by revert the modified file to HEAD
      git checkout HEAD $repo/$file_path
      cp -r $file_path $output/$org/$file_dir
    fi

    # Copy modified file back to repo
    if [ $status == $' M' ]; then
      cp -r $output/$mod/$file_path $file_path
    fi

    # Remove deleted file
    if [ $status == $' D' ]; then
      if [ -n "$dir_to_del" ]; then
        echo "Deleted" $dir_to_del
        rm -r $dir_to_del
      else
        echo "Deleted" $file_path
        rm $repo/$file_path
      fi
    fi

  done
IFS=ifs_org

# Pause for the result
read -rsp $'\nPress any key to continue...\n' -n 1
