class SubscriptionManager():

    def __init__(self):
        self.subscribers = []

    def subscribe(self, id, subject):
        self.subscribers.append(Subscriber(id, subject))

    def publish(self, message):
        for subscriber in self.subscribers:
            print "publishing message to subscriber:"+subscriber.id
            subscriber.subject.write_message(message)

    def get_all_subscribers(self):
        return self.subscribers.values()


class Subscriber():
    def __init__(self, id, subject):
        self.id = id
        self.subject = subject