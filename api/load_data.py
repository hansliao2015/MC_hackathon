import requests

def get_data(api_url):
    response = requests.get(api_url)
    
    if response.status_code == 200:
        return response.json()  # 假設返回 JSON 格式的資料
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None
