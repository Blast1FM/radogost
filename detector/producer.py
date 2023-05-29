import pika
import socket

#Class to send detection data off to the message queue

class MessageProducer():
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

class SocketVideoSendThing():
    #TODO implement everything lmao
    #Think of a way to get args, find an unused port, then just send
    #the fucking frames you eejit
    def __init__(self):
        self.HOST = "127.0.0.1"
        self.PORT = "7473"

    def send_shit(self):
        #this is just copy pasted do something with it lol
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)