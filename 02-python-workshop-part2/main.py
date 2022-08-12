import argparse
import subprocess


# returns dictionary of arguments
def parse_arguments():
    msg = 'Script that lists current directory.'
    parser = argparse.ArgumentParser(description=msg)

    parser.add_argument('--orderby', type=str, nargs='*',
                        help='Order by: n - name | '
                             't - last modified time | '
                             's - size')

    parser.add_argument('--f', action='store_true',
                        help='Lists only files.')
    parser.add_argument('--d', action='store_true',
                        help='Lists only directories.')

    parser.add_argument('--info', action='store_true',
                        help='Detailed view.')

    parser.add_argument('--depth', type=int, default=1,
                        help='Listing subfolders to specified depth.')

    parser.add_argument('--format', type=str, default='table',
                        help='Result format: table | json | xml')

    parser.add_argument('--filename', type=str, nargs=2,
                        help='Print result to file: FILANAME & o - overwrite |'
                             ' a - append to existing | c - create new'
                             'file')

    return parser.parse_args()


# function that executes shell commands (without starting the shell)
# returns a result list that contains files/folders with/without additional
# info
def command_builder(args_dict):
    ls_args = '-l'

    orderby_args = {
        'n': '',
        't': 't',
        's': 'S'
    }
    if args_dict.orderby:
        for criteria in args_dict.orderby:
            ls_args += orderby_args[criteria]

    # TODO: search by depth with find command with maxdepth argument

    if args_dict.d and not args_dict.f:
        ls_args += ' -d */'

    command = subprocess.Popen(('ls', ls_args), stdout=subprocess.PIPE)
    command.wait()

    if args_dict.f and not args_dict.d:
        # command_args += ' | grep -v "^d"'
        command = subprocess.Popen(['grep', '-v', "^d"],
                                   stdin=command.stdout,
                                   stdout=subprocess.PIPE)

    # showing detailed view by default, otherwise show only entity names
    if not args_dict.info:
        # command_args += ' | tr -s " " | cut -d" " -f9'
        command = subprocess.Popen(['tr', '-s', " "],
                                   stdin=command.stdout,
                                   stdout=subprocess.PIPE)
        command = subprocess.Popen(['cut', '-d ', '-f9'],
                                   stdin=command.stdout,
                                   stdout=subprocess.PIPE)

    # string result parsing
    result = command.communicate()[0].decode('UTF-8').split("\n")[1:-1]
    return result


# helper function for print_result(...)
# filename_and_mode is an array which consists out of 2 elements
def my_print(line, file):
    if file:
        file.write(str(line) + '\n')
    else:
        print(line)


# printing result in json | xml | table format
def print_result(result, args):
    file = None
    if args.filename:
        filename = args.filename[0]
        mode = args.filename[1]

        match mode:
            case 'o':
                file = open(filename, 'w')
                file.seek(0)
            case 'a':
                file = open(filename, 'a')
            case 'c':
                file = open(filename, 'x')

    match args.format:
        case 'table':
            if not args.info:
                my_print('Name', file)
            else:
                my_print('Permissions\tType\tOwner\tGroup\tSize\tTime\t'
                         '\tName', file)
            for line in result:
                my_print(line, file)

        case 'json':
            for line in result:
                fields = line.split()
                elem = {
                    'Permissions': fields[0],
                    'Type': fields[1],
                    'Owner': fields[2],
                    'Group': fields[3],
                    'Size': fields[4],
                    'Time': fields[5] + ' ' + fields[6] + ' ' + fields[7],
                    'Name': fields[8]
                }
                my_print(elem, file)

        case 'xml':
            pass
            # TODO: xml format output

    if file:
        file.close()


if __name__ == '__main__':
    # os.system('ls -l >> temp.txt')
    # with open("ping.txt", "r") as ping:
    #     print(ping.read())
    # os.system('rm temp.txt')

    args_dict = parse_arguments()
    result = command_builder(args_dict)
    print_result(result, args_dict)
