from celery import Celery, Task
# from .celeryconfig import app
app = Celery()

app.config_from_object('deviceapp.celeryconfig')
# Mailchimp feature
# from mailchimp import Mailchimp
# Emailer = Mailchimp(api_key)

class BaseTask(Task):
    def __call__(self, *args, **kwargs):
        print('TASK STARTING: {0.name}[{0.request.id}]'.format(self))
        return super(BaseTask, self).__call__(*args, **kwargs)
