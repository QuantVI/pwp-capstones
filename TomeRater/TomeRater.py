# User class.
    # Tome Rater object contains Users
class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = str(email)
        self.books = {}

    def get_email(self):
        # print(self.email)
        return self.email

    def change_email(self, address):
        self.email = str(address)
        print("User {}'s email is now {}".format(self.name,self.email))

    def __repr__(self):
        return "User : {}\nEmail: {}\nBooks: {}".format(
            self.name,self.email,len(self.books))

    def __eq__(self, other_user):
        return (other_user.name == self.name and
        other_user.email == self.email)
    # More methods
    def read_book(self,book,rating=None):
        self.books[book] = rating
    def get_arverage_rating(self):
        if self.books:
            all_r = [self.books[b_key] for b_key in self.books]
            int_r = [num_rating for num_rating in all_r if num_rating != None]
            s = sum(int_r)
            avg = s/len(int_r)
            return avg
        else:
            return "{uzr} hasn't read any books.".format(uzr=self.name)


# Book class.
    # Tome Rater object contains Books
    # Books also within User object. (Users "read" books)

class Book:
    def __init__(self,title,isbn):
        self.title = title
        self.isbn = int(isbn)
        self.ratings = []
        self.__ratings = {}

    def __hash__(self):
        return hash((self.title.lower(), self.isbn))

    def __eq__(self, other_book):
        return self.__hash__() == other_book.__hash__()
    
    #def __repr__(self):
    #    return "Book: {tt} , ISBN: {bn}".format(tt=self.title,bn=self.isbn)

    def get_title(self):
        return self.title
    def get_isbn(self):
        return self.isbn
    def set_isbn(self,new_isbn):
        self.isbn = int(new_isbn)
        abbr = ''.join([word[0] for word in self.title.split()])
        print('The ISBN for {} is now {}'.format(abbr, self.isbn))

    # I feel like Books should be able to keep track of who
    # gave a rating. Thus added additional functionality.
        # extra, takes unlimited User objects as the person
        # or people giving thar rating.
        # When omitted, rating is considered done by the "system"
        # e.g. add_rating(4, pen)
    def add_rating(self, rating, *users):
        """Extra: Takes unlimited Users (by name), as the person
        or people giving that rating.
        When omitted, rating is considered done by the "system".
        
        Examples:
        thisBook.add_rating(4) 
            # add 4 to ratings, System under 4 in __ratings
        thisBook.add_rating(3, johndoe)
            # add 3 to ratings, johndoe under 3 in __ratings
        thisBook.add_rating(2, jack,jill)
            # add 3 to ratings twice, jack and jill under 3 in __ratings 

        Allows function to be used as in the docs, but
        a separate __ratings variable is tracked with the
        related Users.
        As I'm writing htis, I realize that maybe the Book
        should call User.rating on the User at once. Nice!
        """
        if (rating == None or (rating >= 0 and rating <= 4)):
            # basic use
            if not users:
                sys = User('System',"WinDosX@local.host")
                users = [sys]
            else:
                for uzr in users:
                    self.ratings.append(rating)
                    if rating in self.__ratings.keys():
                        self.__ratings[rating].append(uzr)
                    else:
                        self.__ratings[rating] = [uzr]

                    # this might not work.
                    # inifnite loop? this book not ready?
                    #uzr.read_book(self,rating)
        else:
            print("\n\tInvalid Rating\n")
    
    def get_arverage_rating(self):
        s = 0
        for r in self.ratings: s += r
        return s/len(self.ratings)

class Fiction(Book):
    def __init__(self,title,author,isbn):
        super().__init__(title,isbn)
        self.author = author
    def get_author(self):
        return str(self.author)
    def __repr__(self):
        return "{} by {}".format(self.title,self.author)

class Non_Fiction(Book):
    def __init__(self,title,subject,level,isbn):
        super().__init__(title,isbn)
        self.subject = subject
        self.level = level
    def get_subject(self):
        return str(self.subject)
    def get_level(self):
        return str(self.level)
    def __repr__(self):
        return "{} , a {} manual on {}".format(self.title,self.level,self.subject)



#   ----    main object ----
#   ----    ----    ----
class TomeRater:
    def __init__(self):
        # an empty dictionary that will map a user’s email 
        #   to the corresponding User object
        self.users = {}
        # an empty dictionary that will map a Book object 
        #   to the number of Users that have read it
        self.books = {}
    # whenever we make a new book, we should call this method to add it
    #   to self.books, checking to see if it's there
    # This method doubles to add a book with 1 as the read count
    #   when we call add_book_to_user on an unknown book
    def book_creation(self,book_object,via_user=False):
        if via_user:
            # for some reason "not in" does not compare the book hashes
            #   via the eq method

            #if book_object.__hash__() not in [x.__hash__() for x in self.books.keys()]:
            if book_object not in self.books.keys():
                self.books[book_object] = 1
            # book existed and now another read it
            #   so we add 1 to its read count
            else:
                self.books[book_object] +=1
        else: 
            if book_object not in self.books.keys():
                self.books[book_object] = 0

    def create_book(self,title,isbn):
        b = Book(title,isbn)
        #self.book_creation(b)
        return b

    def create_novel(self,title,author,isbn):
        b = Fiction(title,author,isbn)
        self.book_creation(b)
        return b

    def create_non_fiction(self,title,subject,level,isbn):
        b = Non_Fiction(title,subject,level,isbn)
        self.book_creation(b)
        return b
    
    # stuff for Users
    def user_creation(self,uzr_obj):
        this_uzr_em = uzr_obj.get_email()
        if this_uzr_em in self.users.keys():
            pass
        else:
            self.users[this_uzr_em] = uzr_obj


    def add_book_to_user(self,book,email,rating=None):
        if email in self.users.keys():
            uzr = self.users[email]
            uzr.read_book(book,rating)
            book.add_rating(rating)
            self.book_creation(book,via_user=True)
        else:
            print("No user with email {em}".format(em=email))
    
    def add_user(self,name,email, user_books=None):
        nuzr = User(name,email)
        self.user_creation(nuzr)
        if user_books:
            for a_book in user_books:
                self.add_book_to_user(a_book,email)
    
    # Analysis Methods
    def print_catalog(self):
        for bb in self.books:
            print(bb,sep='\n')

    def print_users(self):
        for em in self.users:
            print (self.users[em],sep='\n')
    
    def most_read_book(self):
        mx = max(self.books.values())
        mostrb = [this for this in self.books if self.books[this]==mx]
        if len(mostrb) != 1:
            print("There are {sz} books tied for most read".format(len(mostrb)))
        return mostrb[0]
    
    def highest_rated_book(self):
        each_avg = [(ab.get_arverage_rating(), ab) for ab in self.books]
        mx_avg = max([elem[0] for elem in each_avg])
        mxi = [elem[0] for elem in each_avg].index(mx_avg)
        hrb = each_avg.index(mxi)[1]
        return hrb
    
    def most_positive_user(self):
        # users is a dict where k:v is email:UserObject
        # within UserObject books is a dict where k:v is BookObj:rating
        each_avg = [(self.users[em].get_arverage_rating(), self.users[em]) for em in self.users]
        mx_avg = max([elem[0] for elem in each_avg])
        mxi = [elem[0] for elem in each_avg].index(mx_avg)
        mpu = each_avg.index(mxi)[1]
        return mpu
