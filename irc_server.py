#!/usr/bin/python

#
# 非常简单、黑客、简陋的IRC服务器。
#
# Todo:
#   - 为每条消息编码格式并使用ERR_NEEDMOREPARAMS进行回复
#   - 已启动时启动服务器无法正常工作。  PID文件未更改，不显示错误消息
#   - 如果最后一个用户离开，删除频道。
#   - Empty channels are left behind(留下空通道)
#   - No Op assigned when new channel is created.
#   - 用户可以/加入多次(不向频道添加更多内容，确实说'加入')
#   - PING超时
#   - 允许所有数字命令。
#   - 用户可以将命令发送到他们不在的频道(PART)
# Not Todo (不支持)
#   - 链接服务器


import sys
import optparse
import logging
import configparser
import os
import socketserver
import socket
import select
import re

SRV_NAME = "Hircd"
SRV_VERSION = "0.1"
SRV_WELCOME = "Welcome to %s v%s, the ugliest IRC server in the world." % (
    SRV_NAME, SRV_VERSION)

RPL_WELCOME = '001'
ERR_NOSUCHNICK = '401'
ERR_NOSUCHCHANNEL = '403'
ERR_CANNOTSENDTOCHAN = '404'
ERR_UNKNOWNCOMMAND = '421'
ERR_ERRONEUSNICKNAME = '432'
ERR_NICKNAMEINUSE = '433'
ERR_NEEDMOREPARAMS = '461'


class IRCError(Exception):
    """
    IRC命令处理程序抛出异常以通知客户端服务器/客户端错误。
    """

    def __init__(self, code, value):
        self.code = code
        self.value = value

    def __str__(self):
        return repr(self.value)


class IRCChannel(object):
    """
    表示IRC频道的对象。
    """

    def __init__(self, name, topic='No topic'):
        self.name = name
        self.topic_by = 'Unknown'
        self.topic = topic
        self.clients = set()


class IRCClient(socketserver.BaseRequestHandler):
    """
    IRC client connect and command handling. Client connection is handled by
    the `handle` method which sets up a two-way communication with the client.
    It then handles commands sent by the client by dispatching them to the
    handle_ methods.
    """
    """
    IRC客户端连接和命令处理。  客户端连接由。处理
    `handle`方法，用于建立与客户端的双向通信。
    然后它处理客户端发送的命令，将它们分配给
    handle_ 方法。
    """

    def __init__(self, request, client_address, server):
        self.user = None
        self.host = client_address  # Client's hostname / ip.
        self.realname = None        # Client's real name
        self.nick = None            # Client's currently registered nickname
        self.send_queue = []        # Messages to send to client (strings)
        self.channels = {}          # Channels the client is in

        socketserver.BaseRequestHandler.__init__(
            self, request, client_address, server)

    def handle(self):
        logging.info('Client connected: %s' % (self.client_ident(), ))

        while True:
            buf = ''
            ready_to_read, ready_to_write, in_error = select.select(
                [self.request], [], [], 0.1)

            # 将任何命令写入客户端
            while self.send_queue:
                msg = self.send_queue.pop(0)
                logging.debug('to %s: %s' % (self.client_ident(), msg))
                self.request.send(msg + '\n')

            # 查看客户端是否有任何命令。
            if len(ready_to_read) == 1 and ready_to_read[0] == self.request:
                data = self.request.recv(1024)

                if not data:
                    break
                elif len(data) > 0:
                    # 有数据。  处理它并将其转换为面向行的输入。
                    buf += str(data)

                    while buf.find("\n") != -1:
                        line, buf = buf.split("\n", 1)
                        line = line.rstrip()

                        response = ''
                        try:
                            logging.debug('from %s: %s' %
                                          (self.client_ident(), line))
                            if ' ' in line:
                                command, params = line.split(' ', 1)
                            else:
                                command = line
                                params = ''
                            handler = getattr(self, 'handle_%s' %
                                              (command.lower()), None)
                            if not handler:
                                logging.info(
                                    'No handler for command: %s. Full line: %s' % (command, line))
                                raise IRCError(
                                    ERR_UNKNOWNCOMMAND, '%s :Unknown command' % (command))
                            response = handler(params)
                        except AttributeError as e:
                            raise e
                            logging.error('%s' % (e))
                        except IRCError as e:
                            response = ':%s %s %s' % (
                                self.server.servername, e.code, e.value)
                            logging.error('%s' % (response))
                        except Exception as e:
                            response = ':%s ERROR %s' % (
                                self.server.servername, repr(e))
                            logging.error('%s' % (response))
                            raise

                        if response:
                            logging.debug('to %s: %s' %
                                          (self.client_ident(), response))
                            self.request.send(response + '\r\n')

        self.request.close()

    def handle_nick(self, params):
        """
        处理用户昵称和缺刻更改的初始设置。
        """
        nick = params

        # 有效的昵称？
        if re.search('[^a-zA-Z0-9\-\[\]\'`^{}_]', nick):
            raise IRCError(ERR_ERRONEUSNICKNAME, ':%s' % (nick))

        if not self.nick:
            # 新连接
            if nick in self.server.clients:
                # 其他人正在使用这个昵称
                raise IRCError(ERR_NICKNAMEINUSE, 'NICK :%s' % (nick))
            else:
                # 昵称可用，注册，发送欢迎和MOTD。
                self.nick = nick
                self.server.clients[nick] = self
                response = ':%s %s %s :%s' % (
                    self.server.servername, RPL_WELCOME, self.nick, SRV_WELCOME)
                self.send_queue.append(response)
                response = ':%s 376 %s :End of MOTD command.' % (
                    self.server.servername, self.nick)
                self.send_queue.append(response)
                return()
        else:
            if self.server.clients.get(nick, None) == self:
                # 已经注册用户
                return
            elif nick in self.server.clients:
                # 其他人正在使用这个昵称
                raise IRCError(ERR_NICKNAMEINUSE, 'NICK :%s' % (nick))
            else:
                # 昵称可用，改变昵称
                message = ':%s NICK :%s' % (self.client_ident(), nick)

                self.server.clients.pop(self.nick)
                prev_nick = self.nick
                self.nick = nick
                self.server.clients[self.nick] = self

                # 在被更换昵称所在的所有频道，向所有客户发送昵称更改通知
                for channel in list(self.channels.values()):
                    for client in channel.clients:
                        if client != self:  # 不发送给客户端本身。
                            client.send_queue.append(message)

                # 向客户端本身发送昵称更改通知
                return(message)

    def handle_user(self, params):
        """
        处理用于向服务器标识用户的USER命令。
        """
        if params.count(' ') < 3:
            raise IRCError(ERR_NEEDMOREPARAMS,
                           '%s :Not enough parameters' % (USER))

        user, mode, unused, realname = params.split(' ', 3)
        self.user = user
        self.mode = mode
        self.realname = realname
        return('')

    def handle_ping(self, params):
        """
        处理客户端PING请求以保持连接活动。
        """
        response = ':%s PONG :%s' % (
            self.server.servername, self.server.servername)
        return (response)

    def handle_join(self, params):
        """
        处理用户与频道的联接。有效的频道名称以＃、a-z、A-Z、0-9或_开始。
        """
        channel_names = params.split(' ', 1)[0]  # Ignore keys
        for channel_name in channel_names.split(','):
            r_channel_name = channel_name.strip()

            # 有效的频道名称？
            if not re.match('^#([a-zA-Z0-9_])+$', r_channel_name):
                raise IRCError(ERR_NOSUCHCHANNEL,
                               '%s :No such channel' % (r_channel_name))

            # 将用户添加到频道(如果不存在则创建新频道)
            channel = self.server.channels.setdefault(
                r_channel_name, IRCChannel(r_channel_name))
            channel.clients.add(self)

            # 将频道添加到用户的频道列表
            self.channels[channel.name] = channel

            # 发送主题
            response_join = ':%s TOPIC %s :%s' % (
                channel.topic_by, channel.name, channel.topic)
            self.send_queue.append(response_join)

            # 发送加入消息给频道中的每个人，包括你自己，并将用户的频道列表发回给用户。
            response_join = ':%s JOIN :%s' % (
                self.client_ident(), r_channel_name)
            for client in channel.clients:
                # if client != self: # FIXME: 根据规格，这应该是因为用户被包含在稍后发送的频道列表中。
                client.send_queue.append(response_join)

            nicks = [client.nick for client in channel.clients]
            response_userlist = ':%s 353 %s = %s :%s' % (
                self.server.servername, self.nick, channel.name, ' '.join(nicks))
            self.send_queue.append(response_userlist)

            response = ':%s 366 %s %s :End of /NAMES list' % (
                self.server.servername, self.nick, channel.name)
            self.send_queue.append(response)

    def handle_privmsg(self, params):
        """
        处理向用户或频道发送私人消息。
        """
        # FIXME: ERR_NEEDMOREPARAMS
        target, msg = params.split(' ', 1)

        message = ':%s PRIVMSG %s %s' % (self.client_ident(), target, msg)
        if target.startswith('#') or target.startswith('$'):
            # 消息到频道。检查通道是否存在。
            channel = self.server.channels.get(target)
            if channel:
                if not channel.name in self.channels:
                    # 用户不在频道中。
                    raise IRCError(ERR_CANNOTSENDTOCHAN,
                                   '%s :Cannot send to channel' % (channel.name))
                for client in channel.clients:
                    # Send message to all client in the channel, except the user himself.
                    # 发送消息给频道中除用户外的的所有客户端。
                    # TODO: 将此抽象为一个单独的方法，以便不是每个函数都有
                    # 检查用户是否在该频道中。
                    if client != self:
                        client.send_queue.append(message)
            else:
                raise IRCError(ERR_NOSUCHNICK, 'PRIVMSG :%s' % (target))
        else:
            # 发消息给用户
            client = self.server.clients.get(target, None)
            if client:
                client.send_queue.append(message)
            else:
                raise IRCError(ERR_NOSUCHNICK, 'PRIVMSG :%s' % (target))

    def handle_topic(self, params):
        """
        处理主题命令。
        """
        if ' ' in params:
            channel_name = params.split(' ', 1)[0]
            topic = params.split(' ', 1)[1].lstrip(':')
        else:
            channel_name = params
            topic = None

        channel = self.server.channels.get(channel_name)
        if not channel:
            raise IRCError(ERR_NOSUCHNICK, 'PRIVMSG :%s' % (target))
        if not channel.name in self.channels:
            # The user isn't in the channel.
            raise IRCError(ERR_CANNOTSENDTOCHAN,
                           '%s :Cannot send to channel' % (channel.name))

        if topic:
            channel.topic = topic
            channel.topic_by = self.nick
        message = ':%s TOPIC %s :%s' % (
            self.client_ident(), channel_name, channel.topic)
        return(message)

    def handle_part(self, params):
        """
        处理离开频道的用户。
        """
        for pchannel in params.split(','):
            if pchannel.strip() in self.server.channels:
                # 向用户所在的所有频道中的所有客户端发送消息，并从频道中删除用户。
                channel = self.server.channels.get(pchannel.strip())
                response = ':%s PART :%s' % (self.client_ident(), pchannel)
                if channel:
                    for client in channel.clients:
                        client.send_queue.append(response)
                channel.clients.remove(self)
                self.channels.pop(pchannel)
            else:
                response = ':%s 403 %s :%s' % (
                    self.server.servername, pchannel, pchannel)
                self.send_queue.append(response)

    def handle_quit(self, params):
        """
        使用QUIT命令与客户端断开连接。
        """
        response = ':%s QUIT :%s' % (self.client_ident(), params.lstrip(':'))
        # 向用户所在的所有频道中的所有客户端发送消息，并从频道中删除用户。
        for channel in list(self.channels.values()):
            for client in channel.clients:
                client.send_queue.append(response)
            channel.clients.remove(self)

    def handle_dump(self, params):
        """
        转储内部服务器信息以进行调试。
        """
        print("Clients:", self.server.clients)
        for client in list(self.server.clients.values()):
            print(" ", client)
            for channel in list(client.channels.values()):
                print("     ", channel.name)
        print("Channels:", self.server.channels)
        for channel in list(self.server.channels.values()):
            print(" ", channel.name, channel)
            for client in channel.clients:
                print("     ", client.nick, client)

    def client_ident(self):
        """
        Return the client identifier as included in many command replies.
        返回许多命令回复中包含的客户端标识符。
        """
        return('%s!%s@%s' % (self.nick, self.user, self.server.servername))

    def finish(self):
        """
        The client conection is finished. Do some cleanup to ensure that the
        client doesn't linger around in any channel or the client list, in case
        the client didn't properly close the connection with PART and QUIT.
        """
        logging.info('Client disconnected: %s' % (self.client_ident()))
        response = ':%s QUIT :EOF from client' % (self.client_ident())
        for channel in list(self.channels.values()):
            if self in channel.clients:
                # Client is gone without properly QUITing or PARTing this
                # channel.
                for client in channel.clients:
                    client.send_queue.append(response)
                channel.clients.remove(self)
        self.server.clients.pop(self.nick)
        logging.info('Connection finished: %s' % (self.client_ident()))

    def __repr__(self):
        """
        Return a user-readable description of the client
        """
        return('<%s %s!%s@%s (%s)>' % (
            self.__class__.__name__,
            self.nick,
            self.user,
            self.host[0],
            self.realname,
        )
        )


class IRCServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        self.servername = 'localhost'
        # Existing channels (IRCChannel instances) by channelname
        self.channels = {}
        # Connected clients (IRCClient instances) by nickname
        self.clients = {}
        socketserver.TCPServer.__init__(
            self, server_address, RequestHandlerClass)


class Daemon:
    """
    Daemonize the current process (detach it from the console).
    """

    def __init__(self):
        # Fork a child and end the parent (detach from parent)
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)  # End parent
        except OSError as e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" %
                             (e.errno, e.strerror))
            sys.exit(-2)

        # Change some defaults so the daemon doesn't tie up dirs, etc.
        os.setsid()
        os.umask(0)

        # Fork a child and end parent (so init now owns process)
        try:
            pid = os.fork()
            if pid > 0:
                try:
                    f = file('hircd.pid', 'w')
                    f.write(str(pid))
                    f.close()
                except IOError as e:
                    logging.error(e)
                    sys.stderr.write(repr(e))
                sys.exit(0)  # End parent
        except OSError as e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" %
                             (e.errno, e.strerror))
            sys.exit(-2)

        # Close STDIN, STDOUT and STDERR so we don't tie up the controlling
        # terminal
        for fd in (0, 1, 2):
            try:
                os.close(fd)
            except OSError:
                pass


if __name__ == "__main__":
    #
    # Parameter parsing
    #
    parser = optparse.OptionParser()
    parser.set_usage(sys.argv[0] + " [option]")

    parser.add_option("--start", dest="start", action="store_true",
                      default=True, help="Start hircd (default)")
    parser.add_option("--stop", dest="stop", action="store_true",
                      default=False, help="Stop hircd")
    parser.add_option("--restart", dest="restart",
                      action="store_true", default=False, help="Restart hircd")
    parser.add_option("-a", "--address", dest="listen_address",
                      action="store", default='127.0.0.1', help="IP to listen on")
    parser.add_option("-p", "--port", dest="listen_port",
                      action="store", default='6667', help="Port to listen on")
    parser.add_option("-V", "--verbose", dest="verbose", action="store_true",
                      default=False, help="Be verbose (show lots of output)")
    parser.add_option("-l", "--log-stdout", dest="log_stdout",
                      action="store_true", default=False, help="Also log to stdout")
    parser.add_option("-e", "--errors", dest="errors", action="store_true",
                      default=False, help="Do not intercept errors.")
    parser.add_option("-f", "--foreground", dest="foreground",
                      action="store_true", default=False, help="Do not go into daemon mode.")

    (options, args) = parser.parse_args()

    # Paths
    configfile = os.path.join(os.path.realpath(
        os.path.dirname(sys.argv[0])), 'hircd.ini')
    logfile = os.path.join(os.path.realpath(
        os.path.dirname(sys.argv[0])), 'hircd.log')

    #
    # Logging
    #
    if options.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.WARNING

    log = logging.basicConfig(
        level=loglevel,
        format='%(asctime)s:%(levelname)s:%(message)s',
        filename=logfile,
        filemode='a')

    #
    # Handle start/stop/restart commands.
    #
    if options.stop or options.restart:
        pid = None
        try:
            f = file('hircd.pid', 'r')
            pid = int(f.readline())
            f.close()
            os.unlink('hircd.pid')
        except ValueError as e:
            sys.stderr.write('Error in pid file `hircd.pid`. Aborting\n')
            sys.exit(-1)
        except IOError as e:
            pass

        if pid:
            os.kill(pid, 15)
        else:
            sys.stderr.write('hircd not running or no PID file found\n')

        if not options.restart:
            sys.exit(0)

    logging.info("Starting hircd")
    logging.debug("configfile = %s" % (configfile))
    logging.debug("logfile = %s" % (logfile))

    if options.log_stdout:
        console = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        console.setFormatter(formatter)
        console.setLevel(logging.DEBUG)
        logging.getLogger('').addHandler(console)

    if options.verbose:
        logging.info("We're being verbose")

    #
    # Go into daemon mode
    #
    if not options.foreground:
        Daemon()

    #
    # Start server
    #
    try:
        ircserver = IRCServer(
            (options.listen_address, int(options.listen_port)), IRCClient)
        logging.info('Starting hircd on %s:%s' %
                     (options.listen_address, options.listen_port))
        ircserver.serve_forever()
    except socket.error as e:
        logging.error(repr(e))
        sys.exit(-2)
