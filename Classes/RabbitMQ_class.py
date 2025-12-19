


'''

RabbitMQ - class
    To start:
        brew services start rabbitmq
    To stop
        brew services stop rabbitmq

'''


import pika

class RabbitMQ():

    def __init__(self):
        pass


    #   PRODUCER & CONSUMER
    #   ------------------------------------------------------------------------------------------------
    def createConnection(self, host='localhost', port=5672, username = 'guest', password='guest' ):
        '''
            producer & consumer
        '''
        credentials = pika.PlainCredentials(username, password) 
        parameters  = pika.ConnectionParameters( host=host, 
                                                 port = port, 
                                                 credentials=credentials)
        connection = pika.BlockingConnection(parameters=parameters)
        self.channel = connection.channel()
        # channel.exchange_declare(exchange = 'sensor_data', auto_delete=True)
        

    #   PRODUCER & CONSUMER
    #   ------------------------------------------------------------------------------------------------
    def declareExchange(self, name, exchange_type='fanout'):
        '''
            producer & consumer
        '''
        self.channel.exchange_declare(  exchange      = name, 
                                        exchange_type = exchange_type,
                                        auto_delete   = True )


    #   PRODUCER
    #   ------------------------------------------------------------------------------------------------
    def publish(self, exchange_name, body, routing_key=''):
        '''
            Producer side
        '''
        self.channel.basic_publish( exchange    = exchange_name, 
                                    routing_key = routing_key, 
                                    body        = body  )
    

    #   CONSUMER
    #   ------------------------------------------------------------------------------------------------
    def declareQueue(self, name='', exclusive=True ):
        '''
            Consumer side
        '''
        result = self.channel.queue_declare(  queue     = name, 
                                              exclusive = exclusive )
        
        return result
        '''
        queue_name = result.method.queue
        print(queue_name)
        '''


    #   CONSUMER
    #   ------------------------------------------------------------------------------------------------
    def bind_exchangeQueue(self, exchange_name, queue_name, routing_key=''):
        '''
            Consumer side
        '''
        self.channel.queue_bind(  exchange = exchange_name, 
                                  queue    = queue_name,
                                  routing_key =routing_key     )
    

    #   CONSUMER
    #   ------------------------------------------------------------------------------------------------
    def define_consume(self, queue_name, callback_function, auto_ack=True):
        '''
            Consumer side

            Example:
                def callback(body):
                    print(f" [x] {body}")
                    print()
        '''
            

        self.channel.basic_consume(  queue               = queue_name, 
                                     on_message_callback = callback_function, 
                                     auto_ack            = True         )
    
    
    #   CONSUMER
    #   ------------------------------------------------------------------------------------------------
    def start_consuming(self):
        '''
            Consumer side
        '''
        self.channel.start_consuming( )  

    def stop_consuming(self):
        '''
            Consumer side
        '''
        self.channel.stop_consuming()  






