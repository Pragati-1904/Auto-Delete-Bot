from decouple import config
from traceback import format_exc

try:
    BOT_TOKEN = config("BOT_TOKEN")
    REDISPASSWORD = config("REDISPASSWORD", default=None)
    REDISHOST = config("REDISHOST", default=None)
    REDISPORT = config("REDISPORT", default=None)
    REDISUSER = config("REDISUSER", default=None)
    ADMINS = [int(i) for i in config("ADMINS").split(" ")]
except BaseException:
    print(format_exc())
    exit()