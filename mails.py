from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def accountVarificationEmail(name,email,uuid,token):
    sg = SendGridAPIClient("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")
    html_content = """
    Hi {},
    Please click on the link to confirm your registration,
    http://127.0.0.1:8000/activate/{}/{}
    If you think, it's not you, then just ignore this email. 
    """.format(name, uuid, token)
    message = Mail(
        from_email='info@jamiamosque.co.ke',
        to_emails=email,
        subject='Activate your account.',
        html_content=html_content)
    try:
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


def wellcomeEmail(email,password):
    sg = SendGridAPIClient("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")
    html_content = """
    Hey ,
    Thank you for donation we have created account foy you to track your contributions
    you can login with email by entering following password {}
    """.format(password)
    message = Mail(
        from_email='info@jamiamosque.co.ke',
        to_emails=email,
        subject='Wellcome to Jamia',
        html_content=html_content)
    try:
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


def resetPasswordEmail(email, uuid, token):
    sg = SendGridAPIClient("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")
    html_content = """
    We received a request to reset the password for your account for this email address. To initiate the password reset 
    process for your account, click the link below.,
    http://127.0.0.1:8000/reset_password/{}/{}
    If you think, it's not you, then just ignore this email. 
    """.format(uuid, token)
    message = Mail(
        from_email='info@jamiamosque.co.ke',
        to_emails=email,
        subject='Reset Password',
        html_content=html_content)
    try:
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
