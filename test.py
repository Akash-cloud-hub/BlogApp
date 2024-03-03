# from main import connectToDb , performCRUD
# query = f'''SELECT TOP (1000) [UserId]
#       ,[NameOfUser]
#       ,[Email]
#       ,[UserName]
#       ,[Password]
#   FROM [BlogApp].[dbo].[Users]
# '''
# cursor = connectToDb()
# result = performCRUD(query= query)
# print(result)


# student_marks = {'Akash':[20,30,40],
#                  'Theshan' : [70,80,90]}
#
# query_name = input()
#
# sum = 0
#
# score_list = student_marks[query_name]
#
# for i in score_list:
#     sum += i
#
# average = sum/3
#
# print(format(average,".2f"))


# N = int(input("Enter the number of commands : "))
#
# my_list = [30,40,90]
# count = 0
#
# def get_value(command):
#     value = 0
#     for i in command:
#         if i.isdigit():
#             value = i
#     return value
#
#
# while count < N :
#     count += 1
#     prompt = ""
#     command = input( f"{count} command : ")
#     if command == "sort":
#         my_list.sort()
#
#     if command == "pop":
#         my_list.pop()
#
#     if command == "reverse":
#         my_list.reverse()
#
#     if command == "print":
#         print(my_list)
#
#     for j in command:
#         if not j.isdigit() and j is not None:
#             prompt += str(j)
#
#     print("The prompt is : " , prompt)
#     if prompt == "remove":
#         value = int(get_value(command))
#         print(value)
#         my_list.remove(int(value))
#
#     if prompt == "append ":
#         print("Append is activated..")
#         value = int(get_value(command))
#         print(value)
#         my_list.append(value)



import re

text = "Sample text with 2024-03-27T13:50 date and time."

# Define the pattern to keep
pattern = r'[0-9\-:]+'

# Find all matches in the text
matches = re.findall(pattern, text)

# Concatenate matches into a single string
result = ' '.join(matches)

print(result)
