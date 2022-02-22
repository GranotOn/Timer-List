import time
import sys
import os

argc = len(sys.argv)
SEPERATOR = ','

if argc != 2:
    sys.stdout.write("\r Usage: ./timer_list.py [List file name]")
    exit()


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


# Print iterations progress
# https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
def get_progress_bar(
    iteration,
    total,
    prefix='',
    suffix='',
    decimals=1,
    length=20,
    fill='█',
):
    percent = ("{0:." + str(decimals) + "f}").format(
        100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    return f'{prefix} |{bcolors.OKGREEN}{bar}{bcolors.ENDC}| {percent}% {suffix}'


def get_time_in_seconds(time_string):
    time_string_as_array = time_string.split(' ')
    time = time_string_as_array[0]
    time_type = time_string_as_array[1]
    if time_type == 's' or time_type == 'sec' or time_type == 'seconds' or time_type == 'second':
        return int(time)

    elif time_type == 'm' or time_type == 'min' or time_type == 'minute' or time_type == 'minutes':
        return int(time) * 60

    elif time_type == 'h' or time_type == 'hour' or time_type == 'hours':
        return int(time) * 60 * 60

    else:
        return 0


class Todo:
    def __init__(self, line) -> None:
        self.split_line = line.split(SEPERATOR)
        self.time = get_time_in_seconds(self.split_line[0])
        self.remaining_time = self.time
        self.task = self.split_line[1]
        self.complete = False

    def complete(self):
        self.complete = True

    def decrement(self):
        self.remaining_time = self.remaining_time - 1


def get_map_from_file(f):
    map = []
    for line in f.read().splitlines():
        if line[0] == '#':  # Ignore comments
            continue
        map.append(Todo(line))
    return map


try:
    f = open(sys.argv[1], "r")
    try:
        todo_list = get_map_from_file(f)
        current_task_idx = 0
        while current_task_idx < len(todo_list):
            os.system('cls' if os.name == 'nt' else 'clear')
            for i, todo in enumerate(todo_list):
                sys.stdout.write("\r")
                if i < current_task_idx:
                    sys.stdout.write(
                        f"\r{bcolors.OKGREEN}{todo.task}{bcolors.ENDC} - ✅\n")
                else:
                    is_current_task = i == current_task_idx
                    if todo.remaining_time <= 0:
                        current_task_idx = current_task_idx + 1
                        continue

                    text_color = bcolors.WARNING if is_current_task else bcolors.OKCYAN
                    remaining_time_as_str = time.strftime(
                        '%H:%M:%S', time.gmtime(todo.remaining_time))
                    sys.stdout.write(
                        f"\r{text_color}{todo.task}{bcolors.ENDC} - [{remaining_time_as_str}]"
                    )

                    if is_current_task:
                        iteration = todo.time - todo.remaining_time
                        sys.stdout.write(get_progress_bar(
                            iteration, todo.time))
                        todo.decrement()
                    sys.stdout.write("\n")
                sys.stdout.flush()
            time.sleep(1)
        sys.stdout("\rComplete! \n")
    finally:
        f.close()
except IOError:
    print("Couldn't open file provided: {}".format(sys.argv[1]))
    exit()
