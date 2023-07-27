from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import (
    current_user,
    LoginManager,
    login_required,
    login_user,
    logout_user,
    UserMixin,
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import validates, joinedload
from datetime import datetime

app = Flask(__name__, template_folder="./templates")

DB_URI = "mysql+mysqlconnector://{user}:{password}@{host}/{dbname}".format(
    user="root", password="password", host="localhost", dbname="python_flask"
)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = "JUyDHed7kJnuU85goeyU31Hy1IOtO3"
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    # Relationships
    comments = db.relationship("Comment", back_populates="user")
    replies = db.relationship("Reply", back_populates="user")
    likes = db.relationship("Like", back_populates="user")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @validates("username")
    def validate_username(self, key, username):
        assert len(username) > 3

        return username

    @validates("password")
    def validate_password(self, key, password):
        assert len(password) > 4

        return password

    def get_id(self):
        return str(self.id)


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    user = db.relationship("User", back_populates="comments")
    replies = db.relationship("Reply", cascade="all,delete", back_populates="comment")
    likes = db.relationship("Like", cascade="all,delete", back_populates="comment")


class Reply(db.Model):
    __tablename__ = "replies"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(2048), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    user = db.relationship("User", back_populates="replies")
    comment = db.relationship("Comment", back_populates="replies")


class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"))

    # Relationships
    user = db.relationship("User", back_populates="likes")
    comment = db.relationship("Comment", back_populates="likes")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.template_filter("pluralize_comment")
def pluralize_comment(count):
    if count == 1:
        return "1 comment"
    else:
        return str(count) + " " + "comments"


@app.template_filter("pluralize_like")
def pluralize_like(count):
    if count == 1:
        return "1 like"
    else:
        return str(count) + " " + "likes"


@app.template_filter("pluralize_reply")
def pluralize_reply(count):
    if count == 1:
        return "1 reply"
    else:
        return str(count) + " " + "replies"


@app.template_filter("comment_username")
def comment_username(comment_id):
    comment = Comment.query.get(comment_id)

    if current_user.is_authenticated:
        if comment.user_id == current_user.id:
            return "YOU"
        else:
            return comment.user.username


@app.template_filter("reply_username")
def reply_username(reply_id):
    reply = Reply.query.get(reply_id)

    if current_user.is_authenticated:
        if reply.user_id == current_user.id:
            return "YOU"
        else:
            return reply.user.username


@app.template_filter("like_username")
def like_username(like_id):
    like = Like.query.get(like_id)

    if current_user.is_authenticated:
        if like.user_id == current_user.id:
            return "YOU"
        else:
            return like.user.username


@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%a, %#m/%#d/%y")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        comments = Comment.query.all()
        replies = Reply.query.all()
        likes = Like.query.all()

        if not current_user.is_authenticated:
            return render_template(
                "index.html",
                comments=comments,
                replies=replies,
                likes=likes,
                current_page="index",
                unauth=True,
                unauth_msg="You must be logged in to interact with the comment forum.",
            )

        if not comments:
            return render_template(
                "index.html",
                no_comments=True,
                no_comments_msg="No comments posted yet...be the first!!",
            )

        return render_template(
            "index.html",
            comments=comments,
            replies=replies,
            likes=likes,
            current_page="index",
        )

    if request.method == "POST":
        if not current_user.is_authenticated:
            return redirect(url_for("index"))

        comment_content = request.form.get("contents")
        comment = Comment(content=comment_content, user=current_user)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("index"))


@app.route("/comment/edit/<int:comment_id>", methods=["GET", "POST"])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get(comment_id)

    if comment.user_id != current_user.id:
        return redirect(url_for("index"))

    if request.method == "POST":
        comment.content = request.form["contents"]
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("edit_comment.html", comment=comment)


@app.route("/comment/reply/<int:comment_id>", methods=["GET", "POST"])
@login_required
def reply_comment(comment_id):
    comment = Comment.query.get(comment_id)

    if request.method == "POST":
        reply_content = request.form.get("contents")
        reply = Reply(content=reply_content, user=current_user, comment_id=comment_id)
        db.session.add(reply)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("reply_comment.html", comment=comment)


@app.route("/replies/<int:comment_id>", methods=["GET"])
@login_required
def replies(comment_id):
    comment = Comment.query.get(comment_id)
    replies = Reply.query.filter_by(comment_id=comment_id).all()

    if comment is None:
        return redirect(url_for("index"))

    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    return render_template("replies.html", comment=comment, replies=replies)


@app.route("/comment/delete/<int:comment_id>", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)

    if comment is None:
        return redirect(url_for("index"))

    if comment.user_id != current_user.id:
        return redirect(url_for("index"))

    Reply.query.filter_by(comment_id=comment_id).delete()
    Like.query.filter_by(comment_id=comment_id).delete()
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/reply/delete/<int:reply_id>", methods=["POST"])
@login_required
def delete_reply(reply_id):
    reply = Reply.query.get(reply_id)

    if reply is None:
        return redirect(url_for("index"))

    if reply.user_id != current_user.id:
        return redirect(url_for("index"))

    db.session.delete(reply)
    db.session.commit()
    return redirect(url_for("replies", comment_id=reply.comment_id))


@app.route("/comment/like/<int:comment_id>", methods=["POST"])
@login_required
def like_comment(comment_id):
    comment = Comment.query.get(comment_id)

    if comment is None:
        return redirect(url_for("index"))

    like = Like.query.filter_by(comment_id=comment_id, user_id=current_user.id).first()
    if like is None:
        like = Like(comment_id=comment_id, user_id=current_user.id, value=True)
        db.session.add(like)
    elif like.value:
        db.session.delete(like)

    db.session.commit()

    return redirect(url_for("index"))


# @app.route("/comment/like/<int:comment_id>", methods=["POST"])
# @login_required
# def like_comment(comment_id):
#     comment = Comment.query.get(comment_id)
#     like = Like(comment_id=comment_id, user_id=current_user.id, value=True)
#     db.session.add(like)
#     db.session.commit()
#     return redirect(url_for("index"))


# @app.route("/comment/unlike/<int:comment_id>", methods=["POST"])
# @login_required
# def unlike_comment(comment_id):
#     comment = Comment.query.get(comment_id)
#     like = Like.query.filter_by(comment_id=comment_id, user_id=current_user.id).first()
#     db.session.delete(like)
#     db.session.commit()
#     return redirect(url_for("index"))


@app.route("/user_comments/<int:user_id>", methods=["GET"])
def user_comments(user_id):
    user = User.query.get(user_id)
    comments = Comment.query.filter_by(user_id=user.id).all()
    replies = Reply.query.filter_by(user_id=user.id).all()
    likes = Comment.query.filter_by(user_id=user.id).all()

    if user is None:
        return jsonify({"message": "User not found"}), 404

    user_comments = (
        Comment.query.options(joinedload(Comment.replies).joinedload(Reply.user))
        .options(joinedload(Comment.likes).joinedload(Like.user))
        .filter_by(user_id=user.id)
        .all()
    )

    user_data = {"id": user.id, "username": user.username, "comments": []}

    for comment in user_comments:
        comment_data = {
            "id": comment.id,
            "content": comment.content,
            "created_at": comment.created_at,
            "replies": [],
            "likes": [],
        }

        for reply in comment.replies:
            reply_data = {
                "id": reply.id,
                "content": reply.content,
                "username": reply.user.username,
                "created_at": reply.created_at,
            }
            comment_data["replies"].append(reply_data)

        for like in comment.likes:
            like_data = {
                "id": like.user.id,
                "username": like.user.username,
            }
            comment_data["likes"].append(like_data)

        user_data["comments"].append(comment_data)

    return render_template(
        "user_info.html",
        user=user,
        user_data=user_data,
        comments=comments,
        replies=replies,
        likes=likes,
        type="comments",
    )


@app.route("/user_replies/<int:user_id>", methods=["GET"])
def user_replies(user_id):
    user = User.query.get(user_id)
    comments = Comment.query.filter_by(user_id=user.id).all()
    replies = Reply.query.filter_by(user_id=user.id).all()
    likes = Like.query.filter_by(user_id=user.id).all()

    if user is None:
        return jsonify({"message": "User not found"}), 404

    user_replies = (
        Reply.query.options(joinedload(Reply.comment).joinedload(Comment.user))
        .options(
            joinedload(Reply.comment).joinedload(Comment.likes).joinedload(Like.user)
        )
        .filter_by(user_id=user.id)
        .all()
    )

    user_data = {"id": user.id, "username": user.username, "replies": []}

    for reply in user_replies:
        reply_data = {
            "id": reply.id,
            "content": reply.content,
            "created_at": reply.created_at,
            "comment": {
                "id": reply.comment.id,
                "content": reply.comment.content,
                "username": reply.comment.user.username,
                "created_at": reply.comment.created_at,
                "total_replies": len(reply.comment.replies),
                "total_likes": len(reply.comment.likes),
                "replies": [],  # Placeholder for nested replies
                "likes": [],  # Placeholder for likes on the comment
            },
        }

        for reply in reply.comment.replies:
            comment_reply_data = {
                "reply_content": reply.content,
                "reply_username": reply.user.username,
                "reply_created_at": reply.created_at,
            }
            reply_data["comment"]["replies"].append(comment_reply_data)

        for like in reply.comment.likes:
            comment_like_data = {
                "id": like.user.id,
                "username": like.user.username,
            }
            reply_data["comment"]["likes"].append(comment_like_data)

        user_data["replies"].append(reply_data)

    return render_template(
        "user_info.html",
        user=user,
        user_data=user_data,
        comments=comments,
        replies=replies,
        likes=likes,
        type="replies",
    )


@app.route("/user_likes/<int:user_id>", methods=["GET"])
def user_likes(user_id):
    user = User.query.get(user_id)
    comments = Comment.query.filter_by(user_id=user.id).all()
    replies = Reply.query.filter_by(user_id=user.id).all()
    likes = Like.query.filter_by(user_id=user.id).all()

    if user is None:
        return jsonify({"message": "User not found"}), 404

    user_likes = (
        Like.query.options(joinedload(Like.comment).joinedload(Comment.user))
        .options(
            joinedload(Like.comment).joinedload(Comment.replies).joinedload(Reply.user)
        )
        .filter_by(user_id=user.id)
        .all()
    )

    user_data = {"id": user.id, "username": user.username, "likes": []}

    for like in user_likes:
        like_data = {
            "id": like.comment.id,
            "content": like.comment.content,
            "username": like.comment.user.username,
            "created_at": like.comment.created_at,
            "total_replies": len(like.comment.replies),
            "total_likes": len(like.comment.likes),
            "replies": [],  # Placeholder for nested replies
            "likes": [],  # Placeholder for likes on the comment
        }

        for reply in like.comment.replies:
            comment_reply_data = {
                "content": reply.content,
                "username": reply.user.username,
                "created_at": reply.created_at,
            }
            like_data["replies"].append(comment_reply_data)

        for like in like.comment.likes:
            comment_like_data = {
                "id": like.user.id,
                "username": like.user.username,
            }
            like_data["likes"].append(comment_like_data)

        user_data["likes"].append(like_data)

    return render_template(
        "user_info.html",
        user=user,
        user_data=user_data,
        comments=comments,
        replies=replies,
        likes=likes,
        type="likes",
    )


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            return render_template(
                "register.html",
                error=True,
                error_msg="There is already a registered user with that username. Please try again.",
            )

        if username == "" or password == "":
            return render_template(
                "register.html",
                error=True,
                error_msg="Username and/or password cannot be blank. Please try again.",
            )

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("index"))


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        return render_template("login.html")

    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user is None or not user.check_password(request.form["password"]):
            return render_template(
                "login.html", error=True, error_msg="Incorrect username and/or password"
            )

        login_user(user)
        return redirect(url_for("index"))


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
