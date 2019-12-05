
import random
from django.core.mail import send_mail  # 这个是django自带的邮件发送方法
from django.core.validators import EmailValidator
#生成一个随机的字符串
def get_random_str(count):
    random_str = ''
    chars = 'fjdsalkfjdsklafjlkewjflkdjfsaflaeiw9ru'
    str_len = len(chars) - 1
    for i in range(count):
        randindex = random.randint(0, str_len)
        randomchar = chars[randindex]
        random_str +=randomchar
    return random_str

if __name__ == '__main__':
    print(get_random_str(10))