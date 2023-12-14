import os
import glob
import json


# json 파일 예시
# {"image_id":"8952_5","image_file_name":"8952_5_RH.jpg","value_1":"0","value_2":"0","value_3":"0","value_4":"0","value_5":"0","value_6":"0"}

# 캡션 생성 함수
def create_caption_final(json_data):
    # 카테고리와 상태 매핑
    categories = {
        "1": "Microdermabrasion condition",
        "2": "Excess Sebum condition",
        "3": "Folliculitis condition",
        "4": "Folliculitis/Boil condition",
        "5": "Dandruff condition",
        "6": "Balding? Don't Extract!!!"
    }
    states = {
        "0": "shows no issues,",
        "1": "is optimal,",
        "2": "exhibits mild concerns,",
        "3": "exhibits moderate issues,",
        "4": "is severe,"
    }
    
    last_states = {
        "0": "shows no issues.",
        "1": "is optimal.",
        "2": "exhibits mild concerns.",
        "3": "exhibits moderate issues.",
        "4": "is severe."
    }

    # 파일 경로 예시 "image_file_name":"8952_5_RH.jpg"
    # 사진 파일 이름만
    file_path = json_data["image_file_name"]

    # 중증도별로 증상을 저장하고 정렬
    captions = []
    for i, (key, category) in enumerate(categories.items()):
        value_key = f"value_{key}"
        # state = states[json_data[value_key]]
        state_key = int(json_data[value_key])

        if state_key > 0:
            # 탈모 제외
            if key == "6":
                pass
            else:
                # captions 증상과 중증도 숫자로 구성
                captions.append((category, state_key))
    
    # captions를 중증도 숫자순서로 정렬
    captions.sort(key=lambda x: x[1], reverse = True)
    # captions 를 바탕으로 caption 에 증상과 중증도 설명
    # 마지막 증상은 제외
    caption = [f"{caption[0]} {states[str(caption[1])]}" for caption in captions[:-1]]
    
    # 증상이 1가지 이상 있을경우 아래 시작
    # 마지막 증상에 대해서 증상 생성
    if captions:
        last_captions = captions[-1]
        last_caption = f"{last_captions[0]} {last_states[str(last_captions[1])]}"
        caption.append(last_caption)
    # last_state = last_states[json_data[value_key]]
        # 이게 밸류값임 큰 순서대로 정렬이 필요 json_data[value_key]

    
    # 이하 구버전
        # 상태가 "없음"이고 마지막 항목이면 "없다"로 변경
        # if key == "6":
        #     break
        # if key != "5":
        #     caption = f"{category} {state}"
        # else:
        #     caption = f"{category} {last_state}."
        # captions.append(caption)
    # 이상 구버전
    
    # 증상이 아무것도 없을경우 증상없음 출력
    else:
        caption = ["There is no symptoms"]
    # 캡션 합치기
    full_caption = f"{file_path}, {' '.join(caption)}"
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
# test_json = {"image_id":"8952_5","image_file_name":"8952_5_RH.jpg","value_1":"1","value_2":"2","value_3":"0","value_4":"0","value_5":"0","value_6":"0"}

# print(create_caption_final(test_json))

# 파일 생성

with open('captions.txt', 'w') as f:
    for caption in all_captions:
        f.write(caption + '\n')