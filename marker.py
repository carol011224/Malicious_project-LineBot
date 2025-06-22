"""
搜尋 marker 類別
""" 

from ckiptagger import data_utils, construct_dictionary, WS
import re

# 讀取 markers
with open("./markers/hedge_markers.txt", "r", encoding="utf-8") as f:
    hedge = [line.strip() for line in f if line.strip()]

print('成功讀取 hedge\n\n', hedge)

with open("./markers/booster_markers.txt", "r", encoding="utf-8") as f:
    booster = [line.strip() for line in f if line.strip()]
print('成功讀取 booster\n\n', booster)

with open("./markers/attitude_markers.txt", "r", encoding="utf-8") as f:
    attitude = [line.strip() for line in f if line.strip()]

print('成功讀取 attitude\n\n', attitude)

with open("./markers/self_mention_markers.txt", "r", encoding="utf-8") as f:
    self_mention = [line.strip() for line in f if line.strip()]

print('成功讀取 self_mention\n\n', self_mention)

with open("./markers/engagement_markers.txt", "r", encoding="utf-8") as f:
    engagement = [line.strip() for line in f if line.strip()]
print('成功讀取 engagement\n\n', engagement)

with open("./markers/predefined_markers.txt", "r", encoding="utf-8") as f:
    predefined = [line.strip() for line in f if line.strip()]

print('成功讀取 predefined\n\n', predefined)


# def convert_marker_to_regex(marker: str, max_length: int = 6) -> str:
#     """
#     將像「令人…的」這類語構 marker 轉換為 regex pattern，使用 \w。
#     """
#     if "…" in marker or "..." in marker:
#         # 把 … 或 ... 換成 \w{0,n}
#         pattern = re.sub(r"[…\.]{1,3}", rf"\\w{{0,{max_length}}}", marker)
#         return pattern
#     elif " " in marker:
#         # 把空格當成省略處處理
#         parts = marker.split(" ")
#         if len(parts) == 2:
#             return rf"{parts[0]}\\w{{0,{max_length}}}{parts[1]}"
#     return marker  # 沒有省略標記就原樣返回

# regex_hedge=[]
# for h in hedge:
#     h=convert_marker_to_regex(h)
#     regex_hedge.append(h)

# regex_booster=[]
# for b in booster:
#     b=convert_marker_to_regex(b)
#     regex_booster.append(b)

# regex_attitude=[]
# for a in attitude:
#     a=convert_marker_to_regex(a)
#     regex_attitude.append(a)

# regex_self_mention=[]
# for s in self_mention:
#     s=convert_marker_to_regex(s)
#     regex_self_mention.append(s)

# regex_engagement=[]
# for e in engagement:
#     e=convert_marker_to_regex(e)
#     regex_engagement.append(e)


# def save_list_to_txt(lst, filename):
#     with open(filename, "w", encoding="utf-8") as f:
#         for item in lst:
#             f.write(item + "\n")
# save_list_to_txt(regex_hedge, "./regex_markers/hedge_regex.txt")
# save_list_to_txt(regex_booster, "./regex_markers/booster_regex.txt")
# save_list_to_txt(regex_attitude, "./regex_markers/attitude_regex.txt")
# save_list_to_txt(regex_self_mention, "./regex_markers/self_mention_regex.txt")
# save_list_to_txt(regex_engagement, "./regex_markers/engagement_regex.txt")

dict_for_CKIP={}
for item in predefined:
    dict_for_CKIP[item]=1
dict_for_CKIP = construct_dictionary(dict_for_CKIP)


from ckiptagger import WS

# 初始化 CKIP 模型
ws = WS("./data")

# 載入 marker 詞表（假設已經讀進來）
# hedge = [...], booster = [...], ...

# 轉為 set 加快查找速度
hedge_set = set(hedge)
booster_set = set(booster)
attitude_set = set(attitude)
self_mention_set = set(self_mention)
engagement_set = set(engagement)

def analyze_markers(user_input: str, coerce_dict: dict = None) -> dict:
    # CKIP 接收的是 list[str]
    segs = ws([user_input], coerce_dictionary=dict_for_CKIP)[0]
    total_tokens = len(segs)

    result = {
        'hedge': {'count': 0, 'words': []},
        'booster': {'count': 0, 'words': []},
        'attitude': {'count': 0, 'words': []},
        'self_mention': {'count': 0, 'words': []},
        'engagement': {'count': 0, 'words': []}
    }

    for word in segs:
        if word in hedge_set:
            result['hedge']['count'] += 1
            result['hedge']['words'].append(word)
        if word in booster_set:
            result['booster']['count'] += 1
            result['booster']['words'].append(word)
        if word in attitude_set:
            result['attitude']['count'] += 1
            result['attitude']['words'].append(word)
        if word in self_mention_set:
            result['self_mention']['count'] += 1
            result['self_mention']['words'].append(word)
        if word in engagement_set:
            result['engagement']['count'] += 1
            result['engagement']['words'].append(word)

    # 計算個別比例
    for category in result:
        count = result[category]['count']
        result[category]['ratio'] = round(count / total_tokens, 4) if total_tokens > 0 else 0.0

    # 加總所有 interactional markers 的出現次數並計算總比例
    total_marker_count = sum(result[cat]['count'] for cat in result)
    total_ratio = round(total_marker_count / total_tokens, 4) if total_tokens > 0 else 0.0

    result['total_ratio'] = total_ratio

    return result





