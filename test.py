import random
import datetime
import os
from pathlib import Path



dir_path = Path(__file__).parent
current_path = str(dir_path.absolute())



def is_week_file(周数):
    """检查给定路径下是否存在PNG文件"""
    if os.path.exists("current_path"+"值日表"+f"week_{周数}.png"):
        return True
    else:
        return False

today = datetime.date.today()
feb_27 = datetime.date(2023, 2, 27)
breakpoint()
week_num = (today - feb_27).days // 7 +1
print(is_week_file(week_num))