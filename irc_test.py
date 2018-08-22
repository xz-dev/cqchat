import pydle

class MyClient(pydle.Client):
    """ This is a simple bot that will greet people as they join the channel. """

    def on_connect(self):
        super().on_connect()
        # Can't greet many people without joining a channel.
        self.join('#ZERO-test')

    def on_join(self, channel, user):
        super().on_join(channel, user)
        self.message(channel, 'Hey there, {user}!')

client = MyClient('ZERO')
client.connect('127.0.0.1')
client.on_join('#ZERO-test', 'ZERO')
#re = client.message('ZERO', 'hi')
#client.set_nickname('zzz')
#print(re)
#re = client.message('ZERO', 'hi')
client.handle_forever()

