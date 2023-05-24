import pika

#Class to send detection data off to the message queue

class Producer():
    #TODO implement evrything lol
    def __init__(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='detections')
    
    def send_message(self, message, routing_key:str):
        self.channel.basic_publish(
                    exchange='',
                    routing_key=routing_key,
                    body=message)

    def cleanup(self):
        self.connection.close()