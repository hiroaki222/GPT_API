import datetime
import json
import openai

with open('auth.json') as f:
    key = json.load(f)

openai.api_key = key["apikey"]

def call(content):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {
                "role": "user",
                "content": content
            },
        ],
    )
    return res

f = open('input.txt', 'r')
input = f.read()
f.close()
res = call(input)

print(f'response : {res["choices"][0]["message"]["content"]}')

with open('response.json') as f:
    forUpdate = json.load(f)
remaining = float(forUpdate['remaining'])
remaining -= 0.000002 * res["usage"]["total_tokens"]
forUpdate['remaining'] = str(remaining)
with open('response.json', 'w') as f:
    json.dump(forUpdate, f, ensure_ascii=False, indent=4)

print(f'\n使用したトークン\t残りのトークン\n{res["usage"]["total_tokens"]}\t\t\t{remaining}')

with open('response.json') as f:
    forUpdate = json.load(f)
tmp = {str(datetime.datetime.now()) : res}
forUpdate.update(tmp)
with open('response.json', 'w') as f:
    json.dump(forUpdate, f, ensure_ascii=False, indent=4)
