# Rabbit - Get code change for git

------
## GetCodeChange.py - Python script for getting code change of specific commit
### Required
#### GitPython
````
pip install gitpython
````
### Usage
#### config.json
````
{
    "source_path": "test_repo",
    "dest_path":   "test_target_folder",
    "sha":         "9abc45c798dbf5a1b1e2d1c3d7b62e648c597c3f"
}
````
source_path - The git local repository path.  
dest_path - The output path of the code change.  
sha - The commit SHA of the code change.  
#### Command
````
python GetCodeChange.py
````

## Rabbit.sh - Shell script for getting unstage code change
### Usage
````
Rabbit.sh [REPO_PATH] [OUTPUT_PATH]
````
[REPO_PATH] - The git local repository path.  
[OUTPUT_PATH] - The output path of the code change.

## GetCodeChangeGUI.py - GUI version of GetCodeChange.py
### Usage
````
python GetCodeChangeGUI.py
````