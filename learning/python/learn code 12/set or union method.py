s={1,5,32,"abhijeet"}
e=set()
print(s)
# set method
print(s,type(s))
s.add(566)
print(s,type(s))
s.remove(1)
print(s,type(s))
# set union intersection
s1={1,4,7,89}
s2={7,5,34,3}
print(s1.union(s2))
print(s1.intersection(s2))