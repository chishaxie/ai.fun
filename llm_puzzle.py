import json
import sys
from itertools import permutations
import copy

###
Q = '''
参加晚宴的有甲、乙、丙、丁和戊五个女人。女人们坐成一排。她们都来自不同的地点，穿着不同颜色的衣服，喝着不同样的酒，拿着不同的传家宝。
甲穿着一顶醒目的紫色长袍。丁坐在最左边，身旁的客人穿着红色夹克。穿绿衣服的女士坐在穿蓝衣服的人的左边旁边。我记得那件绿衣服是因为穿着它的女士把朗姆酒洒了一地。来自巴黎的旅行者一身白衣。当其中一位客人炫耀她的战争勋章时，她旁边的女人说自己所住的巴黎有更漂亮的奖章。
于是乙展示了一颗珍贵的钻石。来自伦敦的女士对此嗤之以鼻，说这比不上她的戒指。还有人戴着一个珍贵的鸟形吊坠，旁边那位来自柏林的客人看到这个吊坠时，差点把邻座的威士忌打翻在地。戊举起啤酒干杯。来自罗马的女士满口苦艾酒，跳上了桌子，摔倒在中间座位的客人身上，打翻了这位可怜女士的葡萄酒。接着，丙向大家讲述了她在布拉格的狂野青春。
早上，桌子下面有四件传家宝：战争勋章、鼻烟壶、戒指和鸟形吊坠。
但这几样东西分别属于谁？
'''
###

###
A = '''
丁 来自 巴黎，穿着 白色 衣服，喝着 威士忌，拿着 鸟形吊坠
戊 来自 柏林，穿着 红色 衣服，喝着 啤酒，拿着 战争勋章
丙 来自 布拉格，穿着 绿色 衣服，喝着 朗姆酒，拿着 鼻烟壶
乙 来自 罗马，穿着 蓝色 衣服，喝着 苦艾酒，拿着 钻石
甲 来自 伦敦，穿着 紫色 衣服，喝着 葡萄酒，拿着 戒指
'''
###

###
# 剪枝
# 原始 = 5! * 5! * 5! * 5! * 5! = 24,883,200,000
# 一阶 = 4! * 4! * 4! * 5! * 5! =      199,065,600
# 二阶     199,065,600          ->         7,257,600
###

# 定义所有可能的属性
people = ['甲', '乙', '丙', '丁', '戊']
locations = ['巴黎', '伦敦', '柏林', '罗马', '布拉格']
colors = ['紫色', '红色', '绿色', '蓝色', '白色']
drinks = ['朗姆酒', '威士忌', '啤酒', '苦艾酒', '葡萄酒']
heirlooms = ['战争勋章', '钻石', '戒指', '鸟形吊坠', '鼻烟壶']

# 丁坐在最左边，固定丁的位置
remaining_people = [p for p in people if p != '丁']
people_permutations = [('丁',) + other_people for other_people in permutations(remaining_people)]

# 红色在第二个位置，固定红色
remaining_colors = [c for c in colors if c != '红色']
color_permutations = [(other_colors[0], '红色') + other_colors[1:] for other_colors in permutations(remaining_colors)]

# 葡萄酒在中间位置，固定葡萄酒
remaining_drinks = [d for d in drinks if d != '葡萄酒']
drink_permutations = [other_drinks[:2] + ('葡萄酒',) + other_drinks[2:] for other_drinks in permutations(remaining_drinks)]

# 提前计算 locations 和 heirlooms 的排列组合
location_permutations = list(permutations(locations))
heirloom_permutations = list(permutations(heirlooms))

# 输出每个 _permutations 的长度
print(f"people_permutations 长度: {len(people_permutations)}")
print(f"color_permutations 长度: {len(color_permutations)}")
print(f"drink_permutations 长度: {len(drink_permutations)}")
print(f"location_permutations 长度: {len(location_permutations)}")
print(f"heirloom_permutations 长度: {len(heirloom_permutations)}")

# 用于记录遍历次数
traversal_count = 0

# 用于存储找到的解
solutions = []

# 检查特定结果是否为解，根据 need_reasons 和 full_check 参数决定是否输出不匹配原因和进行完整检查
def check_specific_result(person_info, people_order, need_reasons=False, full_check=False):
    if need_reasons:
        not_matching_conditions = []
    if full_check:
        # 线索1：丁坐在最左边
        if people_order[0] != '丁':
            if need_reasons:
                not_matching_conditions.append("线索1：丁坐在最左边")
            else:
                return False
        # 线索2：红色在第二个位置
        if person_info[people_order[1]]['color'] != '红色':
            if need_reasons:
                not_matching_conditions.append("线索2：红色在第二个位置")
            else:
                return False
        # 线索3：葡萄酒在中间位置
        if person_info[people_order[2]]['drink'] != '葡萄酒':
            if need_reasons:
                not_matching_conditions.append("线索3：葡萄酒在中间位置")
            else:
                return False
        # 线索4：甲穿紫色衣服
        if '甲' in people_order and person_info['甲']['color'] != '紫色':
            if need_reasons:
                not_matching_conditions.append("线索4：甲穿紫色衣服")
            else:
                return False
        # 线索5：戊举起啤酒干杯
        if '戊' in people_order and person_info['戊']['drink'] != '啤酒':
            if need_reasons:
                not_matching_conditions.append("线索5：戊举起啤酒干杯")
            else:
                return False
    # 线索6：丙来自布拉格
    if person_info['丙']['location'] != '布拉格':
        if need_reasons:
            not_matching_conditions.append("线索6：丙来自布拉格")
        else:
            return False
    # 线索7：来自罗马的女士满口苦艾酒
    found_roman = False
    for person in people_order:
        if person_info[person]['location'] == '罗马':
            found_roman = True
            if person_info[person]['drink'] != '苦艾酒':
                if need_reasons:
                    not_matching_conditions.append("线索7：来自罗马的女士满口苦艾酒")
                else:
                    return False
                break
    if not found_roman:
        if need_reasons:
            not_matching_conditions.append("线索7：未找到来自罗马的人")
        else:
            return False
    # 线索8：来自巴黎的旅行者一身白衣
    found_paris = False
    for person in people_order:
        if person_info[person]['location'] == '巴黎':
            found_paris = True
            if person_info[person]['color'] != '白色':
                if need_reasons:
                    not_matching_conditions.append("线索8：来自巴黎的旅行者一身白衣")
                else:
                    return False
                break
    if not found_paris:
        if need_reasons:
            not_matching_conditions.append("线索8：未找到来自巴黎的人")
        else:
            return False
    # 线索9：乙展示了一颗珍贵的钻石
    if person_info['乙']['heirloom'] != '钻石':
        if need_reasons:
            not_matching_conditions.append("线索9：乙展示了一颗珍贵的钻石")
        else:
            return False
    # 线索10：来自伦敦的女士拿着戒指
    found_london = False
    for person in people_order:
        if person_info[person]['location'] == '伦敦':
            found_london = True
            if person_info[person]['heirloom'] != '戒指':
                if need_reasons:
                    not_matching_conditions.append("线索10：来自伦敦的女士拿着戒指")
                else:
                    return False
                break
    if not found_london:
        if need_reasons:
            not_matching_conditions.append("线索10：未找到来自伦敦的人")
        else:
            return False
    # 线索11：穿绿衣服的女士坐在穿蓝衣服的人的左边且相邻
    green_index = None
    blue_index = None
    for idx, person in enumerate(people_order):
        if person_info[person]['color'] == '绿色':
            green_index = idx
        if person_info[person]['color'] == '蓝色':
            blue_index = idx
    if green_index is None or blue_index is None or green_index + 1 != blue_index:
        if need_reasons:
            not_matching_conditions.append("线索11：穿绿衣服的女士坐在穿蓝衣服的人的左边且相邻")
        else:
            return False
    # 线索12：穿绿衣服的女士把朗姆酒洒了一地
    found_green = False
    for person in people_order:
        if person_info[person]['color'] == '绿色':
            found_green = True
            if person_info[person]['drink'] != '朗姆酒':
                if need_reasons:
                    not_matching_conditions.append("线索12：穿绿衣服的女士把朗姆酒洒了一地")
                else:
                    return False
                break
    if not found_green:
        if need_reasons:
            not_matching_conditions.append("线索12：未找到穿绿衣服的人")
        else:
            return False
    # 线索13：当其中一位客人炫耀她的战争勋章时，她旁边的女人说自己所住的巴黎有更漂亮的奖章
    war_medal_index = None
    paris_index = None
    for idx, person in enumerate(people_order):
        if person_info[person]['heirloom'] == '战争勋章':
            war_medal_index = idx
        if person_info[person]['location'] == '巴黎':
            paris_index = idx
    if war_medal_index is not None and paris_index is not None:
        if not ((war_medal_index + 1 == paris_index or war_medal_index - 1 == paris_index) and
                0 <= war_medal_index <= 4 and 0 <= paris_index <= 4):
            if need_reasons:
                not_matching_conditions.append("线索13：当其中一位客人炫耀她的战争勋章时，她旁边的女人说自己所住的巴黎有更漂亮的奖章")
            else:
                return False
    else:
        if need_reasons:
            not_matching_conditions.append("线索13：未找到拥有战争勋章或来自巴黎的人")
        else:
            return False
    # 线索14：有人戴着一个珍贵的鸟形吊坠，旁边那位来自柏林的客人看到这个吊坠时，差点把邻座的威士忌打翻在地
    bird_pendant_index = None
    berlin_index = None
    whiskey_index = None
    for idx, person in enumerate(people_order):
        if person_info[person]['heirloom'] == '鸟形吊坠':
            bird_pendant_index = idx
        if person_info[person]['location'] == '柏林':
            berlin_index = idx
        if person_info[person]['drink'] == '威士忌':
            whiskey_index = idx
    if bird_pendant_index is not None and berlin_index is not None:
        valid_bird_condition = (
            (bird_pendant_index + 1 == berlin_index and (bird_pendant_index + 2 == whiskey_index or bird_pendant_index == whiskey_index)) or
            (bird_pendant_index - 1 == berlin_index and (bird_pendant_index - 2 == whiskey_index or bird_pendant_index == whiskey_index))
        )
        if not valid_bird_condition:
            if need_reasons:
                not_matching_conditions.append("线索14：有人戴着一个珍贵的鸟形吊坠，旁边那位来自柏林的客人看到这个吊坠时，差点把邻座的威士忌打翻在地")
            else:
                return False
    else:
        if need_reasons:
            not_matching_conditions.append("线索14：未找到拥有鸟形吊坠或来自柏林的人")
        else:
            return False

    if need_reasons:
        if not_matching_conditions:
            return False, not_matching_conditions
        return True, []
    return True

# 检查输入的 JSON 数据是否包含正确的属性值
def check_input_validity(person_info):
    for person, info in person_info.items():
        if info['location'] not in locations:
            print(f"错误：{person} 的地点 '{info['location']}' 不在预设范围内。")
            return False
        if info['color'] not in colors:
            print(f"错误：{person} 的颜色 '{info['color']}' 不在预设范围内。")
            return False
        if info['drink'] not in drinks:
            print(f"错误：{person} 的饮品 '{info['drink']}' 不在预设范围内。")
            return False
        if info['heirloom'] not in heirlooms:
            print(f"错误：{person} 的传家宝 '{info['heirloom']}' 不在预设范围内。")
            return False
    return True

if len(sys.argv) > 1:
    # 示例 JSON 输入，可将其保存为文件并作为参数传入
    # {
    #     "丁": {
    #         "location": "伦敦",
    #         "color": "绿色",
    #         "drink": "朗姆酒",
    #         "heirloom": "戒指"
    #     },
    #     "戊": {
    #         "location": "巴黎",
    #         "color": "白色",
    #         "drink": "啤酒",
    #         "heirloom": "鼻烟壶"
    #     },
    #     "丙": {
    #         "location": "布拉格",
    #         "color": "红色",
    #         "drink": "威士忌",
    #         "heirloom": "鸟形吊坠"
    #     },
    #     "乙": {
    #         "location": "柏林",
    #         "color": "蓝色",
    #         "drink": "葡萄酒",
    #         "heirloom": "钻石"
    #     },
    #     "甲": {
    #         "location": "罗马",
    #         "color": "紫色",
    #         "drink": "苦艾酒",
    #         "heirloom": "战争勋章"
    #     }
    # }
    file_path = sys.argv[1]
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            specific_solution = json.load(file)
        # 检查输入的 JSON 数据是否包含正确的属性值
        if not check_input_validity(specific_solution):
            sys.exit(1)
        people_order = tuple(specific_solution.keys())
        result, reasons = check_specific_result(specific_solution, people_order, need_reasons=True, full_check=True)
        if result:
            print("特定解是有效的。")
        else:
            print("特定解无效，不满足以下条件：")
            for reason in reasons:
                print(reason)
    except FileNotFoundError:
        print(f"错误：未找到文件 {file_path}。")
    except json.JSONDecodeError:
        print(f"错误：文件 {file_path} 不是有效的 JSON 格式。")
else:
    for people_order in people_permutations:
        for color_order in color_permutations:
            for drink_order in drink_permutations:
                # 前三层循环剪枝，不创建 person_info 字典
                # 线索4：甲穿紫色衣服；线索5：戊举起啤酒干杯
                if (
                        people_order.index('甲') >= 0 and color_order[people_order.index('甲')] != '紫色' or
                        people_order.index('戊') >= 0 and drink_order[people_order.index('戊')] != '啤酒'
                ):
                    continue

                # 创建字典来存储每个人的属性
                person_info = {}
                for i in range(5):
                    person_info[people_order[i]] = {
                        'location': None,
                        'color': color_order[i],
                        'drink': drink_order[i],
                        'heirloom': None
                    }

                for location_order in location_permutations:
                    for i in range(5):
                        person_info[people_order[i]]['location'] = location_order[i]

                    for heirloom_order in heirloom_permutations:
                        for i in range(5):
                            person_info[people_order[i]]['heirloom'] = heirloom_order[i]

                        # 增加遍历次数
                        traversal_count += 1

                        # 检查所有线索
                        result = check_specific_result(person_info, people_order)
                        if not result:
                            continue

                        # 如果满足所有线索，记录解
                        solutions.append(copy.deepcopy(person_info))

    # 输出全部遍历次数
    print(f"全部遍历次数: {traversal_count}")

    # 输出有效的解
    valid_solutions = []
    if solutions:
        print("初步找到有效解，开始二次验证...")
        for solution in solutions:
            people_order = tuple(solution.keys())
            result, _ = check_specific_result(solution, people_order, need_reasons=True, full_check=True)
            if result:
                valid_solutions.append(solution)
        if valid_solutions:
            print("经过二次验证，找到有效解：")
            for idx, solution in enumerate(valid_solutions, start=1):
                print(f"解 {idx}:")
                # 按照从左到右的顺序输出
                for person in people_order:
                    print(f"{person} 来自 {solution[person]['location']}，穿着 {solution[person]['color']} 衣服，喝着 {solution[person]['drink']}，拿着 {solution[person]['heirloom']}")
        else:
            print("经过二次验证，未找到有效解。")
    else:
        print("未找到有效解。")
    
