from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import base64

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def activate_account_template(link):
    html = """
        <!DOCTYPE html>
        <html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <meta name="x-apple-disable-message-reformatting">
        <title></title>
        <!--[if mso]>
        <noscript>
            <xml>
            <o:OfficeDocumentSettings>
                <o:PixelsPerInch>96</o:PixelsPerInch>
            </o:OfficeDocumentSettings>
            </xml>
        </noscript>
        <![endif]-->
        <style>
            table, td, div, h1;
        </style>
        </head>
        <body style="margin:0;padding:0;">
        <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;background:#ffffff;">
            <tr>
            <td align="center" style="padding:0;">
                <table role="presentation" style="width:602px;border-collapse:collapse;border:1px solid #cccccc;border-spacing:0;text-align:left;">
                <tr>
                    <td align="center" style="padding:40px 0 30px 0;background:#eff7fd;">
                    <img src="" alt="" width="200" style="height:auto;display:block;" />
                    </td>
                </tr>
                <tr>
                    <td style="padding:36px 30px 42px 30px;">
                    <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                        <tr>
                        <td style="padding:0 0 36px 0;color:#153643;">
                            <h1 style="font-size:24px;margin:0 0 20px 0;font-family:Arial,sans-serif;">Welcome to DonkeyMailer</h1>
                            <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;">
                                To activate your account, click the button below
                            </p>
                            <br><br>
                            <p style="margin:0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;text-align:center;">
                            <a href="{link}" style="background-color:#82bfef;text-decoration:none;padding:10px;color:white;padding-left:50px;padding-right:50px;margin-top:10px;">Activate Account</a>
                            </p>
                        </td>
                        </tr>
                    </table>
                    </td>
                </tr>
                <tr>
                    <td style="padding:30px;background:#3b86bf;">
                    <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;font-size:9px;font-family:Arial,sans-serif;">
                        <tr>
                        <td style="padding:0;width:50%;" align="left">
                            <p style="margin:0;font-size:14px;line-height:16px;font-family:Arial,sans-serif;color:#ffffff;">
                            DonkeyMailer
                            </p>
                        </td>
                        <td style="padding:0;width:50%;" align="right">
                            <table role="presentation" style="border-collapse:collapse;border:0;border-spacing:0;">
                            <tr>
                            </tr>
                            </table>
                        </td>
                        </tr>
                    </table>
                    </td>
                </tr>
                </table>
            </td>
            </tr>
        </table>
        </body>
        </html>
        """.format(link=link)

    return html


def send_email_activate(email, link):
    message = Mail(
        from_email='codehub.company@gmail.com',
        to_emails=email,
        subject='Sending with Twilio SendGrid is Fun',
        html_content=activate_account_template(link))
    try:
        sg = SendGridAPIClient(
            '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')
        sg.send(message)
    except Exception as e:
        print(e.message)


def reset_password_template(link):
    html = """
        <!DOCTYPE html>
        <html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <meta name="x-apple-disable-message-reformatting">
        <title></title>
        <!--[if mso]>
        <noscript>
            <xml>
            <o:OfficeDocumentSettings>
                <o:PixelsPerInch>96</o:PixelsPerInch>
            </o:OfficeDocumentSettings>
            </xml>
        </noscript>
        <![endif]-->
        <style>
            table, td, div, h1;
        </style>
        </head>
        <body style="margin:0;padding:0;">
        <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;background:#ffffff;">
            <tr>
            <td align="center" style="padding:0;">
                <table role="presentation" style="width:602px;border-collapse:collapse;border:1px solid #cccccc;border-spacing:0;text-align:left;">
                <tr>
                    <td align="center" style="padding:40px 0 30px 0;background:#eff7fd;">
                    <img src="" alt="" width="200" style="height:auto;display:block;" />
                    </td>
                </tr>
                <tr>
                    <td style="padding:36px 30px 42px 30px;">
                    <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                        <tr>
                        <td style="padding:0 0 36px 0;color:#153643;">
                            <h1 style="font-size:24px;margin:0 0 20px 0;font-family:Arial,sans-serif;">Welcome to DonkeyMailer</h1>
                            <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;">
                                To reset your password, click the button below
                            </p>
                            <br><br>
                            <p style="margin:0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;text-align:center;">
                            <a href="{link}" style="background-color:#82bfef;text-decoration:none;padding:10px;color:white;padding-left:50px;padding-right:50px;margin-top:10px;">Reset Password</a>
                            </p>
                        </td>
                        </tr>
                    </table>
                    </td>
                </tr>
                <tr>
                    <td style="padding:30px;background:#3b86bf;">
                    <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;font-size:9px;font-family:Arial,sans-serif;">
                        <tr>
                        <td style="padding:0;width:50%;" align="left">
                            <p style="margin:0;font-size:14px;line-height:16px;font-family:Arial,sans-serif;color:#ffffff;">
                            DonkeyMailer
                            </p>
                        </td>
                        <td style="padding:0;width:50%;" align="right">
                            <table role="presentation" style="border-collapse:collapse;border:0;border-spacing:0;">
                            <tr>
                            </tr>
                            </table>
                        </td>
                        </tr>
                    </table>
                    </td>
                </tr>
                </table>
            </td>
            </tr>
        </table>
        </body>
        </html>
        """.format(link=link)

    return html


def send_email(email, link):
    message = Mail(
        from_email='codehub.company@gmail.com',
        to_emails=email,
        subject='Sending with Twilio SendGrid is Fun',
        html_content=reset_password_template(link))
    try:
        sg = SendGridAPIClient(
            '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')
        sg.send(message)
    except Exception as e:
        print(e.message)


def encrypt_email(email):
    message_bytes = email.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


def decrypt_email(encrypted_email):
    base64_bytes = encrypted_email.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message
