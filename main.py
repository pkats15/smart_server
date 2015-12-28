import os
import os.path
import subprocess
import time
import threading
from exceptions import ValueError, BaseException
from threading import Timer

#TODO Fix STOP



class Owner(object):
    owners = []

    def __init__(self, name):
        try:
            Owner.get_by_name(name)
            raise ValueError('{0} already exists'.format(name))
        except BaseException:
            pass
        self.name = name
        self.time = 0
        self.is_banned = False
        self.id = len(Owner.owners)
        self.updater = Owner.Updater(self)
        self.updater.start()
        Owner.owners.append(self)

    def add_time(self, minutes):
        self.time += minutes * 60

    def get_servers(self):
        return [server for server in Server.servers if server.owner == self]

    @staticmethod
    def get_by_name(name):
        owners = ([owner for owner in Owner.owners if owner.name == name])
        if len(owners) == 1:
            return owners[0]
        else:
            raise ValueError('There is no {0}'.format(name))
    class Updater(threading.Thread):
        # TODO Complete Timer
        start_time = 0

        def __init__(self, owner, group=None, target=None, name=None, *args, **kwargs):
            self.owner = owner
            super(Owner.Updater, self).__init__(group, target, name, args, kwargs)

        def run(self):
            while self.is_alive:
                for server in self.owner.get_servers():
                    if server.running and server.owner.time > 0:
                        server.owner.time -= 1
                for server in self.owner.get_servers():
                    if server.owner.time == 0 and server.running:
                        server.stop()
                cycle_time = (time.time() - Owner.Updater.start_time) % 1
                diff = time.time() - Owner.Updater.start_time
                time.sleep(1 - cycle_time)

        @staticmethod
        def start_time_counting():
            Owner.Updater.start_time = time.time()


class Server(object):
    servers = []
    DEFAULT_PATH = os.path.expanduser('~')
    thread = None

    def __init__(self, owner, name):
        self.owner = owner
        self.name = name
        self.id = int(len(Server.servers))
        self.running = False
        self.process = None
        Server.servers.append(self)

    def start(self):
        print 'starting server \'{0}\', id: {1}'.format(self.name,self.id)
        self.running = True

    def read_output(self):
        pass

    def write_input(self):
        pass

    def stop(self):
        self.running = False
        Timer(5, self.kill).start()

    def kill(self):
        print 'stopping server \'{0}\', id: {1}'.format(self.name,self.id)
        if self.process != None and self.process.return_code != None:
            self.process.kill()


class MinecraftServer(Server):
    MINECRAFT_PATH = os.path.join(Server.DEFAULT_PATH, 'minecraft')
    MINECRAFT_EXE = 'spigot.jar'

    def __init__(self, owner, name, port):
        self.port = port
        self.name = name
        self.process = None
        super(MinecraftServer, self).__init__(owner, name)

    def start(self):
        self.process = subprocess.Popen(['java', '-jar', MinecraftServer.MINECRAFT_EXE],
                                        cwd=MinecraftServer.MINECRAFT_PATH,
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        super(MinecraftServer, self).start()

    def stop(self):
        for line in self.process.communicate(input='stop')[0].splitlines():
            print line
            pass
        super(MinecraftServer, self).stop()

if __name__ == '__main__':
    Owner.Updater.start_time_counting()
    pk15 = Owner('pk15')
    pk15.add_time(10)
    mc = MinecraftServer(Owner.get_by_name('pk15'), 'MC Server',2345)
    srv = Server(Owner.get_by_name('pk15'), 'Another server')
    print(os.linesep)
    mc.start()
    srv.start()