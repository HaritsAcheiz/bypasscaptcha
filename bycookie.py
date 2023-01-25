import requests




if __name__ == '__main__':
    tag = input('Type a tag: ')
    page = 1
    url = f'https://stackoverflow.com/questions/tagged/{tag}?tab=newest&page={str(page)}&pagesize=50'
    response = requests.request(method='GET', url=url)
    print(response)
    print(response.text)