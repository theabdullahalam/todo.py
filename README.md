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

### Add Task
```bash
$ todo.py add

> update readme
--------------------
TASK LIST [todo.txt]
--------------------
[0]     update readme
```

### Edit Task
```bash
$ todo.py ls

--------------------
TASK LIST [todo.txt]
--------------------
[0]     add information about todotxt format +todopy
[1]     buy eggs @home
[2]     buy milk @home
[3]     update readme


$ todo.py edit 0

--------------------
EDIT TASK [todo.txt]
--------------------
From: add information about todotxt format +todopy
To:   add information about todo.txt format +todopy
--------------------------
CONFIRM UPDATE? [todo.txt]
--------------------------
From: add information about todotxt format +todopy
To:   add information about todo.txt format +todopy
y/n:  y
-----------------------
TASK UPDATED [todo.txt]
-----------------------
```

### Mark as done
```bash
$ todo.py do 0

-----------------------------
MARK TASK AS DONE? [todo.txt]
-----------------------------
[0]     update readme

y/n: y

--------------------
TASK LIST [todo.txt]
--------------------
---------------
DONE [todo.txt]
---------------
[0]     x update readme
```

### Filters
Use `-p` to filter by project, and `-c` to filter by context.
```bash
$ todo.py ls

--------------------
TASK LIST [todo.txt]
--------------------
[0]     add information about todotxt format +todopy
[1]     buy eggs @home
[2]     buy milk @home
[3]     update readme


$ todo.py ls -p todopy

--------------------
TASK LIST [todo.txt]
--------------------
[0]     add information about todotxt format +todopy


$ todo.py ls -c home

--------------------
TASK LIST [todo.txt]
--------------------
[1]     buy eggs @home
[2]     buy milk @home
```

