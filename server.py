# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 21:57:46 2019

@author: Erdal Guclu
"""

#books stored as bookID, bookTitle, bookGenre
global books
books = 0 #no of books
#ratings stored as userName, bookID, bookRating
global ratings
ratings = 0 #no of ratings
#users stored as userName, password, profile
global users
users = 0 #no of users

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
        overwrite = False
        with open("user_data.data", "r") as userData:
            for line in userData:
                data = line.strip("\n")
                data = data.split("/")
                if(query[0] == data[0]):
                    overwrite = True
            queryFormat = formatData(query)
        if(not overwrite):
            with open("user_data.data", "a") as userData:
                userData.write(queryFormat)
                users += 1
        else:
            delData(True, False, False, query)
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
        return None
    if(not password == passwordRepeat):
        print("Error: Passwords do not match")
        return None
    with open("user_data.data", "r") as userData:
        for line in userData:
            data = line.strip("\n")
            data = data.split("/")
            if(userName == data[0]):
                print("Error: Username taken")
                return None
    addData(True, False, False, (userName,password,[[]])) 
    #last element is the profile - first item is History
    return (userName,password,[[]])

def createRating(userName, bookTitle, rating):
    if(rating > 10 or rating < 0):
        print("Error: Rating not in available range")
        return None
    userExists = False
    with open("user_data.data", "r") as userData:
        for line in userData:
            user = line.strip("\n")
            user = user.split("/")
            if(userName == user[0]):
                userExists = True
        if(not userExists):
            print("Error: The user in question does not exist")
            return None
        
    bookExists = False
    with open("book_data.data", "r") as bookData:
        for line in bookData:
            book = line.strip("\n")
            book = book.split("/")
            if(bookTitle == book[1]):
                bookExists = True
        if(not bookExists):
            print("Error: The book in question does not exist")
            return None
            
    res = addData(False, True, False, (userName,bookTitle,rating))
    res = updateUserHistory(userName)
    return res

def deleteRating(userName, bookTitle):
    bookExists = False
    with open("book_data.data", "r") as bookData:
        for line in bookData:
            book = line.strip("\n")
            book = book.split("/")
            if(bookTitle == book[1]):
                bookExists = True
        if(not bookExists):
            print("Error: The book in question does not exist")
            return None
            
    res = delData(False, True, False, (userName,bookTitle))
    res = updateUserHistory(userName)
    return res

def addBook(bookTitle, bookGenre):
    bookID = books + 1
    
    res = addData(False, False, True, (bookID, bookTitle, bookGenre))
    return res

def updateUserHistory(userName):
    history = []
    with open("ratings_data.data", "r") as ratingData:
            for line in ratingData:
                data = line.strip("\n")
                data = data.split("/")
                if(data[0] == userName):
                    history.append((data[1],data[2]))
    
    query = None
    with open("user_data.data", "r") as userData:
        for line in userData:
            user = line.strip("\n")
            user = user.split("/")
            if(userName == user[0]):
                query = [user[0],user[1],[history]]
    
    addData(True, False, False, query)
    return history
    

def getBookRatings(bookTitle):
    ratingList = []
    with open("ratings_data.data", "r") as ratingData:
        for line in ratingData:
            data = line.strip("\n")
            data = data.split("/")
            if(data[1] == bookTitle):
                ratingList.append((data[0],data[2]))
    
    return ratingList

def getAverageRating(bookTitle):
    ratingList = getBookRatings(bookTitle)
    total = 0
    for rating in ratingList:
        total += int(rating[1])
    if(len(ratingList) != 0):
        average = total // len(ratingList)
        return average
    return 0

def getBookScore(userName, bookTitle):
    userHistories = {} #other users
    userHistory = [] #target user
    with open("user_data.data", "r") as userData:
        for line in userData:
            user = line.strip("\n")
            user = user.split("/")
            if(userName == user[0]):
                if(user[2] == "[[]]"):
                    userHistory = [[]]
                else:
                    temp = user[2].strip("[")
                    temp = temp.strip("]")
                    temp = temp.split("), (")
                    temp[-1] = temp[-1].strip(")")
                    temp[0] = temp[0].strip("(")      
                    for i in range(len(temp)):
                        temp[i] = temp[i].split(", ")
                        temp[i] = [temp[i][0].strip("'"), temp[i][1].strip("'")]
                    userHistory = temp
            else:
                if(user[2] == "[[]]"):
                    userHistories[user[0]] = [[]]
                else:
                    temp = user[2].strip("[")
                    temp = temp.strip("]")
                    temp = temp.split("), (")
                    temp[-1] = temp[-1].strip(")")
                    temp[0] = temp[0].strip("(")  
                    for i in range(len(temp)):
                        temp[i] = temp[i].split(", ")
                        temp[i] = [temp[i][0].strip("'"), temp[i][1].strip("'")]
                    userHistories[user[0]] = temp
    
    userSimilarity = []
    booksRated = []
    
    for rating in userHistory:
        if(rating == []):
            break
        booksRated.append(rating[0])
    
    score = 0
    if(booksRated != []):
        for user in userHistories:    
            totalBooks = len(booksRated)
            history = userHistories[user]
            neighbourVisits = []
            for rating in history:
                if(history == [[]]):
                    break
                neighbourVisits.append(rating[0])
            match = 0
            if(neighbourVisits == []):
                userSimilarity.append((user[0], 0))
            else:
                for book in neighbourVisits:
                    if(book in booksRated):
                        match += 1
                    else:
                        totalBooks += 1
                similarity = match / totalBooks
                userSimilarity.append((user[0], similarity))
                
        targetBook = getData(False, False, True, bookTitle)
        targetGenres = targetBook[2].split(",")
        genreWeight = 1 / len(targetGenres)
        
        #consider target user
        for rating in userHistory:
            if(rating[0] == bookTitle):
                continue
            else:
                bookRating = rating[1]
                book = getData(False, False, True, rating[0])
                bookGenres = book[2].split(",")
                for genre in bookGenres:
                    if(genre in targetGenres):
                        score += (int(bookRating) * genreWeight)
    
        #consider other users           
        for user in userHistories:
            history = userHistories[user]
            similarityWeight = 0
            for pair in userSimilarity:
                if(user[0] == pair[0]):
                    similarityWeight = pair[1]
            for rating in history:
                if(history == [[]]):
                    break
                book = getData(False, False, True, rating[0])
                bookGenres = book[2].split(",")
                for genre in bookGenres:
                    if(genre in targetGenres):
                        score += (int(bookRating) * genreWeight * similarityWeight)
    
    if(score <= 0): #lack of information so base off of averages
        score = getAverageRating(bookTitle) * 0.05 #multiplier ensures that books that can be recommended from data are prioritized
        
    return score

def getRecommendations(userName):
    allBooks = []
    booklist = []
    with open("book_data.data", "r") as bookData:
        for line in bookData:
            book = line.strip("\n")
            book = book.split("/")
            allBooks.append([book,0])
            booklist.append(book)
    for i in range(len(booklist)):
        score = getBookScore(userName, booklist[i][1])
        allBooks[i][1] = score
    
    recommendations = []
    bestBook = ("", 0)
    for k in range(10):
        if(len(allBooks) == 0):
            break
        j = 0
        for i in range(len(allBooks)):
            if(allBooks[i][1] >= bestBook[1]):
                bestBook = (booklist[i][1], allBooks[i][1])
                j = i
        recommendations.append(bestBook)
        del allBooks[j]
        del booklist[j]
        bestBook = ("", 0)
        
    return recommendations        

with open("book_data.data") as bookData:
    for line in bookData:
        books += 1
        
with open("ratings_data.data") as ratingData:
    for line in ratingData:
        ratings += 1
        
with open("user_data.data") as userData:
    for line in userData:
        users += 1
        data = line.strip("\n")
        data = data.split("/")
        updateUserHistory(data[0])

global user
def main():
    global user
    print("Book Recommender System Ready")
    user = None
    loggedIn = False
    running = True
    while(running):
        if(not loggedIn):
            choice = input("Enter 'login' to login to an existing account or 'register' to create a new one or 'x' to terminate: ")
            if(choice.lower() == "login"):
                userName = input("Please enter username: ")
                with open("user_data.data", "r") as userData:
                    for line in userData:
                        data = line.strip("\n")
                        data = data.split("/")
                        if(userName == data[0]):
                            user = data
                            loggedIn = True
                            print("You are logged in as %s" % data[0])
                            break
                if(user == None):
                    print("Error: User specified does not exist")
                    continue
            elif(choice.lower() == "register"):
                userName = input("Please enter username: ")
                user = createUser(userName, "pass", "pass")
                if(user == None):
                    continue
                else:
                    loggedIn = True
                    print("Account " + user[0] + " successfully created")
            elif(choice.lower() == "x"):
                running = False
                print("Shutting down")
                continue
            else:
                choice = None
                print("Error: Command not recognized")
                continue
        
        print()
        print("Enter 'addrating' to rate a book, 'delrating' to delete your rating, 'recommend' to view recommendations,...")
        choice = input("...'viewratings' to view own ratings, 'x' to terminate, 'logout' to logout: ")
        if(choice.lower() == "addrating"):
            bookTitle = input("Enter title of book to rate: ")
            rating = int(input("Enter rating for the book in inteval (inclusive) 1-10: "))
            res = createRating(user[0], bookTitle, rating)
            if(res == None):
                continue
            else:
                print("Rating successfully submitted")
        if(choice.lower() == "delrating"):
            bookTitle = input("Enter title of book to delete rating for: ")
            res = deleteRating(user[0],bookTitle)
            if(res == None):
                continue
            else:
                print("Rating successfully deleted")
        elif(choice.lower() == "recommend"):
            recommendations = getRecommendations(user[0])
            print("Top 10 Recommendations:")
            print()
            for i in range(len(recommendations)):
                string = str(i+1)
                string += ": %s with score %.2f" % (recommendations[i][0], recommendations[i][1])
                print(string)
        elif(choice.lower() == "viewratings"):
            print("Your ratings: ")
            print()
            hasRatings = False
            with open("ratings_data.data", "r") as ratingData:
                for line in ratingData:
                    data = line.strip("\n")
                    data = data.split("/")
                    if(data[0] == user[0]):
                        hasRatings = True
                        print("Book: " + data[1] + " Rating: " + data[2])
            if(not hasRatings):
                print("You have not submitted any ratings")
        elif(choice.lower() == "x"):
            running = False
            print("Shutting down")
            continue
        elif(choice.lower() == "logout"):
            user = None
            loggedIn = False
            print("Logged out")
            continue
        else:
            choice = None
            print("Error: Command not recognized")
            continue            
          
if __name__ == '__main__':
    main()

#starting sample data
"""
addBook("Sci-fi1", "Sci-fi,Comedy")
addBook("Sci-fi2", "Sci-fi")
addBook("Fantasy1", "Fantasy")
addBook("Fantasy2", "Fantasy")
addBook("Sci-fi3", "Sci-fi,Romance")
addBook("Comedy1", "Comedy")
addBook("Romance1", "Romance")
addBook("Romance2", "Romance,Comedy")
addBook("History1", "History")
addBook("Detective1", "Detective")
addBook("Detective2", "Detective")
addBook("Drama1", "Drama")
addBook("Drama2", "Drama,Sci-fi")
print()
createUser("1", "pass", "pass")
createUser("2", "pass", "pass")
createUser("3", "pass", "pass")
createUser("4", "pass", "pass")  
createUser("5", "pass", "pass")
createUser("6", "pass", "pass")
print()
createRating("1", "Sci-fi1", 10)
createRating("1", "Sci-fi2", 8)
createRating("1", "Romance1", 2)
createRating("1", "Fantasy1", 6)

createRating("2", "Sci-fi1", 7) 
createRating("2", "Sci-fi2", 6)
createRating("2", "Detective1", 8)

createRating("4", "History1", 8)

createRating("6", "History1", 8)
createRating("6", "Detective1", 10)

createRating("5", "Drama1", 4)    
createRating("5", "Drama2", 7)
"""





    
    
    
    
    
    