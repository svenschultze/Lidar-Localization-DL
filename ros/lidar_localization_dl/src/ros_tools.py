import rospy

class Node():
    def __init__(self, name, topics={}):
        rospy.init_node(name)
        self.subscribers = []
        self.timed_subscriber_memory = {}
        self.pubs = {}
        for topic, msg_type in topics.items():
            self.pubs[topic] = rospy.Publisher(
                topic, msg_type
            )

    def spin(self):
        for sub in self.subscribers:
            rospy.Subscriber(
                sub["topic"], sub["type"], sub["callback"]
            )
        
        rospy.spin()

    def subscribe(self, topic, msg_type):
        def subscribe_decorator(callback):
            self.subscribers.append({
                "topic": topic, 
                "callback": callback,
                "type": msg_type
            })

        return subscribe_decorator

    def subscribe_timed(self, period, topic, msg_type):
        def timed_decorator(callback):
            self.timed_subscriber_memory[topic] = None

            self.subscribers.append({
                "topic": topic, 
                "callback": lambda msg: self.timed_subscriber_memory.update({topic: msg}),
                "type": msg_type
            })

            rospy.Timer(
                period=rospy.Duration(period),
                callback=lambda event: (
                    callback(self.timed_subscriber_memory[topic]) 
                    if self.timed_subscriber_memory[topic] 
                    else False
                )
            )

        return timed_decorator

    def timed(self, period):
        def timed_decorator(callback):
            rospy.Timer(
                period=rospy.Duration(period),
                callback=callback
            )

        return timed_decorator

    def publish(self, topic, msg):
        self.pubs[topic].publish(msg)

    def service_proxy(self, name, service_class):
        return rospy.ServiceProxy(name, service_class)
