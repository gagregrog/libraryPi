from os import system


def title(*args):
    lines = []
    for i in range(len(args)):
        if str(args[i]).find('\n') >= 0:
            splitter = args[i].split('\n')
            for j in range(len(splitter)):
                lines.append(splitter[j])
        else:
            lines.append(args[i])
    system('clear')
    longest = 0
    for i in range(len(lines)):
        if len(str(lines[i])) > longest:
            longest = len(str(lines[i]))
    print('\n' + '*' * (longest + 8))
    print('*' + ' ' * (longest + 6) + '*')
    for i in range(len(lines)):
        if len(str(lines[i])) == longest:
            print('*   ' + lines[i] + '   *')
        elif longest % 2 == 0:
            if len(str(lines[i])) % 2 == 0:
                spaces = (longest + 6 - len(str(lines[i]))) // 2
                print('*' + ' ' * spaces + lines[i] + ' ' * spaces + '*')
            else:
                spaces = (longest + 6 - len(str(lines[i]))) // 2
                print('*' + ' ' * spaces + lines[i] + ' ' * (spaces + 1) + '*')
        else:
            if len(str(lines[i])) % 2 == 1:
                spaces = (longest + 6 - len(str(lines[i]))) // 2
                print('*' + ' ' * spaces + lines[i] + ' ' * spaces + '*')
            else:
                spaces = (longest + 6 - len(str(lines[i]))) // 2
                print('*' + ' ' * spaces + lines[i] + ' ' * (spaces + 1) + '*')
    print('*' + ' ' * (longest + 6) + '*')
    print('*' * (longest + 8) + '\n\n')