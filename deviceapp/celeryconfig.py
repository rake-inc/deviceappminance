enable_utc = True
timezone = "Asia/Kolkata"
task_serializer = 'json'
task_routes = {
    'device.task': {'queue': 'emailer'},
}
broker_url = 'amqp://guest:guest@172.21.0.1:5672/'
imports = ['device.task']