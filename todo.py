import os
import argparse

# settings
DEFAULT_FILE_NAME = "todo.txt"

# vars
parser = argparse.ArgumentParser()
current_filename = DEFAULT_FILE_NAME

# filter vars
project_filter = None

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

def setup_args():
  global parser
  parser.add_argument("command", help="The command you wish to perform. Eg: ls, add, done, etc")
  parser.add_argument("task", help="The task number to act on", default=None, nargs='?')
  parser.add_argument("-f", "--file", help="Specify which file to use. Default: todo.txt in the current directory.")
  parser.add_argument("-p", "--project", help="Filter tasks by project (case sensitive).")

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

def done(task_num):
  try:
    i = int(task_num)
    tasks = get_tasks()
    task = tasks[i]
    if len(task) > 3:
      if task[:2] != "x ":
        tasks[i]  = f"x {task}"
    write_tasks(tasks)
  except Exception as e:
    print(e)

def get_tasks():
  with open(current_filename, "r") as cf:
    contents = cf.read()
    tasks = contents.split("\n")
    return tasks

def write_tasks(tasks):
  with open(current_filename, 'w') as cf:
    for i in range(0, len(tasks)):
      newline = "\n" if i < len(tasks) -1 else ""
      cf.write(tasks[i] + newline)

def ls():

  def print_task(i, task):
    print(f"[{i}] {bcolors.BOLD}{task}{bcolors.ENDC}")

  tasks = get_tasks()
  print(header('TASK LIST'))

  if len(tasks[0]) > 0:
    for i in range(0, len(tasks)):
      task = tasks[i]

      if project_filter:
        if f'+{project_filter}' in task:
          print_task(i, task)
      else:
        print_task(i, task)

def header(title, color=bcolors.HEADER):
  text = f'{title} [{current_filename}]'
  lines = "".join(['-' for i in range(0, len(text))])
  return f'''{color}{bcolors.BOLD}{lines}
{text}
{lines}{bcolors.ENDC}'''

def main():

  print()

  # global vars
  global project_filter

  # setup argument parser
  setup_args()
  args = parser.parse_args()

  # create file if it doesn't exist
  setup_file(args.file)

  # add project filters
  project_filter = args.project

  if args.command == "add":
    add()
  elif args.command == "ls":
    ls()
  elif args.command == "done":
    done(args.task)

  print()


main()