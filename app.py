from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))

    @staticmethod
    def cadastrar(username, password):
        newUser = Users(username=username, password=password)
        db.session.add(newUser)
        db.session.commit()
        return {"msg": "success", "id": newUser.id}

    @staticmethod
    def auth(username, password):
        user = Users.query.filter_by(username=username).first()
        if user and password == user.password:
            return {"msg": "success", "id": user.id}

    @staticmethod
    def delete_user(id):
        user = Users.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {"msg": "success"}

    @staticmethod
    def edit_password(newPassword, password, id):
        user = Users.query.get_or_404(id)
        if password == user.password:
            user.password = newPassword
            db.session.commit()
            return {"msg": "success"}
        else:
            return {"msg": "incorrect password"}

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(255))
    author = db.Column(db.String(30))

    @staticmethod
    def create(text, author):
        newPost = Posts(text=text, author=author)
        db.session.add(newPost)
        db.session.commit()
        return {"msg": "success", "id": newPost.id}

    @staticmethod
    def delete(post_id, password):
        post = Posts.query.get_or_404(post_id)
        autor = Users.query.filter_by(username=post.author).first()
        if autor and password == autor.password:
            db.session.delete(post)
            db.session.commit()

@app.route("/api/delete-account", methods=["GET"])
def deletarConta():
    user_id = request.args.get("user")
    return jsonify(Users.delete_user(user_id))

@app.route("/api/criar-post", methods=["POST"])
def criarPost():
    data = request.get_json()
    return jsonify(Posts.create(data["text"], data["author"]))

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/api/get-posts", methods=["GET"])
def getPosts():
    all_posts = Posts.query.all()
    posts_data = [{"id": post.id, "text": post.text, "author": post.author} for post in all_posts]
    return {"posts": posts_data}

@app.route("/cadastro")
def cadastroPage():
    return render_template("cadastro.html")

@app.route("/api/cadastrar", methods=["POST"])
def cadastro():
    data = request.get_json()
    return jsonify(Users.cadastrar(data["username"], data["password"]))

@app.route("/logar", methods=["GET"])
def logarConta():
    username = request.args.get("username")
    password = request.args.get("password")
    return jsonify(Users.auth(username, password))

@app.route("/settings")
def settingsPage():
    return render_template("settings.html")

@app.route("/api/change-password", methods=["POST"])
def editInfos():
    data = {
        "newPassword": request.args.get("senha-nova"),
        "password": request.args.get("senha-atual"),
        "user": request.args.get("user")
    }
    return jsonify(Users.edit_password(data["newPassword"], data["password"], data["user"]))

if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0")
