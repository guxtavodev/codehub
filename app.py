from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))

class Posts(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    text = db.Column(db.String(255))
    author = db.Column(db.String(30))
    likes = db.relationship('Likes', backref='post', lazy=True)
    comments = db.relationship('Comments', backref='post', lazy=True)

with app.app_context():
    db.create_all()

class User():
  def cadastrar(self, username, password):
    idUnico = "12347"
    newUser = Users(id=str(idUnico), username=username, password=password)
    db.session.add(newUser)
    db.session.commit()

    return {
      "msg": "success",
      "id": str(idUnico)
    }

  def auth(self, username, password):
    user = Users.query.filter_by(username=username).first()

    if user and password == user.password:
      return {
        "msg": "success",
        "id": user.id
      }

  def delete_user(self, id):
    user = Users.query.filter_by(username=id).first()
    db.session.delete(user)
    db.session.commit()

    return {
      "msg": "success"
    }

  def edit_password(self, newPassword, password, id):
    user = Users.query.filter_by(id=id).first()
    if user.password == password:
      user.password = password 
      db.session.commit()
      return {
        "msg": "success"
      }
    else:
      return {
        "msg": "incorrect password"
      }

class Post():
  def create(self, text, author):
    newPost = Posts(id="ok", text=text, author=author)
    db.session.add(newPost)
    db.session.commit()

    return {
      "msg": "success",
      "id": newPost.id
    }

  def delete(self, post, password):
    post = Posts.query.filter_by(id=id).first()
    autor = Users.query.filter_by(author=post.author).first()
    if autor and password == autor.password:
      db.session.delete(post)
      db.session.commit()


@app.route("/api/delete-account", methods=["GET"])
def deletarConta():
  user = request.args.get("user")
  return jsonify(User().delete_user(user))

@app.route("/api/criar-post", methods=["POST"])
def criarPost():
  data = request.get_json()
  return jsonify(Post().create(data["text"], data["author"]))

@app.route("/")
def homepage():
  return render_template("index.html")

@app.route("/api/get-posts", methods=["GET"])
def getPosts():
    # Recupera todos os posts da tabela 'Posts'
    all_posts = Posts.query.all()

    posts_data = []
    for post in all_posts:
        post_data = {
            'id': post.id,
            'text': post.text,
            'author': post.author
        }
        posts_data.append(post_data)

    return {'posts': posts_data}


@app.route("/cadastro")
def cadastroPage():
  return render_template("cadastro.html")

@app.route("/api/cadastrar", methods=["POST"])
def cadastro():
  data = request.get_json()
  return jsonify(User().cadastrar(data["username"], data["password"]))

@app.route("/logar", methods=["GET"])
def logarConta():
  username = request.args.get("username")
  password = request.args.get("password")

  return jsonify(User().auth(username, password))

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
  return jsonify(User().edit_password(data["newPassword"], data["password"], data["user"]))

if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0")
