

# dic = {"fname": "mikee", "lname":"kola","age": 23}

# # print(dic.items())
# for i in dic.keys():
#     print(i)

class Student:
    name = ""
    age: int = 0


# stud = Student(name="mike", age=34)

# print(stud)

# print(Student.__dict__)
for k in Student.__dict__:
    if k.startswith('_') == False:
        print(k)
