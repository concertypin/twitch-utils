class Bot:
    """
    A class to make a Twitch Bot.
    register method is used to add a trigger response.
    """

    def __init__(
        self,
        username: str,
        token: str,
        channel: str,
        callback,
        debug: bool = False,
    ):
        """
        username: Twitch username of the bot.
        token: Twitch token
        channel: Twitch channel
        callback: A function which called when a message is received. parameters: sender, message.
        if return is None, the message won't be sent. if return is a string, the message will be sent.
        debug: Set to True to print debug messages
        """
        import socket
        import threading

        self.username = username
        self.password = "oauth:" + token
        self.channel = channel
        self.debug = debug
        self.socket = socket.socket()
        self.socket.connect(("irc.twitch.tv", 6667))
        self.socket.send(bytes("PASS " + self.password + "\r\n", "utf-8"))
        self.socket.send(bytes("NICK " + self.username + "\r\n", "utf-8"))
        self.socket.send(bytes("JOIN #" + self.channel + "\r\n", "utf-8"))

        self.callback = callback

        self.responses = {}
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.start()

    def run(self):
        """
        This is the main loop of the bot.
        """
        import re

        while True:
            response = self.socket.recv(1024).decode("utf-8")
            if self.debug:
                print(response)
            if response == "":
                break
            if "PING" in response:
                self.socket.send(bytes("PONG\r\n", "utf-8"))
            if "PRIVMSG" in response:
                sender = re.search(r"\w+", response).group(0)
                message = re.sub(r"^\w+\W+", "", response)
                res = self.callback(sender, message)

                def send(msg):
                    # send message to channel
                    self.socket.send(
                        bytes("PRIVMSG #" + self.channel + " :" + msg + "\r\n", "utf-8")
                    )

                if res is not None:
                    send(res)
