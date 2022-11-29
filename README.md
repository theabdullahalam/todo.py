# Pure Python todo.txt
An implementation of the non-nonsense todo.txt format in a single file python script with no third party libraries. I needed one to allow me to maintain a todo.txt per project, and here it this.

It isn't as exhaustive as the popular [todo.txt-cli,](https://github.com/todotxt/todo.txt-cli) (although it is a work in progress) but it gets the job done.

## Installation
Clone the project, add the the project folder to your path. Then run `todo.py` from anywhere.

## Usage Cheatsheet
```bash
# help
todo.py -h

#list
todo.py ls

# add
todo.py add

# edit
todo.py edit <num>

# delete
todo.py delete <num>

# list, filtered by project
todo.py ls -p <project>

# list, filtered by context
todo.py ls -c <context>

# use a specific file; 
# example using ls
# can be used with any command
todo.py ls -f /path/to/file
```
