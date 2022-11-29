# Pure Python todo.txt Implementation
An implementation of the non-nonsense todo.txt format in a single file python script with no third party libraries. I needed one to allow me to maintain a todo.txt per project, and here it this.

It isn't as exhaustive as the popular [todo.txt-cli,](https://github.com/todotxt/todo.txt-cli) (although it is a work in progress) but it gets the job done.

## Installation
Clone the project, add the the project folder to your path. Then run `todo.py` from anywhere.

## Usage
The commands below assume the project is in your `PATH`. If not, the commands will work with just `python todo.py`.

### Help
```bash
todo.py -h
```

### List Tasks
```bash
todo.py ls
```
```
--------------------
TASK LIST [todo.txt]
--------------------
```

### Add Task
```bash
todo.py add
```
```
> update readme
--------------------
TASK LIST [todo.txt]
--------------------
[0]     update readme
```