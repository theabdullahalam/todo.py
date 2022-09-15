import os
import argparse
from functools import wraps
import readline

# settings
DEFAULT_FILE_NAME = "todo.txt"

# vars
parser = argparse.ArgumentParser()
current_filename = DEFAULT_FILE_NAME

# filter vars
project_filter = None
context_filter = None

# terminal colors
class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input(prompt)  # or raw_input in Python 2
   finally:
      readline.set_startup_hook()

def setup_args():
  global parser
  parser.add_argument("command", help="The command you wish to perform. Eg: ls, add, done, etc")
  parser.add_argument("task", help="The task number to act on", default=None, nargs='?')
  parser.add_argument("-f", "--file", help="Specify which file to use. Default: todo.txt in the current directory.")
  parser.add_argument("-p", "--project", help="Filter tasks by project (case sensitive).")
  parser.add_argument("-c", "--context", help="Filter tasks by context (case sensitive).")

def setup_file(filename):

  global current_filename

  if filename is None:
    filename = DEFAULT_FILE_NAME

  current_filename = filename

  if not os.path.exists(filename):
    with open(filename, "w"):
      pass


def add():
  task = input("> ")
  with open(current_filename, "r+") as cf:
    # .read() also moves cursor to end of file so writing acts like an append
    contents = cf.read()

    # only add newline if there are no tasks
    newline = "" if contents == "" else "\n"

    # add the task
    cf.write(f"{newline}{task}")

  ls()

def get_number_of_completed_tasks(tasks):
  count = 0
  for t in tasks:
    if t[:2] == "x ":
      count += 1

  return count

def catch_task_errors(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    try:
      return f(*args, **kwargs)
    except ValueError:
      print(header('ERROR', bcolors.FAIL))
      print("Enter task number in numeric form")
    except IndexError:
      print(header('ERROR', bcolors.FAIL))
      print(f"Task does not exist")
    except TypeError:
      print(header('ERROR', bcolors.FAIL))
      print(f"Did you forget to enter the task number?")
    except Exception as e:
      print(header('ERROR', bcolors.FAIL))
      print("An unknown error occured")

  return decorated

@catch_task_errors
def do(task_num):
  tasks = get_tasks()
  i = int(task_num)
  task = tasks[i]
  is_done = task[:2] == "x "

  if is_done:
    print(header('MARK TASK AS UNDONE?', bcolors.OKCYAN))
  else:
    print(header('MARK TASK AS DONE?', bcolors.OKCYAN))
  
  print_task(task, i)
  resp = input("\ny/n: ")

  if resp.lower() == "y":
    if len(task) > 3:
      if not is_done:
        tasks[i]  = f"x {task}"
        tasks.append(tasks.pop(i))
      else:
        tasks[i] = task[2:]
        tasks.insert(len(tasks) - get_number_of_completed_tasks(tasks) -1, tasks.pop(i))
    write_tasks(tasks)

  ls()

def get_tasks():
  with open(current_filename, "r") as cf:
    contents = cf.read()
    tasks = contents.split("\n")
    return tasks

def sort():
  tasks = get_tasks()
  tasks.sort()
  done_count = get_number_of_completed_tasks(tasks)

  edge_case_endings = []
  
  if done_count > 0:
    while tasks[-1][:2] != "x ":
      edge_case_endings.append(tasks.pop(-1))
      
  for t in edge_case_endings:
    tasks.insert(len(tasks) - done_count, t)

  write_tasks(tasks)

def write_tasks(tasks):
  with open(current_filename, 'w') as cf:
    for i in range(0, len(tasks)):
      newline = "\n" if i < len(tasks) -1 else ""
      cf.write(tasks[i] + newline)

def print_task(task, i=None):
  if i is not None:
    print(f"[{i}]\t{bcolors.BOLD}{task}{bcolors.ENDC}")
  else:
    print(f"{bcolors.BOLD}{task}{bcolors.ENDC}")

@catch_task_errors
def edit(task_num):
  tasks = get_tasks()
  i = int(task_num)
  task = tasks[i]
  old_task = task

  print(header('EDIT TASK', bcolors.WARNING))
  print(f'From: {old_task}')
  tasks[i] = rlinput("To:   ", old_task)
  new_task = tasks[i]

  print(header('CONFIRM UPDATE?', bcolors.OKCYAN))
  print(f'From: {old_task}')
  print(f'To:   {new_task}')
  resp = input('y/n:  ')

  if resp == "y":
    write_tasks(tasks)
    sort()
    print(header('TASK UPDATED', bcolors.WARNING))
  else:
    print(header('NO CHANGES MADE', bcolors.OKCYAN))

def ls():
  sort()
  tasks = get_tasks()
  print()
  print(header('TASK LIST'))

  if len(tasks[0]) > 0:
    done_header_printed = False
    filtered = []

    for i in range(0, len(tasks)):
      add = True
      project_pass = True
      context_pass = True
      
      if project_filter:
        project_pass = False
        if f"+{project_filter}" in tasks[i]:
          project_pass = True
      
      if context_filter:
        context_pass = False
        if f"@{context_filter}" in tasks[i]:
          context_pass = True

      if project_pass and context_pass:
        filtered.append({"i": i, "task": tasks[i]})

    for j in range(0, len(filtered)):
      task = filtered[j]["task"]
      i = filtered[j]["i"]

      if task[:2] == 'x ' and not done_header_printed:
        print(header('DONE', bcolors().OKGREEN))
        done_header_printed = True      

      print_task(task, i)

  print()

def header(title, color=bcolors.OKBLUE):
  text = f'{title} [{current_filename}]'
  lines = "".join(['-' for i in range(0, len(text))])
  return f'''{color}{bcolors.BOLD}{lines}
{text}
{lines}{bcolors.ENDC}'''

@catch_task_errors
def delete(task_num):
  tasks = get_tasks()
  i = int(task_num)
  task = tasks[i]

  print(header('PERMANENTLY DELETE TASK? (CANNOT BE UNDONE)', bcolors.WARNING))
  print(task)
  resp = input('y/n: ')

  if resp.lower() == 'y':
    tasks.pop(i)
    write_tasks(tasks)
    sort()
    print(header('TASK DELETED!'))
  


def main():

  # global vars
  global project_filter
  global context_filter
  
  # sort the files before proceeding
  sort()

  # setup argument parser
  setup_args()
  args = parser.parse_args()

  # create file if it doesn't exist
  # and update the current_filename variable
  setup_file(args.file)

  # add project filters
  project_filter = args.project
  context_filter = args.context

  if args.command == "add":
    add()
  elif args.command == "ls":
    ls()
  elif args.command == "do":
    do(args.task)
  elif args.command == "sort":
    ls()
  elif args.command == "edit":
    edit(args.task)
  elif args.command == "delete":
    delete(args.task)

main()