# -*-  coding: UTF-8  -*-
# -*- -*- -*- -*- -*- -*-
# 2023/03    zhang9w0v5    created
# 2024/04    zhang9w0v5    fix bugs
# 2025/08    zhang9w0v5    尝试基于AI优化
# 2026/06    zhang9w0v5    skill化便于agent调用
# -*- -*- -*- -*- -*- -*-

DOCS = """
引言:

    河图洛书
    河图有10个数，1-10，阴阳相交，中心为5。其数字总和为55，河图东南西北中五方各两个数相差5。
    洛书有9个数，1-9，阴阳相交，中心为5。纵横斜各条线上三个数之和均为15，其数字总和为45与河图总和相差10。

    天地之数
    阳数，天数：1、3、5、7、9，之和为25。
    阴数，地数：2、4、6、8、10，之和为30。
    天地之数，阴阳相交，其数字总和为55，加上五行的5，共60。

    五行之数
    阳数：1，3，5，之和为9。
    阴数：2，4，之和为6。

    历法演进
    现代考古推测上古夏朝：有些部落是一年十个“月”的日历（太阳历），基于圆周数360，每“月”36日，与365.2422日相差5.2422日，长期使用不能吻合节气，无法准确指导农耕和计算年龄。
    现代学术推测上古神话：女娲用五色石补天，补的是欠缺的五天，360天十个月，五天用来过年和祭祀，共365天，但仍然有0.2422天的误差。
    现代学术推测上古神话：颛顼帝为整顿民神杂糅不可方物，下令“绝地天通”：断绝民间与上天的直接沟通，将 “观象授时”（观测天文、制定历法）的权力收归王室，由专职巫祝负责。
    现代学术推测上古神话：羲和浴日，十日一周，得十天干；常羲浴月，十二月一岁，得十二地支；常羲与羲和同为帝俊之妻，天干地支而后形成六十甲子纪时体系（纪年、纪月、纪日、纪时）。
    现代学术推测上古神话：夸父追日，是立杆追日影，确立冬至夏至，逐渐产生二十四节气。
    现代学术推测上古神话：后裔射日，十日射九日是指消灭不同历法，统一历法。
    现代现行公历闰年规则：公历闰年是补日差，平年365天，闰年366天，四年一闰，百年不闰，四百年再闰。
    现代现行农历闰月规则：农历也称阴阳历，结合了日月周期，农历闰月是补月差，19年设置7个闰月，弥补农历年（约354天）与太阳回归年（约365.24天）的天数差。
                          每个农历月以 “朔日”（月球位于太阳和地球之间，肉眼看不到月亮）为初一。
                          闰月放在不含 “中气”（二十四节气中双数的节气，如雨水、春分）的月份之后，该月重复上一个月的名称（如闰四月）。
                          二十四节气是农历的阳历成分，由太阳黄经位置确定，与月相无关。
    
    我们的农历，是阴阳历，是结合了太阳，月亮、地球运行规律的三维的星历。视觉上北斗七星绕北极星旋转的规律，从而定义了二十四宿，进一步完善了天体坐标体系。

    八卦易经（河图洛书、八卦，符号先出现，后人著易经）
    易经之始为伏羲所创先天八卦，后人称之为乾坤易，后有连山易和归藏易以及梅花易，相传由人类迁徙导致命名不同，是易经不同时期的名称。
    后天八卦由西周的周文王改造伏羲先天八卦而来（先天八卦主要表达地球时间，后天八卦纳入了地球空间与人文），代表着文明发生了巨大变化。
    先天八卦时期是禅位制，后天八卦时期是世袭封建制。

    易经是华人的人文之祖，我们的汉字和一些词汇均可追溯至易经。
    易经是为人处事之道，教化人们用发展的规律和不同的角度去思维。
    易经的核心是忧患意识，将忧患思维梳理清晰，避免毫无头绪的无效思维。
    遇事不决，则可以卜卦，通过卜卦来学习易经的思维，可厘清思维，化解无效的思维。
    综上，八八六十四卦实际就是抽象的索引和字典，偶尔查查字典非常利于教化自身。


金钱卦:

    金钱卦常用乾隆通宝(民间认为乾隆在位超60年，流通人气足)，或现代人民币，字为阳为数字[3]，花或背面为阴为数字[2]。
    金钱卦每爻由三个数字组成，共四种组合：三个阳[333]，三个阴[222]，两阳一阴[332]，两阴一阳[322]。
    金钱卦如阴阳难定，则重点参考错卦(又称对卦)，错卦刚好是阴阳爻对立的卦。
"""

# -*- -*- -*- -*- -*- -*-

import os
import re
import sys
import time
import random
import json
from datetime import datetime

# -*- -*- -*- -*- -*- -*-

def printfn(*args, **kwargs):
    """打印函数，用于全局控制print打印输出"""
    print(*args, **kwargs)

# -*- -*- -*- -*- -*- -*-


class Symbols(object):
    """
    符号类，包含八卦和六十四卦的符号常量
    """

    # 天地人三道
    THREE_DAO = {
        6: "天道",
        5: "天道",
        4: "人道",
        3: "人道",
        2: "地道",
        1: "地道"
    }

    # 爻位名称字典 (1-6 -> 爻位名称)
    YAO_POSITION_NAMES = {
        6: "上爻",
        5: "五爻",
        4: "四爻",
        3: "三爻",
        2: "二爻",
        1: "初爻"
    }

    # 阴阳爻位名称字典 (0: 阴爻, 1: 阳爻)
    YAO_YINYANG_POSITION_NAMES = {
        0: {
            6: "上六",
            5: "六五",
            4: "六四",
            3: "六三",
            2: "六二",
            1: "初六"
        },
        1: {
            6: "上九",
            5: "九五",
            4: "九四",
            3: "九三",
            2: "九二",
            1: "初九"
        }
    }

    # 八卦字典 (三爻二进制 -> 八卦符号，从初爻开始)
    TRIGRAMS = {
        "111": "☰:乾:天",  # 乾（初爻阳、二爻阳、三爻阳）
        "110": "☱:兑:泽",  # 兑（初爻阳、二爻阳、三爻阴）
        "101": "☲:离:火",  # 离（初爻阳、二爻阴、三爻阳）
        "100": "☳:震:雷",  # 震（初爻阳、二爻阴、三爻阴）
        "011": "☴:巽:风",  # 巽（初爻阴、二爻阳、三爻阳）
        "010": "☵:坎:水",  # 坎（初爻阴、二爻阳、三爻阴）
        "001": "☶:艮:山",  # 艮（初爻阴、二爻阴、三爻阳）
        "000": "☷:坤:地"   # 坤（初爻阴、二爻阴、三爻阴）
    }

    # 六十四卦字典 (上下卦组合 -> [卦象符号, 卦名])
    HEXAGRAMS = {
        # 四阳宫
        
        # 乾宫八卦:爻划三:西北:父
        "☰☰": "䷀:上乾下乾:乾为天",      # 本宫卦
        "☰☴": "䷫:上乾下巽:天风姤",      # 一世卦（初爻变）
        "☰☶": "䷠:上乾下艮:天山遁",      # 二世卦（初、二爻变）
        "☰☷": "䷋:上乾下坤:天地否",      # 三世卦（初、二、三爻变）
        "☴☷": "䷓:上巽下坤:风地观",      # 四世卦（初、二、三、四爻变）
        "☶☷": "䷖:上艮下坤:山地剥",      # 五世卦（初、二、三、四、五爻变）
        "☲☷": "䷢:上离下坤:火地晋",      # 游魂卦（四爻变回本宫）
        "☲☰": "䷍:上离下乾:火天大有",    # 归魂卦（下卦变回本宫）
        
        # 坎宫八卦:爻划五:正北:中男
        "☵☵": "䷜:上坎下坎:坎为水",      # 本宫卦
        "☵☱": "䷻:上坎下兑:水泽节",      # 一世卦（初爻变）
        "☵☳": "䷂:上坎下震:水雷屯",      # 二世卦（初、二爻变）
        "☵☲": "䷾:上坎下离:水火既济",    # 三世卦（初、二、三爻变）
        "☱☲": "䷰:上兑下离:泽火革",      # 四世卦（初、二、三、四爻变）
        "☳☲": "䷶:上震下离:雷火丰",      # 五世卦（初、二、三、四、五爻变）
        "☷☲": "䷣:上坤下离:地火明夷",    # 游魂卦（四爻变回本宫）
        "☷☵": "䷆:上坤下坎:地水师",      # 归魂卦（下卦变回本宫）
        
        # 艮宫八卦:爻划五:东南:少男
        "☶☶": "䷳:上艮下艮:艮为山",      # 本宫卦
        "☶☲": "䷕:上艮下离:山火贲",      # 一世卦（初爻变）
        "☶☰": "䷙:上艮下乾:山天大畜",    # 二世卦（初、二爻变）
        "☶☱": "䷨:上艮下兑:山泽损",      # 三世卦（初、二、三爻变）
        "☲☱": "䷥:上离下兑:火泽睽",      # 四世卦（初、二、三、四爻变）
        "☰☱": "䷉:上乾下兑:天泽履",      # 五世卦（初、二、三、四、五爻变）
        "☴☱": "䷼:上巽下兑:风泽中孚",    # 游魂卦（四爻变回本宫）
        "☴☶": "䷴:上巽下艮:风山渐",      # 归魂卦（下卦变回本宫）
        
        # 震宫八卦:爻划五:正东:长男
        "☳☳": "䷲:上震下震:震为雷",      # 本宫卦
        "☳☷": "䷏:上震下坤:雷地豫",      # 一世卦（初爻变）
        "☳☵": "䷧:上震下坎:雷水解",      # 二世卦（初、二爻变）
        "☳☴": "䷟:上震下巽:雷风恒",      # 三世卦（初、二、三爻变）
        "☷☴": "䷭:上坤下巽:地风升",      # 四世卦（初、二、三、四爻变）
        "☵☴": "䷯:上坎下巽:水风井",      # 五世卦（初、二、三、四、五爻变）
        "☱☴": "䷛:上兑下巽:泽风大过",    # 游魂卦（四爻变回本宫）
        "☱☳": "䷐:上兑下震:泽雷随",      # 归魂卦（下卦变回本宫）
        
        # 四阴宫
        
        # 巽宫八卦:爻划四:东南:长女
        "☴☴": "䷸:上巽下巽:巽为风",      # 本宫卦
        "☴☰": "䷈:上巽下乾:风天小畜",    # 一世卦（初爻变）
        "☴☲": "䷤:上巽下离:风火家人",    # 二世卦（初、二爻变）
        "☴☳": "䷩:上巽下震:风雷益",      # 三世卦（初、二、三爻变）
        "☰☳": "䷘:上乾下震:天雷无妄",    # 四世卦（初、二、三、四爻变）
        "☲☳": "䷔:上离下震:火雷噬嗑",    # 五世卦（初、二、三、四、五爻变）
        "☶☳": "䷚:上艮下震:山雷颐",      # 游魂卦（四爻变回本宫）
        "☶☴": "䷑:上艮下巽:山风蛊",      # 归魂卦（下卦变回本宫）
        
        # 离宫八卦:爻划四:正南:中女
        "☲☲": "䷝:上离下离:离为火",      # 本宫卦
        "☲☶": "䷷:上离下艮:火山旅",      # 一世卦（初爻变）
        "☲☴": "䷱:上离下巽:火风鼎",      # 二世卦（初、二爻变）
        "☲☵": "䷿:上离下坎:火水未济",    # 三世卦（初、二、三爻变）
        "☶☵": "䷃:上艮下坎:山水蒙",      # 四世卦（初、二、三、四爻变）
        "☴☵": "䷺:上巽下坎:风水涣",      # 五世卦（初、二、三、四、五爻变）
        "☰☵": "䷅:上乾下坎:天水讼",      # 游魂卦（四爻变回本宫）
        "☰☲": "䷌:上乾下离:天火同人",    # 归魂卦（下卦变回本宫）
        
        # 坤宫八卦:爻划六:西南:母
        "☷☷": "䷁:上坤下坤:坤为地",      # 本宫卦
        "☷☳": "䷗:上坤下震:地雷复",      # 一世卦（初爻变）
        "☷☱": "䷒:上坤下兑:地泽临",      # 二世卦（初、二爻变）
        "☷☰": "䷊:上坤下乾:地天泰",      # 三世卦（初、二、三爻变）
        "☳☰": "䷡:上震下乾:雷天大壮",    # 四世卦（初、二、三、四爻变）
        "☱☰": "䷪:上兑下乾:泽天夬",      # 五世卦（初、二、三、四、五爻变）
        "☵☰": "䷄:上坎下乾:水天需",      # 游魂卦（四爻变回本宫）
        "☵☷": "䷇:上坎下坤:水地比",      # 归魂卦（下卦变回本宫）
        
        # 兑宫八卦:爻划四:正西:少女
        "☱☱": "䷹:上兑下兑:兑为泽",      # 本宫卦
        "☱☵": "䷮:上兑下坎:泽水困",      # 一世卦（初爻变）
        "☱☷": "䷬:上兑下坤:泽地萃",      # 二世卦（初、二爻变）
        "☱☶": "䷞:上兑下艮:泽山咸",      # 三世卦（初、二、三爻变）
        "☵☶": "䷦:上坎下艮:水山蹇",      # 四世卦（初、二、三、四爻变）
        "☷☶": "䷎:上坤下艮:地山谦",      # 五世卦（初、二、三、四、五爻变）
        "☳☶": "䷽:上震下艮:雷山小过",    # 游魂卦（四爻变回本宫）
        "☳☱": "䷵:上震下兑:雷泽归妹"     # 归魂卦（下卦变回本宫）
    }


class SixYao(object):
    """
    六爻类，用于实现六爻相关的功能
    """

    @classmethod
    def auto_six_yao(cls):
        """
        生成六爻（金钱卦）
        返回: 六爻列表，每爻结构为 [[3,3,3], 9]
        """
        # -*- -*- -*-
        def auto_one_yao(i):
            """
            生成一爻的数据（金钱卦）
            返回: [[投掷结果], 爻值]
            投掷结果: 3次投掷，随机值为 [0, 2, 0, 3]
            爻值: 6（老阴）、7（少阳）、8（少阴）、9（老阳）
            """
            base_symbols = [0, 2, 0, 3]  # 0号位为无效, 1阳为3, 2阴为2.
            for _ in range(99):
                one_yao = [random.choice(base_symbols) for _ in range(3)]
                total = sum(one_yao)
                if 0 not in one_yao:
                    printfn(f"摇掷 {[one_yao, total]} 有效")
                    return [one_yao, total]
                printfn(f"摇掷 {[one_yao, total]} 无效 -重掷")
                time.sleep(0.05)  # 每次重新摇掷间隔0.05秒
            raise Exception("无效摇掷了99次，如需重新摇掷，请重新运行程序。")
        # -*- -*- -*-
        six_yao = [auto_one_yao(i) for i in range(1, 7)]
        # -*- -*- -*-
        return six_yao

    @classmethod
    def type_six_yao(cls):
        """
        从命令行输入六爻数据
        返回: 六爻列表，每爻结构为 [[投掷结果], 爻值]
        """
        printfn("\n手动摇掷：请按初爻至上爻的顺序手动输入六个爻（三个阳[333], 三个阴[222], 两阳一阴[332], 两阴一阳[322]）。")
        printfn()
        six_yao = []
        def type_one_yao(i):
            yao_name = Symbols.YAO_POSITION_NAMES.get(i)
            for _ in range(99):
                cmd_input = input(f"{yao_name}: ")
                if re.match("^[23]{3}$", cmd_input):
                    one_yao = [int(item) for item in cmd_input]
                    total = sum(one_yao)
                    return [one_yao, total]
                printfn(f"错误: 无效输入[ {cmd_input} ], 请参考: 三个阳[333], 三个阴[222], 两阳一阴[332], 两阴一阳[322].")
            raise Exception("无效摇掷了99次，如需重新摇掷，请重新运行程序。")
        # -*- -*- -*-
        six_yao = [type_one_yao(i) for i in range(1, 7)]
        # -*- -*- -*-
        return six_yao
    
    @classmethod
    def parse_six_yao(cls, six_yao):
        """
        解析六爻
        """
        parsed_six_yao = []
        for i in reversed(range(len(six_yao))):
            yao = six_yao[i]
            yao_yinyang_position_name = Symbols.YAO_YINYANG_POSITION_NAMES[0 if yao[-1] % 2 == 0 else 1][i+1]
            parsed_six_yao.append(f"{yao_yinyang_position_name} {yao}")
        return parsed_six_yao


class Calculator(object):
    """
    计算类，用于实现卦象相关的计算功能
    """

    @classmethod
    def get_up_and_down_symbols(cls, six_yao):
        """取上下卦"""
        six_yao_up   = six_yao[3:] # 上卦：左为四，右为上，从四至上。
        six_yao_down = six_yao[:3] # 下卦：左为初，右为三，从初至三。
        six_yao_up_symbols   = "".join([str(item[-1] % 2) for item in six_yao_up])
        six_yao_down_symbols = "".join([str(item[-1] % 2) for item in six_yao_down])
        diagrams_up = Symbols.TRIGRAMS.get(six_yao_up_symbols)
        diagrams_down = Symbols.TRIGRAMS.get(six_yao_down_symbols)
        diagrams = Symbols.HEXAGRAMS.get(f"{diagrams_up[0]}{diagrams_down[0]}")
        return {
            "卦理": "本卦又称主卦、原卦、遇卦，提示初始或当下。",
            "上卦": diagrams_up,
            "下卦": diagrams_down,
            f"{diagrams_up[-1]}{diagrams_down[-1]}": diagrams
        }

    @classmethod
    def get_active_symbols(cls, six_yao):
        """取主变爻"""
        sum_six_yao = sum([item[-1] for item in six_yao])
        num = 55 - sum_six_yao
        cur = 0 # 给一个初始值(如果输出0, 则计算有错误)
        tmp = num % 12
        if tmp == 0  : cur = 1
        elif tmp < 7 : cur = tmp
        elif tmp > 6 : cur = 6 - (tmp % 6) + 1
        # -*- -*- -*-
        active_symbol = [
            Symbols.YAO_YINYANG_POSITION_NAMES.get(0 if one_yao[-1] % 2 == 0 else 1).get(i+1)
            for i, one_yao in enumerate(six_yao)
            if one_yao[-1] == 6 or one_yao[-1] == 9
        ]
        active_symbol.reverse()
        # -*- -*- -*-
        return {
            "六爻之和": f"{sum_six_yao}",
            "天地余数": f"55-{sum_six_yao}={num} 偶数偏静、奇数偏动。",
            "主变爻序": f"{cur}",
            "主变爻位": Symbols.YAO_YINYANG_POSITION_NAMES.get(0 if six_yao[cur-1][-1] % 2 == 0 else 1).get(cur),
            "主变变在": Symbols.THREE_DAO.get(cur),
            "六九动爻": active_symbol if len(active_symbol) > 0 else "静卦，无动爻。",
            "变动说明": "上两爻为天，中两爻为人，下两爻为地。主变爻仅一个，动爻可六个（太杂乱）也可无（静卦），二者各占位天地人，重叠则表示极强。"
        }

    @classmethod
    def get_changes_symbols(cls, six_yao):
        """取得变卦"""
        new_six_yao = []
        for item in six_yao:
            temp = item[-1]
            if 9 == temp:
                new_six_yao.append([6])
                continue
            if 6 == temp:
                new_six_yao.append([9])
                continue
            new_six_yao.append([temp])
        new_two_symbols = cls.get_up_and_down_symbols(new_six_yao)
        new_two_symbols.update({
            "卦理": "变卦又称之卦，由本卦六九动爻变动而来(动爻变，主变爻不变)。提示万事万物皆可变，阴阳交替，老阴变阳，老阳变阴。"
        })
        return new_two_symbols

    @classmethod
    def get_opposite_symbols(cls, six_yao):
        """获得错卦"""
        new_six_yao = [[((item[-1] % 2) + 1) % 2] for item in six_yao]
        new_two_symbols = cls.get_up_and_down_symbols(new_six_yao)
        new_two_symbols.update({
            "卦理": "错卦又称对卦，由本卦阴阳交错而来。提醒立场相同，目标一致，角度不同，所见不同。提示最终结果，阴向阳发展，阳向阴发展。由于钱币阴阳不明或有误，错卦和本卦一样重要，错卦也可能就是本卦。"
        })
        return new_two_symbols

    @classmethod
    def get_reverse_symbols(cls, six_yao):
        """获得综卦"""
        new_six_yao = list(reversed(six_yao))
        new_two_symbols = cls.get_up_and_down_symbols(new_six_yao)
        new_two_symbols.update({
            "卦理": "综卦，由本卦颠倒旋转180度而来。提醒立场相对，角度不同，所见不同。提示反观视角(第三者的视角或回顾时的视角)。"
        })
        return new_two_symbols

    @classmethod
    def get_mutual_symbols(cls, six_yao):
        """取得互卦"""
        new_six_yao = [item for item in six_yao[1:4]] + [item for item in six_yao[2:5]]
        new_two_symbols = cls.get_up_and_down_symbols(new_six_yao)
        new_two_symbols.update({
            "卦理": "互卦又称复卦，由本卦去初爻和上爻，下卦取二三四，上卦取三四五。提示交互过程(中间互动发展的过程)。各地方言差异，错综互杂和错综复杂一字之差，理念相差较大。"
        })
        return new_two_symbols

    @classmethod
    def get_swap_up_and_down_symbols(cls, six_yao):
        """获得杂卦"""
        new_six_yao = [item for item in six_yao[3:]] + [item for item in six_yao[:3]]
        new_two_symbols = cls.get_up_and_down_symbols(new_six_yao)
        new_two_symbols.update({
            "卦理": "杂卦，由本卦上下卦换位而来。杂揉众卦，错综其义，或以同相类，或以异相明也。六十四卦有三十二对杂卦，上下相对互为杂卦。"
        })
        return new_two_symbols

    @classmethod
    def run(cls, six_yao):
        """
        运行完整的卦象计算流程
        """
        return {
            "本卦": cls.get_up_and_down_symbols(six_yao),
            "主变": cls.get_active_symbols(six_yao),
            "变卦": cls.get_changes_symbols(six_yao),
            "错卦": cls.get_opposite_symbols(six_yao),
            "综卦": cls.get_reverse_symbols(six_yao),
            "互卦": cls.get_mutual_symbols(six_yao),
            "杂卦": cls.get_swap_up_and_down_symbols(six_yao)
        }


if __name__ == "__main__":
    # -*- -*- -*- -*- -*- -*- -*- -*- -*-
    if len(sys.argv) > 1:
        business = " ".join(sys.argv[1:])
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        printfn()
        printfn(f"卜卦之事: {business}")
        printfn()
        printfn("自动起卦中...")
        printfn()
        six_yao = SixYao.auto_six_yao()
    else:
        printfn("-*- " * 25)
        printfn(DOCS)
        printfn("-*- " * 25)
        # -*- -*- -*- -*- -*- -*- -*- -*- -*-
        printfn()
        printfn("卜卦之事:", end="")
        business  = input()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # -*- -*- -*- -*- -*- -*- -*- -*- -*-
        printfn()
        printfn("输入字母[y或Y]自动起卦，输入其他任意字符则需手动摇金钱卦。")
        printfn("自动起卦: ", end="")
        cmd = input()
        printfn()
        if cmd.lower() in ['y', 'yes'] : six_yao = SixYao.auto_six_yao() # 有打印输出
        else                           : six_yao = SixYao.type_six_yao() # 有打印交互
    # -*- -*- -*- -*- -*- -*- -*- -*- -*-
    json_results={"六爻": SixYao.parse_six_yao(six_yao)}
    json_results.update(Calculator.run(six_yao))
    json_results_str = json.dumps(json_results, indent=4, ensure_ascii=False)
    # -*- -*- -*- -*- -*- -*- -*- -*- -*-
    printfn()
    printfn("建议将以下输出内容复制给大语言模型解读：")
    printfn()
    printfn(f"起卦: {timestamp}")
    printfn()
    printfn(f"卜卦: {business}")
    printfn()
    printfn(json_results_str)
    printfn()
    # -*- -*- -*- -*- -*- -*- -*- -*- -*-
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_json_path = os.path.join(output_dir, f"{timestamp.replace('-', '').replace(':', '').replace(' ', '_')}_results.md")
    md_content = f"起卦: {timestamp}\n\n卜卦: {business}\n\n{json_results_str}\n"
    with open(output_json_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    # -*- -*- -*- -*- -*- -*- -*- -*- -*-
