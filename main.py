import sys
import os
import json
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from ui import MainWindow

CONFIG_FILE = "categories_config.json"

def ensure_config():
    """确保配置文件存在"""
    if os.path.exists(CONFIG_FILE):
        return
    
    default = {
        "支出": {
            "食品餐饮": {
                "三餐": "餐饮|饭店|餐厅|食堂|快餐|早餐|午餐|晚餐|夜宵|外卖|盒饭|便当",
                "零食": "零食|小吃|饼干|薯片|糖果|巧克力|坚果|果冻|辣条|薯条",
                "饮料": "奶茶|咖啡|果汁|可乐|雪碧|矿泉水|饮料|茶|牛奶|酸奶|豆浆"
            },
            "交通出行": {
                "公交地铁": "公交|地铁|轨道交通|公共交通|通",
                "打车": "滴滴|出租车|打车|网约车|代驾",
                "火车高铁": "火车|高铁|动车|铁路|城轨",
                "加油": "加油站|加油|汽油|柴油|中石化|中石油"
            }
        },
        "收入": {
            "工资": "工资|薪资|奖金|绩效|津贴|补贴",
            "红包": "红包|转账|收款"
        }
    }
    
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(default, f, ensure_ascii=False, indent=2)

def main():
    ensure_config()
    
    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei", 9))
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()