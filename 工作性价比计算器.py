import sys, math
import base64
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QComboBox, QVBoxLayout, QWidget, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QPalette, QColor, QIcon, QPixmap
from qfluentwidgets import TableWidget, PushButton, LineEdit, MessageBox
from icon import icon_bytes



class CalculateTableWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_data()
        self.initUI()

    def init_data(self):
        #各种系数或者计算用参数
        self.rate_daily_salary = 0
        self.rate_env = 0
        self.rate_env_work = 0
        self.rate_env_diversity =0 
        self.rate_env_coworker = 0
        self.rate_schedule = 0
        self.rate_education = 0
        self.rate_city = 0
        self.all_work_time = 0
        #其他参数
        self.yearly_salary = 0
        #工作环境
        self.env_work_hard = 0.85
        self.env_work_bad = 0.9
        self.env_work_nice = 1.05
        #异性环境
        self.env_diversity_bad = 0.98
        self.env_diversity_normal = 1
        self.env_diversity_nice = 1.02
        #同事环境
        self.env_coworker_bad = 0.98
        self.env_coworker_normal =1
        self.env_coworker_nice = 1.02
        #休息日系数
        self.monthly_twoDay_off = 0.8
        self.monthly_threeDay_off = 0.85
        self.weekends_oneDay_off = 0.9
        self.weekends_twoDays_off = 1
        self.weekends_moreThanTwodays_off = 1
        #上班时间
        self.checkin_time_eight = 0.95
        self.checkin_time_nine = 1
        self.checkin_time_ten = 1.05
        #加班时间
        self.work_overtime_awalys = 0.85
        self.work_overtime_rarely = 1
        self.work_overtime_sometime = 0.95
        #实际工作时长
        self.time_real_work = 0
        self.time_touchfish = 0
        self.time_commuting = 0
        #学历
        self.education_less_junior_college = 0.9
        self.education_Bachelor = 1
        self.education_Bachelor_niceCollege = 1.1
        self.education_master = 1.6
        self.education_master_niceCollege = 1.8
        self.education_doctor = 2.0
        self.education_doctor_niceCollege = 2.4
        #城市
        self.city_first_tire = 1.1
        self.city_almost_first_tire =1.05
        self.city_second_tire = 1.0
        self.city_third_tire = 0.9

        #字典
        self.data_dict = {
    "偏僻地区或郊区的工厂、工地、艰苦户外等": 0.85,
    "工厂、工地、艰苦户外等": 0.9,
    "普通工作环境": 1.0,
    "CBD、体制内等": 1.05,
    "周围没有好看异性": 0.98,
    "周围好看的异性不多不少": 1.0,
    "周围很多好看异性": 1.02,
    "周围脑残同事较多": 0.98,
    "周围基本上都是普通同事": 1.0,
    "周周围优秀同事较多": 1.02,
    "月休2日": 0.8,
    "月休3日及以下": 0.85,
    "单休": 0.9,
    "大小周": 0.95,
    "双休": 1.0,
    "双休以上": 1.0,
    "早上8点左右上班": 0.95,
    "早上9点左右上班": 1.0,
    "早上10点以后上班": 1.05,
    "经常加班": 0.85,
    "很少加班": 1.0,
    "偶尔加班": 0.95,
    "专科及以下": 0.9,
    "本科": 1.0,
    "名校本科": 1.1,
    "硕士": 1.6,
    "名校硕士": 1.8,
    "博士": 2.0,
    "名校博士": 2.4,
    "一线城市": 1.1,
    "准一线城市": 1.05,
    "二线城市": 1.0,
    "三线城市及以下": 0.9
}

    #根据输入汉字找到字典对应系数    
    def get_value_from_dict(self, input_str):
        if input_str in self.data_dict:
            return self.data_dict[input_str]
        else:
            return None

    #平均日薪单位为元(你又不是某爽),平均日薪系数=税前年薪(含各种奖金和各种补贴)/365
    def calculate_daily_salary(self, yearly_salary):
        return float(yearly_salary)/365
    
    #综合环境系数=1×工作环境系数×异性环境系数×同事环境系数
    def calculate_rate_env(self,env_work, env_diversity , env_coworker):
        return  1 * float(env_work) * float(env_diversity) * float(env_coworker)
    
    #综合作息系数=休息日系数×上班时间系数×下班后工作系数
    def calculate_schdule(self, dayoff_time, rate_checkin, rate_workOverTime):
        return float(dayoff_time) * float(rate_checkin) * float(rate_workOverTime)
    
    #25*(工作时长+0.5*通勤时长-0.5*模鱼时长)
    def calculate_all_time(self, work_time, time_commuting, touchfish_time):
       return  25*(float(work_time) + 0.5*float(time_commuting) + 0.5* float(touchfish_time))
    
    #性价比计算
    def final_calculate(self, rate_daily_salary, rate_env, rate_schedule, all_work_time, rate_education, rate_city):
        x= (rate_daily_salary * rate_env * rate_schedule) / (all_work_time * rate_education * rate_city)
        final_result = math.sqrt(x)
        return final_result

    #最后分级0.8凄惨，0.9惨，1.2略爽，1.5超爽
    def rank(self, final_result):
        so_bad = "韭菜"
        bad = "惨"
        normal = "一般"
        good = "爽"
        nice = "很爽"
        self.rank_result = ""
        if final_result <= 0.8:
            return so_bad
        elif  0.8 < final_result <= 0.9:
            return bad
        elif  0.9 < final_result <= 1.2:
            return normal   
        elif  1.2 < final_result <= 1.5:
            return normal                    
        elif  final_result >= 1.5:
            return nice


    def initUI(self):
        self.setWindowTitle('工作性价比计算器')
        self.setWindowIcon(QIcon(self.get_icon()))  # 设置图标
        self.resize(700,600)
        # 设置背景颜色为白色
        # 设置背景颜色为白色
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(249, 249, 249))
        self.setPalette(palette)

        # 创建表格
        self.table = TableWidget(self)
        self.table.setWordWrap(False)
        self.table.setRowCount(12)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['名称', '系数/标准', '备注'])

        #第一列标题列
        list_title = ["税前年薪","工作环境","工作异性环境","同事环境","工作时长","休息日","上班时间", "加班", "摸鱼时间", "通勤时间", "学历","城市"]
        list_note = []
        #填充第一列
        for row, value in enumerate(list_title):
            item = QTableWidgetItem(str(value))
            self.table.setItem(row, 0, item)
        
        #备注列内容
        #list_title = ["税前年薪","工作环境","工作异性环境","同事环境","工作时长","休息日","上班时间", "加班", "摸鱼时间", "通勤时间", "学历","城市"]
        list_note = ["含各种奖金与补贴/元","", "", "", "下班时间-上班时间/小时", "实际能休", "", "", "不干活时长+吃饭时长+午休时长", "", "", "准二线苏州、杭州、南京、武汉,成都等" ]
        #填充第一列
        for row, value in enumerate(list_note):
            item = QTableWidgetItem(str(value))
            self.table.setItem(row, 2, item)


        # 税前年薪
        self.yearly_salary_input = LineEdit()
        self.table.setCellWidget(0, 1, self.yearly_salary_input)

        # 工作环境
        self.work_environment_combobox = QComboBox()
        self.work_environment_combobox.addItems(["偏僻地区或郊区的工厂、工地、艰苦户外等", "工厂、工地、艰苦户外等", "普通工作环境", "CBD、体制内等"])
        self.table.setCellWidget(1, 1, self.work_environment_combobox)

        # 异性环境
        self.gender_diversity_combobox = QComboBox()
        self.gender_diversity_combobox.addItems(["周围没有好看异性", "周围好看的异性不多不少", "周围很多好看异性"])
        self.table.setCellWidget(2, 1, self.gender_diversity_combobox)

        # 同事环境
        self.coworker_environment_combobox = QComboBox()
        self.coworker_environment_combobox.addItems(["周围脑残同事较多", "周围基本上都是普通同事", "周周围优秀同事较多"])
        self.table.setCellWidget(3, 1, self.coworker_environment_combobox)

        # 工作时长
        self.actual_work_time_input = LineEdit()
        self.table.setCellWidget(4, 1, self.actual_work_time_input)

        # 休息日
        self.rest_day_combobox = QComboBox()
        self.rest_day_combobox.addItems(["月休2日", "月休3日及以下", "单休", "大小周", "双休", "双休以上"])
        self.table.setCellWidget(5, 1, self.rest_day_combobox)

        # 上班时间
        self.check_in_time_combobox = QComboBox()
        self.check_in_time_combobox.addItems(["早上8点左右上班", "早上9点左右上班", "早上10点以后上班"])
        self.table.setCellWidget(6, 1, self.check_in_time_combobox)

        # 加班
        self.overtime_work_combobox = QComboBox()
        self.overtime_work_combobox.addItems(["经常加班", "偶尔加班", "很少加班"])
        self.table.setCellWidget(7, 1, self.overtime_work_combobox)

        # 摸鱼时间
        self.slacking_time_input = LineEdit()
        self.table.setCellWidget(8, 1, self.slacking_time_input)

        # 通勤时间
        self.commuting_time_input = LineEdit()
        self.table.setCellWidget(9, 1, self.commuting_time_input)

        # 学历
        self.education_level_combobox = QComboBox()
        self.education_level_combobox.addItems(["专科及以下", "本科", "名校本科", "硕士", "名校硕士", "博士", "名校博士"])
        self.table.setCellWidget(10, 1, self.education_level_combobox)

        # 城市
        self.city_tier_combobox = QComboBox()
        self.city_tier_combobox.addItems(["三线城市及以下", "二线城市", "准一线城市", "一线城市"])
        self.table.setCellWidget(11, 1, self.city_tier_combobox)

        
        #单元格提示词
        #self.table.item(8, 2).setToolTip("123")

        # 添加输入框
        #self.age_input = QLineEdit()
        #self.table.setCellWidget(0, 2, self.age_input)

        #自适应列宽
        self.table.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
        #隐藏序号
        self.table.verticalHeader().setHidden(True)
        #表格不可编辑
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        #计算按钮
        self.button = PushButton("确认", self)
        self.button.clicked.connect(self.button_clicked)


        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    #计算按钮点击事件
    def button_clicked(self):
        #获取文本输入框信息
        self.yearly_salary = self.yearly_salary_input.text() # 获取税前年薪
        self.time_real_work = self.actual_work_time_input.text()# 获取工作时长
        self.time_touchfish = self.slacking_time_input.text()# 获取摸鱼时间    
        self.time_commuting = self.commuting_time_input.text()# 获取通勤时间

        #判断输入框是否为空
        if self.isBlank():
            self.showDialog("提示","表格不能填写为空或者非数字字符")
            return

        # 获取税前年薪
        rate_daily_salary = self.calculate_daily_salary(self.yearly_salary)
        

        # 获取工作环境
        self.work_environment = self.work_environment_combobox.currentText()
        self.rate_env_work = self.get_value_from_dict(self.work_environment)

        # 获取异性环境
        self.gender_diversity = self.gender_diversity_combobox.currentText()
        self.rate_env_diversity = self.get_value_from_dict(self.gender_diversity)

        # 获取同事环境
        self.coworker_environment = self.coworker_environment_combobox.currentText()
        self.rate_env_coworker = self.get_value_from_dict(self.coworker_environment)
        
        #工作环境系数计算
        rate_env = self.calculate_rate_env(self.rate_env_work,  self.rate_env_diversity , self.rate_env_coworker)



        # 获取休息日
        self.rest_day = self.rest_day_combobox.currentText()
        self.rate_rest_day = self.get_value_from_dict(self.rest_day)

        # 获取上班时间
        self.check_in_time = self.check_in_time_combobox.currentText()
        self.rate_check_in_time = self.get_value_from_dict(self.check_in_time)

        # 获取加班情况
        self.overtime_work = self.overtime_work_combobox.currentText()
        self.rate_overtime_work = self.get_value_from_dict(self.overtime_work)

        #作息系数计算
        rate_schedule = self.calculate_schdule(self.rate_rest_day, self.rate_check_in_time, self.rate_overtime_work)

        #实际工作时间计算
        all_work_time = self.calculate_all_time(self.time_real_work,  self.time_commuting, self.time_touchfish)
        
        # 获取学历
        self.education_level = self.education_level_combobox.currentText()
        self.rate_education = self.get_value_from_dict(self.education_level)



        # 获取城市
        self.city_tier = self.city_tier_combobox.currentText()
        self.rate_city = self.get_value_from_dict(self.city_tier)
        result = self.final_calculate(rate_daily_salary, rate_env, rate_schedule, all_work_time,  self.rate_education, self.rate_city)
        self.showDialog("结果","您的工作性价比是：\n"+ str(result)[0:7] + "\n"+self.rank(result))

    #消息弹窗        
    def showDialog(self, title, content):
        # w = MessageDialog(title, content, self)   # Win10 style message box
        w = MessageBox(title, content, self)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')
    
    #判断输入框是否为空
    def isBlank(self):
        variables= [self.yearly_salary, self.time_real_work, self.time_touchfish,  self.time_commuting]
        for var in variables:
            if var is None or var == "" or not var.isdigit():
                return True
        return False

    # 图标bytes转成pixmap格式
    def get_icon(self):
        icon_img = base64.b64decode(icon_bytes)  # 解码
        icon_pixmap = QPixmap()  # 新建QPixmap对象
        icon_pixmap.loadFromData(icon_img)  # 往QPixmap中写入数据
        return icon_pixmap


if __name__ == '__main__':
    app = QApplication(sys.argv)
    table_widget = CalculateTableWidget()
    table_widget.show()
    sys.exit(app.exec_())


####完整计算公式####
#根号下{平均日薪系数×综合环境系数×综合作息系数/25*(工作时长+0.5*通勤时长-0.5*模鱼时长)*学历系数*城市系数}
