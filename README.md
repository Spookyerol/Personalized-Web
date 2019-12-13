# Personalized-Web

This system was tested on windows 10 CMD.
In order to run it requires that 3 files share the same directory with server.py:
- book_data.data 	###Stores books as bookID/bookTitle/bookGenres*
- ratings_data.data ###Stores ratings as username/bookTitle/rating(1-10 inclusive)
- user_data.data	###Stores users as username/password**/searchHistory***
All the main fields are separated by "/"
*Books that have multiple Genres separate them with ","
**passwords are placeholders and are not actively used but are important to the format (legacy)
***essentially is the profile of the user with which we keep track of their preferences

To run the program simply navigate to the directory that server.py is at and execute the python
script.
This will initiate a text based interface which will give instructions through prompts and let
the user do various things.
The 3 data files come with a small data sample to help make it easy to test, however can be easily
extended/replaced with a text editor so long as the format of the files is followed.

At the bottom of the source code there are some commented method calls that highlight how to extend
the data.
--------------------------------------------------------------------------------------------------
Features:
- The text interface allows the user to log in to an existing account or create a completely new one
- The user can log out of one account and switch to another one
- The user can view all the ratings that the account has posted
- The user can at will get a top 10 recommendation list based on the recommendation algorithm
- The user can create new ratings and delete old ones

The recommendation algorithm bases its recommendations off of two main factors:
- The ratings history of the user is maintained persistently and ratings and genres of books
  factored in. If a user has rated many sci-fi books, they are likely to be recommended sci-fi
  books. If they rate these books highly, this chance goes up further
- The ratings that others give also effect the recommendations, however their ratings are weighted
  by the laccard coefficient, which provides a measure of similarity in user tastes