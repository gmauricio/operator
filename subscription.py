class SubscriptionManager():

    def __init__(self):
        self.subscribers = {}

    def subscribe(self, id, subscriber):
        self.subscribers.get(id, []).append(subscriber)