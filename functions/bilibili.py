import requests


def get_bilibili_username(user_id):
    url = f'https://api.bilibili.com/x/space/acc/info?mid={user_id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data and 'data' in data and 'name' in data['data']:
            return data['data']['name']
        else:
            return "Username not found"
    else:
        return f"Failed to retrieve data: {response.status_code}"


if __name__ == '__main__':
    # Example usage
    bilibili_user_id = 295323770
    username = get_bilibili_username(bilibili_user_id)
    print(username)
