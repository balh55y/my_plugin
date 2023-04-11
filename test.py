import random
ls = ["张浩翔","邓长成","尹启河","王伟宁","周正南","赵琳淞","姜明洋","韩怀煜"]
newls = random.sample(ls, 5)
print(''.join(['星期' + str(i+1) + "  "+ls[i] +"\n" for i in range(len(newls))]))
print(ls)

import datetime

today = datetime.date.today()
feb_27 = datetime.date(2023, 2, 27)
# breakpoint()
week_num = (today - feb_27).days // 7 +1

print(f"今天与2月27日相比是第{week_num}周")

import os
os.path.exists("G:/kf/my/my_plugin/值日表/一一一.txt")