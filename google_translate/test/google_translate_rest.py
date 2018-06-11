import requests
r = requests.post("https://translation.googleapis.com/language/translate/v2", data={
    'q':'This is a dog',
    'target':'en'
})
print(r.status_code, r.reason)
print(r.text)