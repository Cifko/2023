import datetime

now = 1095
start_level = 8699
keys = 9
t = datetime.datetime.today()
weekly = 100 + 200 + 250 + 300 + 500
daily = 150 * 3
till_next_season = datetime.timedelta(days=2, hours=10)
till_next_season = int(till_next_season.total_seconds()) // 60 // 60
while till_next_season >= 8:
    till_next_season -= 8
    now += daily // 3
print(start_level + now // 50)
level = start_level + now // 50
print(keys + level // 120 - start_level // 120)
print(now)
