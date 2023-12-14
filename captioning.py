import os
import glob
import json


# json 파일 예시
# {"image_id":"8952_5","image_file_name":"8952_5_RH.jpg","value_1":"0","value_2":"0","value_3":"0","value_4":"0","value_5":"0","value_6":"0"}

# 캡션 생성 함수
def create_caption_final(json_data):
    # 카테고리와 상태 매핑
    categories = {
        "1": "미세각질",
        "2": "피지과다",
        "3": "모낭사이홍반",
        "4": "모낭홍반/농포",
        "5": "비듬",
        "6": "탈모"
    }
    states = {
        "0": "없고",
        "1": "양호하고",
        "2": "경증이고",
        "3": "중등도이고",
        "4": "중증이고"
    }
    # 마지막 상태 "다" 로 끝나게 만듬
    last_states = {
        "0": "없다",
        "1": "양호하다",
        "2": "경증이다",
        "3": "중등도이다",
        "4": "중증이다"
    }

    # 파일 경로 예시 "image_file_name":"8952_5_RH.jpg"
    # 사진 파일 이름만
    file_path = json_data["image_file_name"]

    # 캡션 구성
    captions = []
    for i, (key, category) in enumerate(categories.items()):
        value_key = f"value_{key}"
        state = states[json_data[value_key]]
        last_state = last_states[json_data[value_key]]

        # 상태가 "없음"이고 마지막 항목이면 "없다"로 변경
        if key != "6":
            caption = f"{category} {state}"
        else:
            caption = f"{category} {last_state}."
        captions.append(caption)

    # 캡션 합치기
    full_caption = f"{file_path}, {' '.join(captions)}"
    return full_caption

def read_json_files(folder_path):
    json_files = glob.glob(os.path.join(folder_path, '*.json'))
    captions = []
    
    for file in json_files:
        with open(file, 'r') as f:
                json_data = json.load(f)
                caption = create_caption_final(json_data)
                captions.append(caption)
                
    return captions

# base_folder 만 라벨링데이터 파일 경로에 맞게 수정
base_folder = ".\\라벨링데이터"
categories = ["1.미세각질", "2.피지과다", "3.모낭사이홍반", "4.모낭홍반농포", "5.비듬", "6.탈모"]
sub_categories = ["0.양호", "1.경증", "2.중등도", "3.중증"]

all_captions = []
for category in categories:
    for sub_category in sub_categories:
        folder_path = os.path.join(base_folder, category, sub_category)
        all_captions.extend(read_json_files(folder_path))

# 테스트
# test_json = {"image_id":"8952_5","image_file_name":"8952_5_RH.jpg","value_1":"0","value_2":"0","value_3":"0","value_4":"0","value_5":"0","value_6":"0"}

# print(create_caption_final(test_json))


# 파일 생성

with open('captions.txt', 'w') as f:
    for caption in all_captions:
        f.write(caption + '\n')