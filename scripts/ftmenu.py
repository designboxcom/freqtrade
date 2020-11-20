import cmd
import os
import psutil
import subprocess
import threading
import time

CONFIG_DIR = os.path.join('user_data', 'config')
CONFIG_STD = os.path.join(CONFIG_DIR, 'config.json')
CONFIG_TELEGRAM = os.path.join(CONFIG_DIR, 'config-telegram-simu.json')
CONFIG_EXCHANGE = os.path.join(CONFIG_DIR,
                               'config-exchange-binance-notrade-for-simu.json')
NBDAYS = 60
EPOCHS = 50
TICK = '1h'


def cpu_load():
    while(True):
        print(f'cpu usage: {psutil.cpu_percent()}', end='\r')
        time.sleep(0.5)


class Prompt(cmd.Cmd):
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
        self.hyperopts = []

    def _execute(self, cmd):
        # t = threading.Thread(target=cpu_load)
        # t.start()
        output = subprocess.run(cmd, capture_output=True)
        # t.join(0)
        return output

    def do_version(self, arg):
        '''version of freqtrade, useful to test if docker is working'''
        cmd = ['docker-compose',
               'run',
               'freqtrade',
               '-V']

        output = subprocess.run(cmd, capture_output=True)
        if output.returncode != 0:
            print('cannot launch freqtrade '
                  f'(return code: {output.returncode})')
            return False

        print(output.stdout.decode('UTF-8'))

    def complete_run_hyperopt(self, text, line, begidx, endidx):
        return [s for s in self.hyperopts if s.startswith(text)]

    def do_run_hyperopt(self, arg):
        cmd = [*self.ft_cmd,
               'download-data',
               *self.ft_config,
               '-t', str(TICK),
               '--days', str(NBDAYS),
               '--exchange', 'binance']
        output = self._execute(cmd)
        print(output)

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
            if status == 'OK' and class_name not in self.hyperopts:
                self.hyperopts.append(class_name)
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
