from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DB_URI = "mysql+mysqlconnector://{user}:{password}@{host}/{dbname}".format(
    user="root", password="password", host="localhost", dbname="python_flask"
)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from app import User, Comment, Reply, Like

with app.app_context():
    # Create sample users
    user1 = User(username='Wanderlust87')
    user1.set_password('password')
    user2 = User(username='Bookworm42')
    user2.set_password('password')
    user3 = User(username='TechGeek99')
    user3.set_password('password')
    db.session.add_all([user1, user2, user3])
    db.session.commit()

    # Create sample comments
    comment1 = Comment(content='I recently visited Paris, and it was a dream come true! The Eiffel Tower was even more breathtaking in person. Can\'t wait to explore more of Europe next!', user=user1)
    comment2 = Comment(content='Just watched the latest Marvel movie, and it was mind-blowing! The action sequences were epic, and the storyline kept me hooked throughout.', user=user2)
    comment3 = Comment(content='Just finished reading \'The Great Gatsby,\' and it\'s now one of my all-time favorite books! The writing style and the depiction of the Jazz Age were mesmerizing.', user=user3)
    comment4 = Comment(content='Just got my hands on the new iPhone, and I\'m loving it! The camera quality is outstanding, and the Face ID works like magic.', user=user1)
    comment5 = Comment(content='Tried a new recipe for homemade pizza, and it turned out delicious! The crust was crispy, and the toppings were perfectly balanced.', user=user2)
    comment6 = Comment(content='Started a new yoga routine, and it\'s been incredibly rejuvenating! The combination of stretching and mindfulness has helped me find balance in my daily life.', user=user3)
    comment7 = Comment(content='Started a new fitness routine, and I can already feel the difference! Incorporating strength training along with cardio has really boosted my energy levels.', user=user1)
    comment8 = Comment(content='Attended a live concert last night, and it was an unforgettable experience! The energy of the crowd and the performer\'s talent made it an incredible night.', user=user2)
    comment9 = Comment(content='Just returned from a backpacking trip in Southeast Asia, and it was an adventure of a lifetime! From pristine beaches to vibrant cities, every moment was unforgettable.', user=user3)
    db.session.add_all([comment1, comment2, comment3])
    db.session.commit()

    # Create sample replies
    reply1 = Reply(content='I\'m glad you enjoyed Paris! If you\'re planning to visit Italy, make sure to visit Rome. The Colosseum is a must-see, and the food is incredible!', user=user2, comment=comment1)
    reply2 = Reply(content='Paris is indeed a beautiful city! Did you get a chance to visit the Louvre Museum? The art collection there is amazing.', user=user3, comment=comment1)
    reply3 = Reply(content='Congratulations on the new iPhone! I\'ve been thinking of upgrading mine as well. How\'s the battery life on the new model?', user=user2, comment=comment4)
    reply4 = Reply(content='I\'m still using an older iPhone model, but hearing your positive experience makes me excited to try the new one. Enjoy your new gadget!', user=user3, comment=comment4)
    reply5 = Reply(content='That\'s fantastic! Strength training is a game-changer. Have you tried incorporating any specific exercises, like deadlifts or squats?', user=user2, comment=comment7)
    reply6 = Reply(content='I\'m glad to hear that! Fitness routines can make a huge difference in overall well-being. Don\'t forget to take rest days to let your body recover properly.', user=user3, comment=comment7)
    reply7 = Reply(content='I\'m a huge Marvel fan too! Which movie was it? I\'m excited to catch up on the latest releases.', user=user1, comment=comment2)
    reply8 = Reply(content='Marvel movies are always a treat. If you loved that one, make sure to watch the post-credit scenes. They often tease upcoming movies or provide extra context.', user=user3, comment=comment2)
    reply9 = Reply(content='That sounds amazing! Mind sharing the recipe or any special tips you used? I\'d love to give it a try.', user=user1, comment=comment5)
    reply10 = Reply(content='Homemade pizza is the best! Did you experiment with any unique toppings or stick to the classic ones?', user=user3, comment=comment5)
    reply11 = Reply(content='Live concerts are magical! Who was the performer? I\'m always on the lookout for great live shows to attend.', user=user1, comment=comment8)
    reply12 = Reply(content='I completely agree! Live music has a way of connecting people. Any favorite songs or moments from the concert?', user=user3, comment=comment8)
    reply13 = Reply(content='I love \'The Great Gatsby\' too! If you enjoy that era, I highly recommend reading \'The Sun Also Rises\' by Ernest Hemingway.', user=user1, comment=comment3)
    reply14 = Reply(content='That book is a classic for a reason! Do you have any other recommendations for similar literary works?', user=user2, comment=comment3)
    reply15 = Reply(content='Yoga is fantastic for both the body and mind. Have you tried any specific styles like Hatha or Vinyasa?', user=user1, comment=comment6)
    reply16 = Reply(content='I\'m glad to hear that yoga is benefiting you! It\'s a great way to relieve stress and improve flexibility. Have you noticed any specific poses that you enjoy the most?', user=user2, comment=comment6)
    reply17 = Reply(content='Backpacking in Southeast Asia is incredible! Which countries did you visit? I\'m planning a trip there soon and would love some recommendations.', user=user1, comment=comment9)
    reply18 = Reply(content='Wow, backpacking trips are always full of surprises. Did you come across any hidden gems or off-the-beaten-path destinations worth exploring?', user=user2, comment=comment9)
    db.session.add_all([reply1, reply2, reply3, reply4, reply5, reply6, reply7, reply8, reply9, reply10, reply11, reply12, reply13, reply14, reply15, reply16, reply17, reply18])
    db.session.commit()

    # Create sample likes
    like1 = Like(value=True, user=user3, comment=comment1)
    like2 = Like(value=True, user=user1, comment=comment2)
    like3 = Like(value=True, user=user3, comment=comment2)
    like4 = Like(value=True, user=user2, comment=comment3)
    like5 = Like(value=True, user=user1, comment=comment5)
    like6 = Like(value=True, user=user3, comment=comment5)
    like7 = Like(value=True, user=user1, comment=comment6)
    like8 = Like(value=True, user=user1, comment=comment7)
    like9 = Like(value=True, user=user3, comment=comment7)
    like10 = Like(value=True, user=user2, comment=comment9)
    db.session.add_all([like1, like2, like3, like4, like5, like6, like7, like8, like9, like10])
    db.session.commit()

print('Data seeded successfully.')