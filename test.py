contact = {
            'Name': "data.get('Name')",
            'Email': "data.get('Email')",
            'Message': "data.get('Message')",
            'CreatedOnDate': "data.get('CreatedOnDate')",
            'IsActive': "data.get('IsActive')",
            'InstagramLink': "data.get('InstagramLink')",
            'TwitterLink': "data.get('TwitterLink')"
        }

tableName = "Contact"
columnKeys = list(contact.keys())
columnNamesWithSquareBrackets = ['[{}]'.format(key) for key in columnKeys]
columnNamesWithoutSquareBrackets = str(columnNamesWithSquareBrackets)[1:-1].replace("'","")

columnValues = list(contact.values())
columnValuesWithoutBrackets = str(columnValues)[1:-1].replace('"' , "'")
print(columnValuesWithoutBrackets)

query = f'''INSERT INTO [{tableName}]
  ( -- Columns to insert data into
   {columnNamesWithoutSquareBrackets}
  )
  VALUES
  ( -- First row: values for the columns in the list above
   {columnValuesWithoutBrackets}
  )'''

print(query)