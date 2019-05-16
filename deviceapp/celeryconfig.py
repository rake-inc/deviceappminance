enable_utc = True
timezone = "Asia/Kolkata"
# broker_url = 'pyamqp://'
task_serializer = 'json'
task_routes = {
    'device.tasks.send_mail': {'queue': 'emailer'},
}
broker_url = 'amqp://guest:guest@localhost:5672/'