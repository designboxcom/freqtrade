import cmd
import os
import psutil
import shutil
import subprocess
import sys
import termios
import threading
import time

CONFIG_DIR = os.path.join('user_data', 'config')
CONFIG_STD = os.path.join(CONFIG_DIR, 'config.json')
CONFIG_TELEGRAM = os.path.join(CONFIG_DIR, 'config-telegram-simu.json')
CONFIG_EXCHANGE = os.path.join(CONFIG_DIR,
                               'config-exchange-binance-notrade-for-simu.json')
LOG_DIR = os.path.join('user_data', 'log')
NBDAYS = 60
EPOCHS = 50
TICK = '1h'


def get_key():
    '''Wait for a single key and return it, no return key needed'''
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
    new[6][termios.VMIN] = 1
    new[6][termios.VTIME] = 0
    termios.tcsetattr(fd, termios.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 1)
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, old)
    return c


class Prompt(cmd.Cmd):
    '''Use Prompt().cmdloop()'''

    prompt = '> '
    queue_cmd = ['tsp']
    ft_cmd = ['docker-compose',
              'run',
              'freqtrade']
    ft_config = ['-c', CONFIG_STD,
                 '-c', CONFIG_TELEGRAM,
                 '-c', CONFIG_EXCHANGE]

    def __init__(self):
        super().__init__()
        self._debug_enabled = False
        self._check_prerequisites()
        self._hyperopts = []
        self._stop_event = threading.Event()

    def _check_prerequisites(self):
        '''check that docker and other elements are configured'''
        commands = ['docker', 'docker-compose', 'tsp']
        for command in commands:
            if shutil.which(command) is None:
                print(f'command not found: {command}')
                sys.exit(1)

        path_list = ['user_data', CONFIG_DIR, CONFIG_STD,
                     CONFIG_TELEGRAM, CONFIG_EXCHANGE, LOG_DIR]
        for path in path_list:
            if not os.path.exists(path):
                print(f'path does not exist: {path}')
                sys.exit(1)

        systemd = ['systemctl', 'status']
        systemd_services = ['docker']
        for service in systemd_services:
            if self._execute([*systemd, service]).returncode > 0:
                print(f'systemd service not started: {service}')
                sys.exit(1)

    def _cpu_load(self):
        while(not self._stop_event.wait(0.5)):
            print(f'cpu usage: {psutil.cpu_percent():6.2f}', end='\r')
            time.sleep(0.5)
        self._stop_event.clear()

    def _execute(self, cmd, show_cpu_usage=False):
        self._debug('execution command: ' + ' '.join(cmd))

        if show_cpu_usage:
            t = threading.Thread(target=self._cpu_load)
            t.start()

        output = subprocess.run(cmd, capture_output=True)

        if show_cpu_usage:
            self._stop_event.set()
            t.join(1)
            print(' '*30, end='\r')

        self._debug('stdout of command: ' + output.stdout.decode('UTF-8'))
        self._debug('stderr of command: ' + output.stderr.decode('UTF-8'))

        return output

    def _debug(self, msg):
        if self._debug_enabled:
            print('** DEBUG ** ' + msg)

    def do_version(self, arg):
        '''version of freqtrade, useful to test if docker is working'''
        command = ['docker-compose',
                   'run',
                   'freqtrade',
                   '-V']

        output = subprocess.run(command, capture_output=True)
        if output.returncode != 0:
            print('cannot launch freqtrade '
                  f'(return code: {output.returncode})')
            return False

        print(output.stdout.decode('UTF-8'))

    def do_toggle_debug(self, arg):
        '''Toggle printing debug messages on/off'''
        self._debug_enabled = not self._debug_enabled
        print(f'debug enabled is now {self._debug_enabled}')

    def complete_run_hyperopt(self, text, line, begidx, endidx):
        return [s for s in self._hyperopts if s.startswith(text)]

    def do_run_hyperopt(self, arg):
        if arg not in self._hyperopts:
            print(f'requested hyperopt class {arg} is not in the known '
                  f'valid list {", ".join(self._hyperopts)}')
            print('continue anyway? [y/N]')
            c = get_key()
            if c != b'y':
                print('doing nothing')
                return

        print('downloading data...')
        cmd = [*self.ft_cmd,
               'download-data',
               *self.ft_config,
               '-t', str(TICK),
               '--days', str(NBDAYS),
               '--exchange', 'binance']
        self._execute(cmd, show_cpu_usage=True)

        print('running hyperopt...')

        cmd = [*self.ft_cmd,
               'hyperopt',
               *self.ft_config,
               '--strategy', 'BBL3H2RSIStdStrategy',
               '--hyperopt', arg,
               '--logfile', os.path.join(LOG_DIR, arg + '.log'),
               '--hyperopt-loss', 'DefaultHyperOptLoss',
               '-e', str(EPOCHS)]
        self._execute(cmd, show_cpu_usage=True)

    def do_list_hyperopts(self, arg):
        cmd = [*self.ft_cmd, 'list-hyperopts']
        output = self._execute(cmd)

        raw_output = output.stdout.decode('UTF-8')
        for raw_line in raw_output.splitlines():
            if not raw_line.startswith('| '):
                continue
            line = raw_line.split('|')
            _, class_name, file_name, status, _ = [s.strip() for s in line]
            if class_name == 'name':
                continue
            if status == 'OK' and class_name not in self._hyperopts:
                self._hyperopts.append(class_name)
            print(f'{class_name} [{status}] in file {file_name}')

    def complete_test(self, text, line, begidx, endidx):
        keywords = ['yo', 'yo2', 'hello']
        return [i for i in keywords if i.startswith(text)]

    def do_test(self, arg):
        print(arg)

    def do_quit(self, arg):
        '''quit the program'''
        return True


if __name__ == "__main__":
    Prompt().cmdloop()
