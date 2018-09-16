import os
from django.core.mail import send_mail

os.environ['DJANGO_SETTINGS_MODULE'] = 'booksNet.settings'

if __name__ == '__main__':
    send_mail(
        'login code',
        'django test jun！',
        'junjun9772@126.com',
        ['876274128@qq.com'],
    )
