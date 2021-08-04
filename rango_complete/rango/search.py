import json
import requests

def read_search_key():
    """
    Add the specific file to supoort the search funtion
    """
    search_api_key = None
    try:
        with open('search.key', 'r') as f:
            search_api_key = f.readline().strip()
        
    except:
        try:
            with open('../search.key') as f:
                search_api_key = f.readline().strip()
        except:
            raise IOError('search.key file not found')

    if not search_api_key:
        raise KeyError('search key not found')

    return search_api_key

def run_query(search_terms):
    search_key = read_search_key()
    search_url = 'https://api.bing.microsoft.com/v7.0/search'
    headers = {'Ocp-Apim-Subscription-Key': search_key}
    params = {'q': search_terms, 'textDecorations': True, 'textFormat':'HTML'}

    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    results = []
    for result in search_results['webPages']['value']:
        results.append({
            'title': result['name'],
            'link': result['url'],
            'summary': result['snippet']})

    return results

# def main():
#     search_terms = input("Enter query:")
#     results = run_query(search_terms)

#     for result in results:
#         print(result['title'])
#         print(result['link'])
#         print(result['summary'])
#         print('======')

# if __name__ == '__main__':
#     main()
