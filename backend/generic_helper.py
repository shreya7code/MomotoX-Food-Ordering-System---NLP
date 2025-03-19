import re

def extract_session_id(session_str: str):
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        extracted_string = match.group(1)
        return extracted_string

    return ""


def get_str_from_food_dict(food_dict: dict):
    # input - {chole:2, chat:4} output - 2 chole, 4 chat
    result = ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])
    return result

if __name__ == "__main__":
    print("-------")
    print(extract_session_id("project/sessions/abc123/contexts/"))