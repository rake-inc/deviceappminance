enable_utc = True
timezone = "Asia/Kolkata"
task_serializer = 'json'
task_routes = {
    'device.task': {'queue': 'emailer'},
}
broker_url = 'amqp://guest:guest@rabbitmq:5672/'
imports = ['device.task']