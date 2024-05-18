example = 's 468400 102 0700-1600,1600-0000,0000-0000,0000-0000,1600-2300,0700-0000,0700-0000'

data = []

exmpl_list = example.split(sep=' ')

schedule_list = exmpl_list[-1].split(sep=',')

data = [exmpl_list[1], exmpl_list[1], schedule_list]

id, code, schedule = data

print(example, exmpl_list, sep='\n')
print(id, code, *schedule)

