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
DEFAULT_NBDAYS = 60
DEFAULT_EPOCHS = 50
DEFAULT_TICK = '1h'


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

    prompt = '>> '
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
        self._queue_enabled = True
        self._check_prerequisites()
        self._hyperopts = {}
        self._strategies = {}
        self._stop_event = threading.Event()
        self._last_output = None

    def _analyze_table(self, table, output_dict):
        '''Analyze the list table provided by ft for hyperopts or strategies'''
        for raw_line in table.splitlines():
            if not raw_line.startswith('| '):
                continue
            line = raw_line.split('|')
            _, class_name, filename, status, _ = [s.strip() for s in line]
            if class_name == 'name':
                continue
            if class_name not in output_dict.keys():
                output_dict[class_name] = {'status': status,
                                           'filename': filename}

    def _check_prerequisites(self):
        '''Check that docker and other elements are configured'''
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
        '''Basic cpu usage percentage, to use in a thread'''
        while(not self._stop_event.wait(0.5)):
            print(f'cpu usage: {psutil.cpu_percent():6.2f}', end='\r')
            time.sleep(0.5)
        self._stop_event.clear()

    def _debug(self, msg):
        '''Print message only when debug is enabled'''
        if self._debug_enabled:
            print('** DEBUG ** ' + msg)

    def _execute(self, raw_command,
                 queueable=False,
                 show_cpu_usage=False,
                 print_stderr=False,
                 stderr_only_on_nonzero_returncode=True,
                 print_stdout=False):
        '''Queue or execute immediately the command'''
        command = raw_command
        if queueable and self._queue_enabled:
            command = [*self.queue_cmd, *raw_command]
        self._debug('execution command: ' + ' '.join(command))

        if show_cpu_usage:
            t = threading.Thread(target=self._cpu_load)
            t.start()

        output = subprocess.run(command, capture_output=True)
        self._last_output = output

        if show_cpu_usage:
            self._stop_event.set()
            t.join(1)
            print(' '*30, end='\r')

        self._debug('stdout of command: ' + output.stdout.decode('UTF-8'))
        self._debug('stderr of command: ' + output.stderr.decode('UTF-8'))

        if print_stdout:
            print(output.stdout.decode('UTF-8')[:-1])

        if print_stderr:
            if not stderr_only_on_nonzero_returncode or \
              (stderr_only_on_nonzero_returncode and output.returncode != 0):
                print(output.stderr.decode('UTF-8')[:-1])

        return output

    def _input_number(self, msg, default=None):
        raw_number = input(msg)
        try:
            number = int(raw_number)
        except ValueError:
            number = default
        return number

    def do_version(self, arg):
        '''Version of freqtrade, useful to test if docker is working'''
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

    def do_toggle_queue(self, arg):
        '''Toggle queue mode or immediate'''
        self._queue_enabled = not self._queue_enabled
        print(f'queue enabled is now {self._queue_enabled}')

    def do_show_config(self, arg):
        '''Display the current state of the togglable elements'''
        print(f'debug enabled is {self._debug_enabled}')
        print(f'queue enabled is {self._queue_enabled}')

    def complete_run_hyperopt(self, text, line, begidx, endidx):
        return [s for s in self._hyperopts if s.startswith(text)]

    def do_run_hyperopt(self, arg):
        '''Queue or execute an hyperopt computation'''
        if arg not in self._hyperopts:
            print(f'requested hyperopt class {arg} is not in the known '
                  f'valid list {", ".join(self._hyperopts)}')
            print('continue anyway? [y/N]')
            c = get_key()
            if c != b'y':
                print('doing nothing')
                return

        tick = input(f'input tick ? [{DEFAULT_TICK}] ')
        if tick == '':
            tick = DEFAULT_TICK

        nbdays = self._input_number('nb of days for historical data? '
                                    f'[{DEFAULT_NBDAYS}]',
                                    default=DEFAULT_NBDAYS)

        epochs = self._input_number(f'number of epochs? [{DEFAULT_EPOCHS}]',
                                    default=DEFAULT_EPOCHS)

        print('downloading data...')
        command = [*self.ft_cmd,
                   'download-data',
                   *self.ft_config,
                   '-t', str(tick),
                   '--days', str(nbdays),
                   '--exchange', 'binance']
        self._execute(command, queueable=True, show_cpu_usage=True)

        print('running hyperopt...')
        command = [*self.ft_cmd,
                   'hyperopt',
                   *self.ft_config,
                   '--strategy', 'BBL3H2RSIStdStrategy',
                   '--hyperopt', arg,
                   '--logfile', os.path.join(LOG_DIR, arg + '.log'),
                   '--hyperopt-loss', 'DefaultHyperOptLoss',
                   '-e', str(epochs)]
        self._execute(command, queueable=True, show_cpu_usage=True)

    def do_list_hyperopts(self, arg):
        '''Retrieve hyperopts list from freqtrade'''
        command = [*self.ft_cmd, 'list-hyperopts']
        output = self._execute(command)
        raw_output = output.stdout.decode('UTF-8')
        self._analyze_table(raw_output, self._hyperopts)
        for h, hdata in self._hyperopts.items():
            print(f'[{hdata["status"]}] {h} in file {hdata["filename"]}')

    def do_run_backtesting(self, arg):
        '''Queue or execute a backtest'''
        if arg not in self._strategies:
            print(f'requested hyperopt class {arg} is not in the known '
                  f'valid list {", ".join(self._hyperopts)}')
            print('continue anyway? [y/N]')
            c = get_key()
            if c != b'y':
                print('doing nothing')
                return

    def do_list_strategies(self, arg):
        '''Retrieve strategies list from freqtrade'''
        command = [*self.ft_cmd, 'list-strategies']
        output = self._execute(command)
        raw_output = output.stdout.decode('UTF-8')
        self._analyze_table(raw_output, self._strategies)
        for s, sdata in self._strategies.items():
            print(f'[{sdata["status"]}] {s} in file {sdata["filename"]}')

    def complete_queue(self, text, line, begidx, endidx):
        keywords = ['list', 'clear', 'remove', 'movefirst', 'outputfile']
        return [k for k in keywords if k.startswith(text)]

    def do_queue(self, arg):
        '''Manage the task spooler queue'''

        def execute_on_valid_job_number(command_flag):
            raw_job_number = input('job number (return to ignore)? ')
            try:
                int(raw_job_number)
                command = [*self.queue_cmd, command_flag, raw_job_number]
                self._execute(command, print_stderr=True)
            except ValueError:
                print('doing nothing')
                return

        if arg == 'list':
            self._execute(self.queue_cmd, print_stdout=True)

        elif arg == 'clear':
            command = [*self.queue_cmd, '-C']
            self._execute(command)

        elif arg == 'remove':
            execute_on_valid_job_number('-r')

        elif arg == 'movefirst':
            execute_on_valid_job_number('-u')

        elif arg == 'outputfile':
            execute_on_valid_job_number('-o')

        else:
            print(f'unknown command: {arg}')
            return

    def do_last_output(self, arg):
        '''Display the output of the last command'''
        print(self._last_output)

    def do_quit(self, arg):
        '''Quit the program'''
        return True


if __name__ == "__main__":
    Prompt().cmdloop()
