import csv
import sys
input = 'ol_dump_2020-09-30.txt'
output = 'books/books.txt'
smallFile = None
csv.field_size_limit(sys.maxsize)
with open(input, 'r') as csvinputfile:
    csvreader = csv.reader(csvinputfile, delimiter='\t')
    i = 0
    count= 0 
    for row in csvreader:
        if len(row) > 4:
          if (row[0] == '/type/edition'):
            if i % 75000 == 0:
                if smallFile:
                    smallFile.seek(smallFile.tell()-1)
                    smallFile.write(']}')
                    smallFile.close()
                smallFileName = 'books'+str(count)+'.txt'
                count = count + 1
                smallFile = open('books/'+smallFileName, "w")
                smallFile.write('''{"books":[''')
            i = i + 1
            entry = row[4]

            startTitleIndex = entry.find('''"title":''')
            endTitleIndex = entry.find('''",''', startTitleIndex+10)

            name = entry[startTitleIndex+10:endTitleIndex]
            name = name.replace('"', "'")
            name = name.replace("\\", r"")

            title = '''"title": "''' + name + '''"''' 

            startAuthorsIndex = entry.find('''"authors":''')
            endAuthorsIndex = entry.find('''],''', startAuthorsIndex)
            authors = entry[startAuthorsIndex:endAuthorsIndex+1]

            isbn_10_start = entry.find('''"isbn_10":''')
            isbn_10_end = entry.find('''"]''', isbn_10_start)
            isbn_10 = entry[isbn_10_start: isbn_10_end+2]

            isbn_13_start = entry.find('''"isbn_13":''')
            isbn_13_end = entry.find('''"]''', isbn_13_start)
            isbn_13 = entry[isbn_13_start: isbn_13_end+2]

            if (startAuthorsIndex == -1):
              authors = '''"authors": []'''

            if (isbn_10_start == -1 or isbn_10_end == -1 or len(isbn_10) < 25):
                  isbn_10 = '''"isbn_10": []'''

            if (isbn_13_start == -1 or isbn_13_end == -1 or len(isbn_13) < 28):
                  isbn_13 = '''"isbn_13": []'''
              

            smallFile.write('{' + title + ", " + authors + ", " + isbn_10+ ", " + isbn_13+'},')
    if smallFile:
        smallFile.seek(smallFile.tell()-1)
        smallFile.write(']}')
        smallFile.close()
print('Finished reading')
print('Finished writing')