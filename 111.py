from datetime import datetime, timedelta

now = datetime.now()
target_datetime = now - timedelta(seconds=1)
target_datetime_str = target_datetime.strftime('%Y-%m-%d %H:%M:%S')

print(target_datetime_str)
print(now)