foo = '001'
print(foo, int(foo))

foo = ['0700-1600', '1600-0000', '0000-0000', '0000-0000', '1600-2300', '0700-0000', '0700-0000']

for ind, elm in enumerate(foo):
    if elm == '0000-0000':
        foo[ind] = 'Day off'

def exchange_day_off(schedule: list):
    """
    """
    for ind, elm in enumerate(schedule):
        if elm == '0000-0000':
            schedule[ind] = 'Day off'
    
    return schedule

print(exchange_day_off(foo))