# -*- coding: utf-8 -*-
"""
Time series analysis 
@QUAN YUAN

Notice：
1. any columns refer to time must named 'date'
2. date type datetime or string(%y-%m-%d)
"""

# import package
import pandas as pd
import numpy as np
import datetime as datetime
from dateutil.relativedelta import relativedelta
import LunarSolarConverter as ls


# Wind Terminal
from WindPy import *
w.start()
w.isconnected()

class Time_delay:
    '''
    功能：用于生成时间滞后的数据
    '''
    
    def __init__(self, data, freq, n, month = 1, start = None, end = None):
        
        # 用于生成时间模板的两个参数
        self.start = start
        self.end = end
        
        # 待处理的数据
        # 请注意：所有需要处理的数据只要有时间列，默认命名为'date'
        self.data = data
        
        # 用于时间滞后的参数
        # `freq`: 'M', 'D', 'W' 数据频率
        # `n` :   若freq为'M', 则表示延迟到下一个月的n号,(若此日期不是交易日，则延迟到下一个交易日)
        #         若freq为'D', 则表示延迟具体n天,(若延迟后的日期不是交易日，则延迟到下一个交易日)
        #         若freq为'W', 则表示延迟延迟到下周的周n,(若此日期不是交易日，则延迟到下一个交易日)
        # `month`: month参数是为了延迟多月设置的，若month=2表示延迟到2个月后，只有freq = 'M'时有效
        self.freq = freq
        self.n = n
        self.month = month
    
    def __get_time_template(self):
        '''
        功能：私有成员函数，从wind获取时间模板
        输入：需要处理数据的时间序列dataframe格式，注意时间列需要用'date'作为列名，或者直接输入，start，end
        输出：Dataframe格式的时间序列
        '''
        # 判断用户输入的是时间还是data
        if self.start == None and self.end == None:
            try:
                self.start = min(self.data['date'])
                self.end = max(self.data['date'])
            except:
                print 'imput start = ?, end = ? or just input your data'
        else:
            pass
        
        # 从Wind获取交易时间模板，命名为'date_tem'
        template = pd.DataFrame({'date_tem': w.tdays(self.start, self.end).Data[0]})
#        print template
        # 下面仅仅是为了让时间更好看......
        # 转化时间格式为string，去除小时数据，分钟，秒
        template['date_tem'] = template['date_tem'].map(lambda x: x.strftime("%Y-%m-%d"))
        # 将string转回datetime......
        template['date_tem'] = template['date_tem'].map(lambda x: datetime.strptime(x, "%Y-%m-%d"))
        return template
        
    def __judge_trade(self, data, template):
        '''
        功能：私有成员函数，判断时间是否是交易日，仅为为计算提高速度
        输入：由get_time_template生成的交易时间序列，data（dataframe）为需要处理的时间序列数据
        输出：返回更新后的data（在data的基础上加上一列judge_trade用来判别交易日）
        '''
        template_list = list(template['date_tem'])
        data['judge_trade'] = data['date'].map(lambda x: x in template_list)
        return data
    
    
    def __trade_delay(self, data, template):
        '''
        功能：私有成员函数，将每个时间都延后到交易日
        输入：template交易时间序列模板，data待处理数据
        输出：延后时间之后的数据
        '''
        
        # 生成判断judge_trade列，判断是否为交易日
        data = self.__judge_trade(data, template)
        
        # 做时间滞后操作
        
        # 只要数据中还存在False就继续循环剔除
        while len(data[data['judge_trade'] == False]) != 0:
            
            # 把judge_trade为False的行对应的时间滞后1天
            temp = data[data['judge_trade'] == False]['date'] + timedelta(1)
            data.loc[temp.index, 'date'] = temp
            
            # 再次判断是否有非交易日
            data = self.__judge_trade(data, template)
            
            # 仅仅为了方便观察程序运行中的问题
#            print "loop"
            print len(data[data['judge_trade'] == False])
#            print data[data['judge_trade'] == False]
            if len(data[data['judge_trade'] == False]) < 10:
                print data[data['judge_trade'] == False]
        data.index = range(len(data))
        return data
    
    def freq_delay(self):
        '''
        功能：根据不同的时间频率来做延时操作
        输入：data(dataframe), freq(str,'M', 'W', 'D'), n(int), month(default = 1),
        start(optional), end(optional)
        输出：延期之后的数据
        '''
        
        # 判断是否有正确的输入
        if type(self.n) != int or type(self.freq) != str:
            print "Please imput right type of input, any question use code `print freq_delay.__doc__`"
            return None
        else:
            pass
        
        template = self.__get_time_template()
        data = self.data
        
        # 时间滞后
        if self.freq == 'M':
            data['date'] = data['date'].map(lambda x: x + relativedelta(months = self.month) + relativedelta(day = self.n))
            data = self.__trade_delay(data, template)
            return data
        elif self.freq == 'W':
#            data['week_delay'] = data['date'].map(lambda x: timedelta(6 + self.n - x.weekday()))
#            data['date'] += data['week_delay']
            data['date'] += data['date'].map(lambda x: timedelta(6 + self.n - x.weekday()))
            data = self.__trade_delay(data, template)
        elif self.freq == 'D':
            data['date'] = data['date'].map(lambda x: x + relativedelta(days = self.n))
            data = self.__trade_delay(data, template)
        else:
            print "Please input right freq, freq = 'W' or 'M' or 'D', any question use code `print freq_delay.__doc__`"
            return None
        
        # 删去处理过程中多余的列
        try:
            del data['judge_trade']
        except:
            pass
        
        try:
            del data['date_tem']
        except:
            pass
                    
        return data
    
class TB:
    '''
    功能：将Excel转换为可以导入TB的Txt
    '''
    def __init__(self):
        # TXT中想要显示的列名
        # 时间列必须命名为date, 如果为datetime格式无要求，如果为string，则必须为Y-%m-%d格式
        # col必须是list
        pass
        
    def get_txt(self, data, col, name):
        '''
        功能：得到可用于可视化的TB数据
        '''
        data.columns = col
        
        # 如果时间是string格式, 变为datetime格式
        if type(data['date'].iloc[0]) == str:
            data['date'] = data['date'].map(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
        # 将datetime格式转为指定字符串格式
        data['date'] = data['date'].map(lambda x: x.strftime("%Y%m%d"))
        
        result = []
        time = []
        for i in range(len(data)):
            result.append(data.drop(['date'], axis = 1).iloc[i,:].to_dict())
            time.append(data['date'].iloc[i])
        
        if name == None:
            name = 'tb_result.txt'
        else:
            pass
        
        with open(name, 'w') as fp:
            for each in range(len(result)):
                fp.write("[%s]\n" % time[each])
                for p in result[each].items():
                    fp.write("%s=%s\n" % p)
                
class Scale:
    '''
    功能：用于对指定列做变换
    '''
    
    def __init__(self, data, col, scale, fun = None):
        # 需要变换的数据(dataframe)
        self.data = data
        # 需要变换的列(list,每个元素为string)
        self.col = col
        # 需要做的缩放(list,每个元素为num, 默认乘上scale做变换)
        self.scale = scale
        # 需要做的函数映射(list,每个元素为函数)，默认此参数为None
        # fun中每个函数为自定义函数, 只能包含一个参数x
        self.fun = fun
        
    def transform(self):
        '''
        功能：对data进行scale操作
        输入：data（dateframe格式数据，待处理），col（待处理字段）list格式，unit为scale值list格式
        输出：转换好的data
        '''
        
        data = self.data
        # 如果用户不进行函数变换
        if self.fun == None:
            if len(self.col) != len(self.scale):
                print 'the lenght of col and fun must be the same'
                return None
            else:
                for each_col, each_scale in zip(self.col, self.scale):
                    data[each_col] = data[each_col]*each_scale
                
        # 如果进行函数变换
        else:
            if len(self.col) != len(self.fun):
                print 'the lenght of col and fun must be the same'
                return None
            else:
                for each_col, each_fun in zip(self.col, self.fun):
                    data[each_col] = data[each_col].map(each_fun)
        return data
    
class Freq:
    '''
    功能：将数据补为日频率数据
    输入：
    用于生成时间模板的参数start, end, 
    需要处理的数据data, dataframege格式（注意时间列名为'date'）
    输出：日频时间序列数据
    '''
    def __init__(self, data, start = None, end = None):
        self.start = start
        self.end = end
        self.data = data
        
    def __get_time_template(self):
        '''
        功能：私有成员函数，从wind获取时间模板
        输入：需要处理数据的时间序列dataframe格式，注意时间列需要用'date'作为列名，或者直接输入，start，end
        输出：Dataframe格式的时间序列
        '''
        
        if self.start == None and self.end == None:
            try:
                self.start = min(self.data['date'])
                self.end = max(self.data['date'])
            except:
                print 'imput start = ?, end = ? or just input your data'
        else:
            pass
        
        # 从Wind获取交易时间模板，命名为'date_tem'
        template = pd.DataFrame({'date_tem': w.tdays(self.start, self.end).Data[0]})
#        print template
        # 下面仅仅是为了让时间更好看......
        # 转化时间格式为string，去除小时数据，分钟，秒
        template['date_tem'] = template['date_tem'].map(lambda x: x.strftime("%Y-%m-%d"))
        # 将string转回datetime......
        template['date_tem'] = template['date_tem'].map(lambda x: datetime.strptime(x, "%Y-%m-%d"))
        return template
    
    def to_day(self):
        '''
        功能：将数据整合成为日频率数据
        输入：时间序列模板dataframe格式（注意时间列名为'date_tem'）,需要处理的数据dataframege格式（注意时间列名为'date'）
        输出：日频时间序列数据
        '''
        # 获取时间列
        template = self.__get_time_template()
        # 变换index为后续concat做准备
        template.index = list(template['date_tem'])
        data = self.data
        data.index = list(data['date'])
        
        # 拼接时间模板列 
        data = pd.concat([template, data], axis=1, join_axes = [template.index])
        data = data.sort_values(by = 'date_tem', ascending = True)
        for i in range(len(data)):
            # 默认第一列是time
            if len(data.iloc[i][1:].dropna()) >= 1:
                # 保存数据用于拼接
                temp = data.iloc[i]
            else:
                try:
                    data.iloc[i] = temp
                except:
                    pass
                
        data['date'] = data.index
        data.index = range(len(data))
        del data['date_tem']
        return data
        
        
class Year_on_year:
    '''
    功能：生成同期处理之后的数据
    输入：
    data需要处理的数据（dataframe），时间列必须命名为'date', 
        且为datetime或string %y-%m-%d格式
    col为需要处理的列（list）
    freq数据频率（'M','Y'）
    cal算子
    输出：表中第一个数据相对表中其他数据均值的差异
    '''
    def __init__(self, data, col, n, freq, cal, save):
        # 需要处理的数据
        self.data = data
        # col为需要处理的列名(list)
        self.col = col
        # 默认所有列为同一时间频率，可选'year','month','week',''day
        self.freq = freq
        # 自定义处理算子，在cal_obj中有算子可选
        self.cal = cal
        # save表示rolling过程中是否需要对前n期数据做保留
        # 如向前rolling n年，前n年数据取前n年数据代替rolling值，避免损失大量数据
        # 可选为True或者False
        self.save = save
        # n表示向前rolling几年
        self.n = n
        
    def __selection(self, data, day, freq, year, n, save, min_year):
        '''
        功能：筛选出同期数据, 私有函数, 仅为提速
        data: 需要处理的数据
        day：第几行数据
        freq：数据同期频率
        year：当前数据属于第几年
        n：往前rolling计算n年
        save：是否减少数据损耗
        min_year：数据最小年限
        '''
        # 如果不进行数据保留
        if save == False:
            if year <= min_year + n - 1:
                return None
        elif save == True:
            if year <= min_year + n - 1:
                year = min_year + n - 1
        
        # 获取筛选条件, frequency表示代表第几个月或第几周或第几天
        freqency = data.iloc[day][freq]
        # 一级选择，选出同期限数据
        # 对53周的情况特别处理，用前5年52期的数据
        if freqency == 53:
            # 删去用52周索引的第一行，然后concat 53周的第一行
            # 选出当前的数据
            select_data1 = pd.DataFrame(data.iloc[day]).T
#            print select_data1
            select_data2 = data[data[freq] == 52].iloc[1:,:]
#            print select_data2
            select_data = pd.concat([select_data1, select_data2])
#            print select_data
        else:
            select_data = data[data[freq] == freqency]
            
        # 二级筛选，选出最近5年的数据
        # 生成一个时间df
        time_df = pd.DataFrame({'year': [year - i for i in range(n)]})
        # 使用merge方法取出特定年份的数据
        select_data = pd.merge(time_df, select_data, on = 'year', left_index = True)
        return select_data
    
    def corresponding(self):
        '''
        功能：生成去除季节性之后的数据
        输入：
        data需要处理的数据（dataframe）
        col为需要处理的列（list）
        freq数据频率
        cal算子
        输出：表中第一个数据相对表中其他数据均值的差异
        '''
        # 日期从大到小排序
        data = self.data.sort_values(by = 'date', ascending = False)
        
        # 判断data中date列的数据，若为tring则转换为datetime
        if type(data.iloc[0]['date']) == str:
            data['date'] = data['date'].map(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
        else:
            pass
        data.index = range(len(data))
        
        # 生成对应每一行的时间
        # 因为year是必须要的，所以不经过判断
        data['year'] = data['date'].map(lambda x: x.year)
        if self.freq == 'month':
            data['month'] = data['date'].map(lambda x: x.month)
        elif self.freq == 'week':
            data['week'] = data['date'].map(lambda x: x.week)
        elif self.freq == 'day':
            # day初始化
            data['day'] = 1
            # 生成每年第几天的数据
            year_list = list(set(data['year']))
            for i in year_list:
                temp = data[data['year'] == i]
                data.loc[temp.index, 'day'] = range(len(temp))[::-1]
        else:
            print 'please enter the right type of freq, year or month or week or day'
            return None
        
        # 找到数据最早的年份, 用于后续减少数据损失的处理
        min_year = min(data['year'])
        
        # 生成存储数据的列表
        collect = []
        for i in self.col:
            collect.append([])
        
        # 开始做同期变换
        # 对每一行数据
        for i in range(len(data)):
            # 找到对应的年
            year = data.iloc[i].year
            # 筛选出同期数据
            select_data = self.__selection(data, i, self.freq, year, self.n, self.save, min_year)
            # 如果超出了限制就不再做后续处理(主要为了处理不减少损失的情况)
            if len(select_data) == 0:
                break
            # 对每个需要处理的字段进行处理
            for j in range(len(self.col)):
                # 使用cal算子对同期数据进行处理
                collect[j].append(self.cal(select_data, i, self.col[j]))
        
        # 生成处理后的列
        result = data
        for i in range(len(self.col)):
            result['cal_'+ self.col[i]] = collect[i]
        result = result.dropna()
        
        # 只返回date和处理后的数据
        return result
#        return result[['date'] + ['cal_'+ self.col[i] for i in range(len(self.col))]]

class Rolling:
    '''
    功能1：目前数据依据前n年数据进行计算
    （输入：时间序列数据dataframe格式，时间列必须命名为date；Rolling天数；是否节约数据
      输出：时间序列数据的百分位数）
    功能2：按照top_bound和tail_bound来选取时间序列数据
    （输入：时间序列数据dataframe格式，时间列必须命名为date；Rolling天数；是否节约数据；bound上下界；
      输出：部分时间序列数据的百分位数）
    注意：每次只能处理一列数据
    '''
    
    def __init__(self, data, col, n, save, cal, top = None, tail = None):
        
        # 待处理的数据
        self.data = data
        # 哪一列需要处理string
        self.col = col
        # rolling的天数
        self.n = n
        # 是否节约数据
        self.save = save
        # 自定义算子
        self.cal = cal
        # 数据的上界
        self.top = top
        # 数据的下界
        self.tail = tail
        
    def rolling(self):
        '''
        使用算子计算，返回rolling处理后的数据
        '''

        data = self.data.sort_values(by = 'date', ascending = False)
        # 判断data中date列的数据，若为string则转换为datetime
        if type(data.iloc[0]['date']) == str:
            data['date'] = data['date'].map(lambda x: datetime.strptime(x, "%Y-%m-%d"))
        
        data.index = range(len(data))
        
        flag = 0
        result = []
        if self.save == True:
            for i in range(len(data)):
                
                if i + self.n >= len(data) and flag == 0:
                    # 如果超过了保留超过前的哪一个值
                    init = i
                    flag = 1
                
                # 选出待参考数据
                try:
                    select = data.iloc[init : (init + self.n), :]
                except:
                    select = data.iloc[i : (i + self.n), :]
                # 根据待参考数据计算
                result.append(self.cal(select, i, self.col))
                
        elif self.save == False:
            for i in range(len(data)):
                
#                if i + self.n > len(data):
#                    result.append(np.nan)
                
#                else:
                # 选出待参考数据
                select = data.iloc[i : (i + self.n), :]
                # 根据待参考数据计算
                result.append(self.cal(select, i, self.col))
                    
        # 将result进行处理
        result_return = pd.DataFrame({'date': data['date'], 'rolling_result': result})
        return result_return
    
    def truncated_rolling(self):
        
        if self.top == None or self.tail == None:
            print 'please input top and tail parameters'
            return None
        else:
            data = self.data.sort_values(by = 'date', ascending = False)
            # 判断data中date列的数据，若为string则转换为datetime
            if type(data.iloc[0]['date']) == str:
                data['date'] = data['date'].map(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
            
            data.index = range(len(data))
            
            flag = 0
            result = []
            if self.save == True:
                for i in range(len(data)):
                    
                    if i + self.n >= len(data) and flag == 0:
                        # 如果超过了保留超过前的哪一个值
                        init = i
                        flag = 1
                    
                    # 选出待参考数据
                    try:
                        select = data.iloc[init : (init + self.n), :]
                    except:
                        select = data.iloc[i : (i + self.n), :]
                    # 根据待参考数据计算
                    result.append(self.cal(select, i, self.col))
                    
            elif self.save == False:
                for i in range(len(data)):
                    
                    if i + self.n > len(data):
                        result.append(np.nan)
                    
                    else:
                        # 选出待参考数据
                        select = data.iloc[i : (i + self.n), :]
                        # 根据待参考数据计算
                        result.append(self.cal(select, i, self.col))
                        
            # 将result进行处理
            result_return = pd.DataFrame({'date': data['date'], 'rolling_result': result})
            result_return['truncated'] = np.where(result_return['rolling_result']>=self.top,'top',\
                                     np.where(result_return['rolling_result']<=self.tail, 'tail', np.nan))
            result_return = result_return.dropna()
            
            return result_return

class Time_convert:
    '''
    功能：将单个时间或者一个时间序列统一转化为datetime格式
    传入：单个或者时间序列格式数据, 可以为string或者datetime
    输出：单个或一个时间序列全为datetime格式
    '''
    def __init__(self, time):
        self.time = time
        
    def get(self):
        # 判断是单个时间还是一个时间序列
        # 如果格式是string
        
        type_date = type(datetime.strptime('2017-01-01', "%Y-%m-%d"))
        
        if type(self.time) == str:
            return datetime.strptime(self.time, "%Y-%m-%d")
        
        elif type(self.time) == type_date:
            return self.time
        
        # 如果格式为series
        elif type(self.time) == pd.core.series.Series:
            # 如果是由string组成的series
            if type(self.time.iloc[0]) == str:
                return self.time.map(lambda x: datetime.strptime(x, "%Y-%m-%d"))
            # 如果是由datetime组成的series
            elif type(self.time.iloc[0]) == pd._libs.tslib.Timestamp:
                return self.time            
        else:
            print 'plaese input the right type of data, string or series(string)'
            return None
        
class Lunar_solar:
    '''
    功能：实现阴历lunar(农历)和阳历solar(公历)之间的相互转换
    输入：时间数据Series，或者单个时间数据(可以为string或者datetime)
    输出：转换后的时间数据Series(datetime)，或者转换后的单个时间数据(datetime)
    '''
    def __init__(self, lunar = None, solar = None):
        self.lunar = lunar
        self.solar = solar
    
    # 将单个时间数据转化为字典格式year, month, week
    def __time_convert(time):
        return {'year': time.year, 'month': time.month, 'day': time.day}
    
    # 如果输入lunar可用
    def to_lunar(self):
        # 将数据转化为datetime
        Datetime1 = Time_convert(self.solar)
        date = Datetime1.get()
        
        # 定义转化器
        converter = ls.LunarSolarConverter.LunarSolarConverter()
        
        type_date = type(datetime.strptime('2017-01-01', "%Y-%m-%d"))
        
        if type(date) == type_date:
#            structure_time = self.__time_convert(date)
#            
#            year = structure_time['year']
#            month = structure_time['month']
#            day = structure_time['day']
            
            solar = ls.LunarSolarConverter.Solar(date.year, date.month, date.day)
            lunar = vars(converter.SolarToLunar(solar))
            str_lunar = str(lunar['lunarYear']) + '-' + str(lunar['lunarMonth']).zfill(2) \
                        + '-' + str(lunar['lunarDay']).zfill(2)
            Datetime2 = Time_convert(str_lunar)
            datetime_lunar = Datetime2.get()
            return datetime_lunar
            
        elif type(date) == pd.core.series.Series:
            structure_time = date.map(lambda x: \
                            vars(converter.SolarToLunar\
                            (ls.LunarSolarConverter.Solar(x.year, x.month, x.day))))
            structure_time = structure_time.map(lambda x: str(x['lunarYear']) + \
                                                '-' + str(x['lunarMonth']).zfill(2) \
                                                + '-' + str(x['lunarDay']).zfill(2))
            return structure_time
    