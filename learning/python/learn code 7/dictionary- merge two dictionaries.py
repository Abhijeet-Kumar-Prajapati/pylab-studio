# dict1={"john":89,"lisa":99}
# dict2={"lisa":94,"peter:"78}
# print(dict1|dict2)


# Dictionaries
dict1 = {"john": 89, "lisa": 99}
dict2 = {"lisa": 94, "peter": 78}  # Fixed typo in key "peter:"

# Merge dictionaries (Python 3.9+)
merged_dict = dict1 | dict2
print(merged_dict)
print({**dict1,**dict2})  #**operator