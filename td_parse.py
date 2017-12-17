import praw
from DB.base import Base, engine, User, Comment, Post
from datetime import datetime
from sqlalchemy.orm import sessionmaker
import yaml
import tqdm
import time

APP_PARAMS_FILE = 'params.yaml'
WAIT_TIME = 900

app_params = yaml.load(open(APP_PARAMS_FILE, 'r'))

def get_reddit_instance(login_params):
    reddit = praw.Reddit(client_id=login_params['client_id'],
                         client_secret=login_params['secret'],
                         user_agent='my user agent')
    return reddit

def get_session():
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()
    return session

def get_comments(sub):
    sub.comments.replace_more(limit=None)
    for comment in sub.comments.list():
        if not type(comment) == praw.models.reddit.more.MoreComments:
            comm = Comment()
            comm.idx = comment.id
            comm.score = comment.score
            comm.creatd = comment.created

            yield comm, comment

def get_author(comment, users):
    if comment.author:

        if comment.author.name in users:

            user = users[users.index(comment.author.name)]
            user.num_comments += 1
            user.submissions = user.submissions
        else:
            user = User()
            user.name = comment.author.name
            user.num_comments = 1
            user.submissions = 0
        user.last_seen = datetime.now()
        return user

def get_sub_author(comment, users):
    if comment.author:

        if comment.author.name in users:

            user = users[users.index(comment.author.name)]
            user.submissions += 1
        else:
            user = User()
            user.name = comment.author.name
            user.num_comments = 0
            user.submissions = 1
        user.last_seen = datetime.now()
        return user

def wait(wait_time):
    for _ in tqdm.trange(wait_time):
        time.sleep(1)

def main_loop():

    session = get_session()
    reddit = get_reddit_instance(app_params)
    import time
    while True:
        print('Beginning iteration')
        start = time.time()
        for submission in reddit.subreddit('the_donald').hot(limit=25):

            users = session.query(User).all()
            comments = session.query(Comment).all()
            posts = session.query(Post).all()
            if submission.id not in posts:
                author = get_sub_author(submission, users)
                if author not in users:
                    session.add(author)
                post = Post()
                post.idx = submission.id
                post.title = submission.title
                session.add(post)
            for comment, raw_comment in get_comments(submission):
                if comment not in comments:
                    user = get_author(raw_comment, users)
                    #print(raw_comment.__dict__.keys())
                    #input()
                    if user:
                        user.comment.append(comment)
                        session.add(user)


            session.commit()

        print('Finished iteration, pausing {}sec, completed in {}s'.format(WAIT_TIME, time.time() - start))
        wait(WAIT_TIME)

if __name__ == '__main__':
    main_loop()



