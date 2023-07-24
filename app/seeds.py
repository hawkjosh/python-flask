from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import datetime, timedelta

app = Flask(__name__)

DB_URI = "mysql+mysqlconnector://{user}:{password}@{host}/{dbname}".format(
    user="root", password="password", host="localhost", dbname="python_flask"
)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from app import User, Comment, Reply, Like

# def random_date(start, end):
#     delta = end - start
#     random_days = random.randint(0, delta.days)
#     return start + timedelta(days=random_days)

with app.app_context():
    user1 = User(username='ChopHouse51')
    user1.set_password('password')
    user2 = User(username='SilverArrow87')
    user2.set_password('password')
    user3 = User(username='BookWorm42')
    user3.set_password('password')
    user4 = User(username='CodeKing99')
    user4.set_password('password')
    db.session.add_all([user1, user2, user3, user4])
    db.session.commit()
    
    # start_date = datetime(2022, 7, 1)
    # end_date = datetime(2023, 7, 1)

    comment1 = Comment(content='Bought a new acoustic guitar today! Any good recommendations for strings? I typically use a lighter gauge but they tend to break.', user=user1, created_at=datetime(2022, 7, 25, 0, 0, 0), updated_at=datetime(2022, 7, 25, 0, 0, 0))
    comment2 = Comment(content='Started a new yoga routine, and it\'s been incredibly rejuvenating! The combination of stretching and mindfulness has helped me find balance in my daily life.', user=user3, created_at=datetime(2022, 8, 8, 0, 0, 0), updated_at=datetime(2022, 8, 8, 0, 0, 0))
    comment3 = Comment(content='Just got home from a Braves/Mets thriller! The atmosphere in the stadium was electric, and Olsen\'s two-run walkoff in the ninth was unforgettable. Go Braves!!', user=user1, created_at=datetime(2022, 9, 28, 0, 0, 0), updated_at=datetime(2022, 9, 28, 0, 0, 0))
    comment4 = Comment(content='Just got my hands on the new iPhone, and I\'m loving it! The camera quality is outstanding, and the Face ID works like magic.', user=user4, created_at=datetime(2022, 10, 12, 0, 0, 0), updated_at=datetime(2022, 10, 12, 0, 0, 0))
    comment5 = Comment(content='Started a new fitness routine, and I can already feel the difference! Incorporating strength training along with cardio has really boosted my energy levels.', user=user4, created_at=datetime(2023, 1, 3, 0, 0, 0), updated_at=datetime(2023, 1, 3, 0, 0, 0))
    comment6 = Comment(content='Just finished reading \'The Great Gatsby,\' and it\'s now one of my all-time favorite books! The writing style and the depiction of the Jazz Age were mesmerizing.', user=user3, created_at=datetime(2023, 1, 9, 0, 0, 0), updated_at=datetime(2023, 1, 9, 0, 0, 0))
    comment7 = Comment(content='Just watched the latest Marvel movie, and it was mind-blowing! The action sequences were epic, and the storyline kept me hooked throughout.', user=user2, created_at=datetime(2023, 1, 18, 0, 0, 0), updated_at=datetime(2023, 1, 18, 0, 0, 0))
    comment8 = Comment(content='Tried a new recipe for homemade pizza, and it turned out delicious! The crust was crispy, and the toppings were perfectly balanced.', user=user2, created_at=datetime(2023, 2, 14, 0, 0, 0), updated_at=datetime(2023, 2, 14, 0, 0, 0))
    comment9 = Comment(content='I recently visited Paris, and it was a dream come true! The Eiffel Tower was even more breathtaking in person. Can\'t wait to explore more of Europe next!', user=user4, created_at=datetime(2023, 2, 17, 0, 0, 0), updated_at=datetime(2023, 2, 17, 0, 0, 0))
    comment10 = Comment(content='Attended a live concert last night, and it was an unforgettable experience! The energy of the crowd and the performer\'s talent made it an incredible night.', user=user2, created_at=datetime(2023, 3, 16, 0, 0, 0), updated_at=datetime(2023, 3, 16, 0, 0, 0))
    comment11 = Comment(content='Went deep sea fishing on our trip last week, and it was so much fun! Caught a variety of fish, and the view of the open ocean was pretty amazing.', user=user1, created_at=datetime(2023, 5, 12, 0, 0, 0), updated_at=datetime(2023, 5, 12, 0, 0, 0))
    comment12 = Comment(content='Just returned from a backpacking trip in Southeast Asia, and it was an adventure of a lifetime! From pristine beaches to vibrant cities, every moment was unforgettable.', user=user3, created_at=datetime(2023, 6, 14, 0, 0, 0), updated_at=datetime(2023, 6, 14, 0, 0, 0))
    
    db.session.add_all([comment1, comment2, comment3, comment4, comment5, comment6, comment7, comment8, comment9, comment10, comment11, comment12])
    db.session.commit()

    reply1 = Reply(content='Congrats on the new guitar! When it comes to strings, I understand your concern about lighter gauges breaking. You might want to try a set of high-quality coated strings. They tend to be more durable while still offering a comfortable playability. I\'ve had great experiences with Martin coated strings and they strike a good balance between tone and longevity.', user=user2, comment=comment1, created_at=datetime(2022, 8, 17, 0, 0, 0), updated_at=datetime(2022, 8, 17, 0, 0, 0))
    reply2 = Reply(content='Awesome choice on getting a new acoustic guitar! For lighter gauge strings that are less prone to breaking, you could check out D\'Addario\'s \'phosphor bronze\' series. They offer a warm tone and are known for their reliability. Another option could be Ernie Ball \'80/20 bronze\' strings, which also sound great and have good durability. Happy strumming!', user=user4, comment=comment1, created_at=datetime(2022, 8, 20, 0, 0, 0), updated_at=datetime(2022, 8, 20, 0, 0, 0))
    reply3 = Reply(content='Thanks for the string recommendations! I went with the \'80/20 bronze\' but from D\'Addario rather than Ernie Ball. Couldn\'t be happier!', user=user1, comment=comment1, created_at=datetime(2022, 8, 25, 0, 0, 0), updated_at=datetime(2022, 8, 25, 0, 0, 0))
    reply4 = Reply(content='I was at the game too, and it was absolutely incredible! The energy in the stadium was unlike anything I\'ve experienced before. Olsen\'s walkoff had me jumping out of my seat! #GoBraves', user=user2, comment=comment3, created_at=datetime(2022, 9, 29, 0, 0, 0), updated_at=datetime(2022, 9, 29, 0, 0, 0))
    reply5 = Reply(content='Couldn\'t agree more! That game was a rollercoaster of emotions. As a Mets fan, I was hoping for a different outcome, but you can\'t deny the excitement and drama. Congratulations to the Braves on a hard-fought victory!', user=user3, comment=comment3, created_at=datetime(2022, 9, 30, 0, 0, 0), updated_at=datetime(2022, 9, 30, 0, 0, 0))
    reply6 = Reply(content='Congratulations on the new iPhone! I\'ve been thinking of upgrading mine as well. How\'s the battery life on the new model?', user=user2, comment=comment4, created_at=datetime(2022, 10, 14, 0, 0, 0), updated_at=datetime(2022, 10, 14, 0, 0, 0))
    reply7 = Reply(content='Thanks! So far, the battery is much better than my last iPhone. I used to have to charge a few times a day but now I can go the whole day on an overnight charge.', user=user4, comment=comment4, created_at=datetime(2022, 10, 14, 0, 0, 0), updated_at=datetime(2022, 10, 14, 0, 0, 0))
    reply8 = Reply(content='I\'m glad to hear that yoga is benefiting you! It\'s a great way to relieve stress and improve flexibility.', user=user2, comment=comment2, created_at=datetime(2022, 10, 23, 0, 0, 0), updated_at=datetime(2022, 10, 23, 0, 0, 0))
    reply9 = Reply(content='I\'m glad to hear that! Fitness routines can make a huge difference in overall well-being. Don\'t forget to take rest days to let your body recover properly.', user=user3, comment=comment5, created_at=datetime(2023, 1, 5, 0, 0, 0), updated_at=datetime(2023, 1, 5, 0, 0, 0))
    reply10 = Reply(content='I love \'The Great Gatsby\' too! If you enjoy that era, I highly recommend reading \'The Sun Also Rises\' by Ernest Hemingway.', user=user2, comment=comment6, created_at=datetime(2023, 1, 9, 0, 0, 0), updated_at=datetime(2023, 1, 9, 0, 0, 0))
    reply11 = Reply(content='I\'ve read a lot of Hemingway\'s work but never \'The Sun Also Rises\'. I\'ll have to check it out, thanks!', user=user3, comment=comment6, created_at=datetime(2023, 1, 11, 0, 0, 0), updated_at=datetime(2023, 1, 11, 0, 0, 0))
    reply12 = Reply(content='I\'m a huge Marvel fan too! Which movie was it? I\'m excited to catch up on the latest releases.', user=user3, comment=comment7, created_at=datetime(2023, 1, 21, 0, 0, 0), updated_at=datetime(2023, 1, 21, 0, 0, 0))
    reply13 = Reply(content='Marvel movies are always a treat. If you loved that one, make sure to watch the post-credit scenes. They often tease upcoming movies or provide extra context.', user=user4, comment=comment7, created_at=datetime(2023, 1, 22, 0, 0, 0), updated_at=datetime(2023, 1, 22, 0, 0, 0))
    reply14 = Reply(content='Homemade pizza is the best! Did you experiment with any crazy toppings or stick to the classics?', user=user1, comment=comment8, created_at=datetime(2023, 2, 18, 0, 0, 0), updated_at=datetime(2023, 2, 18, 0, 0, 0))
    reply15 = Reply(content='That book is a classic for a reason! Do you have any other recommendations for similar literary works?', user=user4, comment=comment6, created_at=datetime(2023, 2, 23, 0, 0, 0), updated_at=datetime(2023, 2, 23, 0, 0, 0))
    reply16 = Reply(content='That sounds amazing! Mind sharing the recipe or any special tips you used? I\'d love to give it a try.', user=user3, comment=comment8, created_at=datetime(2023, 2, 25, 0, 0, 0), updated_at=datetime(2023, 2, 25, 0, 0, 0))
    reply17 = Reply(content='Glad you enjoyed Paris! If you\'re planning to visit Italy, make sure to visit Rome. The Colosseum is a must-see, and the food is incredible!', user=user1, comment=comment9, created_at=datetime(2023, 2, 28, 0, 0, 0), updated_at=datetime(2023, 2, 28, 0, 0, 0))
    reply18 = Reply(content='Paris is indeed a beautiful city! Did you get a chance to visit the Louvre Museum? The art collection there is amazing.', user=user3, comment=comment9, created_at=datetime(2023, 3, 1, 0, 0, 0), updated_at=datetime(2023, 3, 1, 0, 0, 0))
    reply19 = Reply(content='I did get to see the Louvre. It was incredible!', user=user4, comment=comment9, created_at=datetime(2023, 3, 5, 0, 0, 0), updated_at=datetime(2023, 3, 5, 0, 0, 0))
    reply20 = Reply(content='Live concerts are magical! Who was the performer? I\'m always on the lookout for great live shows to attend.', user=user3, comment=comment10, created_at=datetime(2023, 3, 18, 0, 0, 0), updated_at=datetime(2023, 3, 18, 0, 0, 0))
    reply21 = Reply(content='It was a local band called Boxcar Radio. Not sure if you\'ve heard of them but I\'d definitely recommend catching a show of theirs if you get a chance.', user=user2, comment=comment10, created_at=datetime(2023, 3, 18, 0, 0, 0), updated_at=datetime(2023, 3, 18, 0, 0, 0))
    reply22 = Reply(content='I completely agree! Live music has a way of connecting people. Any favorite songs or moments from the concert?', user=user4, comment=comment10, created_at=datetime(2023, 3, 21, 0, 0, 0), updated_at=datetime(2023, 3, 21, 0, 0, 0))
    reply23 = Reply(content='Sounds like an amazing experience! Deep sea fishing is on my bucket list, and your post just made me even more excited to try it one day. Any tips for a first-timer like me? Tight lines and happy fishing!', user=user3, comment=comment11, created_at=datetime(2023, 5, 15, 0, 0, 0), updated_at=datetime(2023, 5, 15, 0, 0, 0))
    reply24 = Reply(content='Thanks! The biggest piece of advice I would give to a first-timer is to take some motion sickness meds beforehand. It can definitely get a little bit choppy out there and you don\'t want to miserable the whole time.', user=user1, comment=comment11, created_at=datetime(2023, 5, 16, 0, 0, 0), updated_at=datetime(2023, 5, 16, 0, 0, 0))
    reply25 = Reply(content='I love deep sea fishing too! It\'s such a thrill to reel in those big catches from the depths of the ocean. The serenity of being surrounded by the vast open sea is a bonus.', user=user4, comment=comment11, created_at=datetime(2023, 5, 17, 0, 0, 0), updated_at=datetime(2023, 5, 17, 0, 0, 0))
    reply26 = Reply(content='Backpacking in Southeast Asia is incredible! Which countries did you visit? I\'m planning a trip there soon and would love some recommendations.', user=user2, comment=comment12, created_at=datetime(2023, 6, 18, 0, 0, 0), updated_at=datetime(2023, 6, 18, 0, 0, 0))
    reply27 = Reply(content='Wow, backpacking trips are always full of surprises. Did you come across any hidden gems or off-the-beaten-path destinations worth exploring?', user=user4, comment=comment12, created_at=datetime(2023, 7, 21, 0, 0, 0), updated_at=datetime(2023, 7, 21, 0, 0, 0))
    
    db.session.add_all([reply1, reply2, reply3, reply4, reply5, reply6, reply7, reply8, reply9, reply10, reply11, reply12, reply13, reply14, reply15, reply16, reply17, reply18, reply19, reply20, reply21, reply22, reply23, reply24, reply25, reply26, reply27])
    db.session.commit()

    like1 = Like(value=True, user=user2, comment=comment1)
    like2 = Like(value=True, user=user3, comment=comment1)
    like3 = Like(value=True, user=user4, comment=comment1)
    like4 = Like(value=True, user=user2, comment=comment2)
    like5 = Like(value=True, user=user2, comment=comment3)
    like6 = Like(value=True, user=user3, comment=comment3)
    like7 = Like(value=True, user=user4, comment=comment3)
    like8 = Like(value=True, user=user2, comment=comment4)
    like9 = Like(value=True, user=user3, comment=comment4)
    like10 = Like(value=True, user=user3, comment=comment5)
    like11 = Like(value=True, user=user2, comment=comment6)
    like12 = Like(value=True, user=user4, comment=comment6)
    like13 = Like(value=True, user=user3, comment=comment7)
    like14 = Like(value=True, user=user4, comment=comment7)
    like15 = Like(value=True, user=user1, comment=comment9)
    like16 = Like(value=True, user=user2, comment=comment9)
    like17 = Like(value=True, user=user3, comment=comment9)
    like18 = Like(value=True, user=user1, comment=comment10)
    like19 = Like(value=True, user=user3, comment=comment10)
    like20 = Like(value=True, user=user4, comment=comment10)
    like21 = Like(value=True, user=user3, comment=comment11)
    like22 = Like(value=True, user=user4, comment=comment11)
    like23 = Like(value=True, user=user2, comment=comment12)
    like24 = Like(value=True, user=user4, comment=comment12)
    
    db.session.add_all([like1, like2, like3, like4, like5, like6, like7, like8, like9, like10, like11, like12, like13, like14, like15, like16, like17, like18, like19, like20, like21, like22, like23, like24])
    db.session.commit()

print('Data seeded successfully.')