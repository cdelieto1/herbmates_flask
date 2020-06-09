# """CRUD operations."""

from model import db, User, Complex, Description, Inventory, Messaging


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user


# # def add_herb_qty(title, overview, release_date, poster_path):
# #     """Return an addition to the herb qty"""

# #     herb = Inventory(title=title,
# #                   overview=overview,
# #                   release_date=release_date,
# #                   poster_path=poster_path)

# #     db.session.add(movie)
# #     db.session.commit()

# #     return movie


# # def get_movies():
# #     """Return all movies."""

# #     return Inventory.query.all()


# # def create_rating(user, movie, score):
# #     """Create and return a new rating."""

# #     rating = Rating(user=user, movie=movie, score=score)

# #     db.session.add(rating)
# #     db.session.commit()

# #     return rating


def get_herbs_in_inventory():
    """Return all active herbs for a given complex"""

    return Inventory.query.filter(status=1, complex_id=user.complex_id)


def get_user_by_email(email):
    """Return a user by email."""
    return User.query.filter(User.email == email.lower()).first()

def get_user_by_id(user_id):
    return User.query.filter(User.user_id == user_id).first()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
