# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 21:57:46 2019

@author: Erdal Guclu
"""

import pandas

#books stored as bookID, bookTitle, bookGenre
global books
books = 0 #no of books
#ratings stored as userName, bookID, bookRating
global ratings
ratings = 0 #no of ratings
#users stored as userName, password, profile
global users
users = 0 #no of users

with open("book_data.data") as bookData:
    for line in bookData:
        books += 1
        
with open("ratings_data.data") as ratingData:
    for line in ratingData:
        ratings += 1
        
with open("user_data.data") as userData:
    for line in userData:
        users += 1

def formatData(data):
    dataFormat = ""
    for item in data:
        dataFormat += (str(item) + "/")
    dataFormat = dataFormat[0:len(dataFormat)-1]
    dataFormat += "\n"
    return dataFormat     
                    
def addData(user, rating, book, query):
    global users
    global books
    global ratings
    if(user):
        with open("user_data.data", "r") as userData:
            for line in userData:
                data = line.strip("\n")
                data = data.split("/")
                if(query[0] == data[0]):
                    print("Error: Username taken")
                    return -1
            queryFormat = formatData(query)
        with open("user_data.data", "a") as userData:
            userData.write(queryFormat)
            users += 1
    elif(book):
        with open("book_data.data", "r") as bookData:
            for line in bookData:
                data = line.strip("\n")
                data = data.split("/")
                if(query[1] == data[1]):
                    print("Error: Book already exists")
                    return -1
            queryFormat = formatData(query)
        with open("book_data.data", "a") as bookData:
            bookData.write(queryFormat)
            books += 1
    elif(rating):
        overwrite = False
        with open("ratings_data.data", "r") as ratingData:
            for line in ratingData:
                data = line.strip("\n")
                data = data.split("/")
                if(data[0] == query[0] and data[1] == query[1]):
                    overwrite = True
            queryFormat = formatData(query)
        if(not overwrite):
            with open("ratings_data.data", "a") as ratingData:
                ratingData.write(queryFormat)
                ratings += 1
        else:
            delData(False, True, False, query)
            with open("ratings_data.data", "a") as ratingData:
                ratingData.write(queryFormat)
                ratings += 1
            
                
    return 0

def delData(user, rating, book, query):
    global users
    global books
    global ratings
    if(user):
        with open("user_data.data", "r") as userData:
            lines = userData.readlines()
        with open("user_data.data", "w") as userData:
            for line in lines:
                data = line.strip("\n")
                data = data.split("/")
                if(not data[0] == query[0]):
                    userData.write(line)
                else:
                    users -= 1
    elif(book):
        with open("book_data.data", "r") as bookData:
            lines = bookData.readlines()
        with open("book_data.data", "w") as bookData:
            for line in lines:
                data = line.strip("\n")
                data = data.split("/")
                if(not data[1] == query[1]):
                    bookData.write(line)
                else:
                    books -= 1
    elif(rating):
        with open("ratings_data.data", "r") as ratingData:
            lines = ratingData.readlines()
        with open("ratings_data.data", "w") as ratingData:
            for line in lines:
                data = line.strip("\n")
                data = data.split("/")
                if(not data[0] == query[0] or not data[1] == query[1]):
                    ratingData.write(line)
                else:
                    ratings -= 1
    return 0

def getData(user, rating, book, query):
    if(user):
        with open("user_data.data", "r") as userData:
            for line in userData:
                data = line.strip("\n")
                data = data.split("/")
                if(query == data[0]):
                    return (data[0],data[1],data[2])
    elif(book):
        with open("book_data.data", "r") as bookData:
            for line in bookData:
                data = line.strip("\n")
                data = data.split("/")
                if(query == data[1]):
                    return (data[0],data[1],data[2])
    elif(rating):
        with open("ratings_data.data", "r") as ratingData:
            for line in ratingData:
                data = line.strip("\n")
                data = data.split("/")
                if(data[0] == query[0] and data[1] == query[1]):
                    return (data[0],data[1],data[2])
        
def createUser(userName, password, passwordRepeat):
    if(userName == ""):
        print("Error: Invalid username")
        return -1
    if(not password == passwordRepeat):
        print("Error: Passwords do not match")
        return -1
    
    res = addData(True, False, False, (userName,password,[]))
    return res

def createRating(userName, bookTitle, rating):
    if(rating > 10 or rating < 0):
        print("Error: Rating not in available range")
        return -1
    userExists = False
    with open("user_data.data", "r") as userData:
        for line in userData:
            user = line.strip("\n")
            user = user.split("/")
            if(userName == user[0]):
                userExists = True
        if(not userExists):
            print("Error: The user in question does not exist")
            return -1
        
    bookExists = False
    with open("book_data.data", "r") as bookData:
        for line in bookData:
            book = line.strip("\n")
            book = book.split("/")
            if(bookTitle == book[1]):
                bookExists = True
        if(not bookExists):
            print("Error: The book in question does not exist")
            return -1
            
    res = addData(False, True, False, (userName,bookTitle,rating))
    return res

def addBook(bookTitle, bookGenre):
    bookID = books + 1
    
    res = addData(False, False, True, (bookID, bookTitle, bookGenre))
    return res
    
"""  
addBook("Sci-fi1", "Sci-fi,Comedy")
addBook("Sci-fi2", "Sci-fi")
addBook("Comedy1", "Comedy")
addBook("History1","History")
print()
createUser("1", "pass", "pass")
createUser("2", "pass", "pass")
createUser("3", "pass", "pass")
createUser("4", "pass", "pass")  
createUser("5", "pass", "pass")
createUser("6", "pass", "pass")
print()
createRating("1", "Sci-fi1", 7)
createRating("1", "Sci-fi1", 10)
createRating("2", "Sci-fi1", 7) 
createRating("4", "History1", 8)
createRating("6", "History1", 8)
createRating("7", "History1", 8)
createRating("6", "History2", 8)
createRating("2", "Sci-fi1", 1)    
createRating("2", "Sci-fi1", 2)
"""













    
    
    
    
    
    