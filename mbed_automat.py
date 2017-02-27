import argparse

parser = argparse.ArgumentParser(description='Simple tool to copy files downloaded by mbed web compiler to your board')
parser.add_argument('-t', '--text', help='Test to look for in filename. pattern: *<yourText>*.bin', required=True)
parser.add_argument('-b', '--board', help='Board drive letter', required=True)
parser.add_argument('-s', '--source',
                    help='Location of downloaded firmwares. If not specified uses default system Downloads path.',
                    required=False)
parser.add_argument('-n', '--ntimes', help='Execute only once. Otherwise do it constantly', required=False)
args = vars(parser.parse_args())


def main():
    if not args['source']:
        from os import path

        newSource = {'source': path.join('D:/', 'Downloads')}
        args.update(newSource)

    ntimes = None
    if args['ntimes']:
        ntimes = int(args['ntimes'])

    filenameWildcard = '*' + args['text'] + '*.bin'

    print('Looking for files ' + filenameWildcard + ' at ' + args['source'] + ', then copying them to ' + args[
        'board'] + (' forever' if not args['ntimes'] else ' ' + str(ntimes) + ' times') + '.')

    from shutil import move
    from os import path
    from time import sleep
    executedTimes = 0
    beeper = Beeper()
    try:
        while not args['ntimes'] or executedTimes < ntimes:
            try:
                filename = findFile(args['source'], filenameWildcard)
                beeper.warning()
                if 'mbuino' in args['text'].lower():
                    print('mbuino detected. Deleting "firmware.bin"...', end='')
                    from os import remove
                    remove(path.join(args['board'], path.sep, 'firmware.bin'))
                    print('ok')
                    beeper.during()
                print('Moving file ' + filename)
                sourcePath = path.join(args['source'], filename)
                destPath = path.join(args['board'], path.sep)
                move(sourcePath, destPath)
                beeper.finished()
            except FileNotFoundError:
                print('No file matches ' + filenameWildcard)

            sleep(2)
            executedTimes = executedTimes + 1
    except KeyboardInterrupt:
        print('Exiting...')
        exit(0)


def findFile(where: str, filenameHint: str):
    from glob import glob
    from os import chdir
    chdir(where)
    for file in glob(filenameHint):
        return file
    raise FileNotFoundError


class Beeper():
    def __init__(self):
        from winsound import Beep
        self.Beep = Beep

    def during(self):
        self.Beep(1200, 320)

    def warning(self):
        self.Beep(600, 270)

    def finished(self):
        self.Beep(1950, 310)


if __name__ == '__main__':
    main()