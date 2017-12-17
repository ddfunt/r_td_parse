from td_parse import get_session
from DB.base import User, Comment
import numpy as np

session = get_session()

users = session.query(User).all()

print(users)
print(len(users))
n = [u.num_comments for u in users]
print(min(n), max(n), np.mean(n))

x = [user for user in users if user.submissions > 0]
print(len(x))
for user in x:
    print(user)

print(user.last_seen)