#%%
import json

with open('person.json') as f:
    data = json.load(f)

# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
print(data)
# %%
import json

person_dict = {"name": "Bob",
"languages": ["English", "Fench"],
"married": True,
"age": 32
}

with open('person.txt', 'w') as json_file:
  json.dump(person_dict, json_file)
# %%


myfamily = {
  "child1" : {
    "name" : "Emil",
    "year" : 2004
  },
  "child2" : {
    "name" : "Tobias",
    "year" : 2007
  },
  "child3" : {
    "name" : "Linus",
    "year" : 2011
  }
}

with open('person.json', 'w') as f:  # writing JSON object
    json.dump(myfamily, f)


# %%
dicts = {}
keys = range(4)
values = ["Hi", "I", "am", "John"]
for i in keys:
        dicts[i] = values[i]
# print(dicts)

with open('person.json', 'w') as f:  # writing JSON object
    json.dump(dicts, f)

# %%

events = {}
# events['Events'] = []

ID = range(4)
names = ['a', 'b', 'a', 'd']
number = ['asdf', 'sdfa', 'dfas', 'fasd']

for i in range(4):

    if names[i] not in events:
        events[names[i]] = {
            'ID': ID[i],
            'names': names[i],
            'number': number[i],
            'appearance': 1
        }
    
    else: 

        events['a']['appearance'] = events['a']['appearance'] + 1
        # events[names[i]]['appe']
        print('eskalation')
   
# print(events)

with open('data.json', 'w') as f:  # writing JSON object
    json.dump(events, f, indent=4)
# %%

import json

data = {}
data['people'] = []
data['people'].append({
    'name': 'Scott',
    'website': 'stackabuse.com',
    'from': 'Nebraska'
})
data['people'].append({
    'name': 'Larry',
    'website': 'google.com',
    'from': 'Michigan'
})
data['people'].append({
    'name': 'Tim',
    'website': 'apple.com',
    'from': 'Alabama'
})

with open('data.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
# %%
