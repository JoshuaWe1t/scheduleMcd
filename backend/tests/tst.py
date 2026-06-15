foo = [{'code_employee': '400000', 'first_name': 'Nick', 'mon': 'Day off', 'tue': 'Day off', 'wed': 'Day off', 'thu': 'Day off', 
'fri': 'Day off', 'sat': 'Day off', 'sun': 'Day off', 'week_start_date': '2025-08-11', 'id': 102}, 
{'code_employee': '200000', 'first_name': 'Nil', 'mon': '07:00-16:00', 'tue': 'Day off', 'wed': 'Day off', 'thu': 'Day off', 'fri': 'Day off', 'sat': 'Day off', 'sun': '23:55-07:00', 'week_start_date': '2025-09-08', 'id': 17}]

count_day_off = list(foo[0].values()).count('Day off')
print(count_day_off)