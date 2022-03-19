# igsp-ngo
python library to parse data from [here](https://isgp-studies.com/ngo-list-foundations-and-think-tanks-worldwide)
still a work in progress :c

## Installation
1) Download the source, and copy lib_igsp_ngo.py into your python packages folder or wherever you import from.
2) Run ```pip3 install lxml requests``` to install dependencies
3) wait until I learn how to make pypi packages lol

## Usage Examples
1) Get all the NGOs listed on the site, and list all their members
```python3
from lib_igsp_ngo import*

#initialize NGOParser object
ng=NGOParser()

#look through the list of organizations and list their members
for org in ng.orgs:
  print(org)
  for m in org.members:
    print(" ",m)
```
2) Find all the NGOs a person has been affiliated with:
```python3
from lib_igsp_ngo import*

#initialize NGOParser object
ng=NGOParser()

#create an person object to use for the search
normal_everyday_person=ng.new_person("henry kissinger")

#print the organizations that this individual is a part of
for org in normal_everyday_person.orgs:
  print(org.title)
```
3) Find all the people a given person is connected to through organizations they mutually participate in
```python3
from lib_igsp_ngo import*

#initialize NGOParser object
ng=NGOParser()

#create an person object to use for the search
normal_everyday_person=ng.new_person("henry kissinger")

#get the associates
#this returns a dictionary with the format {"organization name": list_of_members}
#using "all" as a dictionary key will yield every member from every organization
for ass in normal_everyday_person.associates["all"]:
  print(ass)
```
