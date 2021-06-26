from decouple import config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from celery.decorators import task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

@task(name='send_mail')
def send_mail(to):
	data = Mail(
		from_email = 'fagozie43@gmail.com',
		to_emails = to,
		subject = "Acknowledgment of Contact Form Receipt",
		html_content = f'<strong>Thank you for reaching out. We will get back to you shortly</strong>'
	)
	try:
		sg = SendGridAPIClient(config('SENDGRID_API_KEY'))
		resp = sg.send(data)
		logger.info("Sent contact email")
		return "Success"
	except Exception as e:
		logger.error(f'{e}')
		return "Failed"