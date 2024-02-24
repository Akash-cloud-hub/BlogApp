from main import connectToDb , performCRUD
query = f'''SELECT TOP (1000) [UserId]
      ,[NameOfUser]
      ,[Email]
      ,[UserName]
      ,[Password]
  FROM [BlogApp].[dbo].[Users]
'''
cursor = connectToDb()
result = performCRUD(query= query)
print(result)