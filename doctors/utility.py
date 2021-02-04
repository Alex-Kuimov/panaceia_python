from django.core.mail import EmailMessage
from userprofile.models import User
from django.conf import settings


def decl_of_num(n, es):
  n = n % 100
  if n >= 11 and n <= 19:
      s = es[2]
  else:
      i = n % 10
      if i == 1:
          s = es[0]
      elif i in [2, 3, 4]:
          s = es[1]
      else:
          s = es[2]
  return s


def send_notify(to, msg, subject):
    _from = settings.DEFAULT_FROM_EMAIL

    email = EmailMessage(
        subject,
        msg,
        _from,
        to,
        headers={'Reply-To': _from}
    )

    email.content_subtype = 'html'
    email.send()


def get_email(id):
    emails = list()
    email = User.objects.get(pk=id).email
    emails.append(email)
    return emails
