from deviceapp.app import app, BaseTask
from deviceapp.app import Emailer

@app.task(base=BaseTask)
def send_mail(email, number):
    # enable for mailchimp
    # mailchimp.campaigns.send(email_id)
    return "mail base been for the allocated device {} which is associated to the email address {}".format(number, email)
