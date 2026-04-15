import json

response = '''{
    "businesses": [
        {
            "name":"Teton Elementary",
            "streetAddress":"126 Main Street",
            "cityStateZip":"Teton, ID 83451",
            "phoneNumber":"208-458-0154",
            "website":"https://sd215tet.ss4.sharpschool.com/",
            "imageURL":"./images/directory-teton-elementary.jpg",
            "membershipLevel":"nonprofit",
            "adcopy":"Teton Elementary has been around a long, long time."
        }
    ]
}'''

try:
    data = json.loads(response)
    print('JSON is valid')
    print('Number of businesses:', len(data['businesses']))
except json.JSONDecodeError as e:
    print('JSON is invalid:', e)