enable_utc = True
timezone = "Asia/Kolkata"
task_serializer = 'json'
celery_routes = {
    'device.task.send_mail': {'queue': 'emailer'},
}
broker_url = 'amqp://guest:guest@localhost:5672/'
imports = ['device.task']