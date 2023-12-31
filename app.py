from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import time
from passlib.hash import bcrypt_sha256

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

def generate_random_id():
    timestamp = int(time.time() * 1000)
    random_number = hash(str(id(time.time())))
    random_id = timestamp + random_number
    return random_id

class Users(db.Model):
    username = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.String(30))
    id = db.Column(db.Integer, autoincrement=True)
    

class Posts(db.Model):
    text = db.Column(db.String(255), primary_key=True)
    author = db.Column(db.String(30))
    id = db.Column(db.Integer, autoincrement=True)


with app.app_context():
    db.create_all()

class User():
    def cadastrar(self, username, password):
        password_hash = bcrypt_sha256.hash(password)
        newUser = Users(username=username, password=password_hash, id=int(generate_random_id()))
        db.session.add(newUser)
        db.session.commit()

        return {
            "msg": "success"
        }

    def auth(self, username, password):
        user = Users.query.filter_by(username=username).first()

        if user and bcrypt_sha256.verify(password, user.password):
            return {
                "msg": "success"
            }
        else:
            return {
                "msg": "incorrect password"
            }

    def delete_user(self, id):
        user = Users.query.filter_by(username=id).first()
        db.session.delete(user)
        db.session.commit()

        return {
            "msg": "success"
        }

    def edit_password(self, newPassword, password, id):
        user = Users.query.filter_by(username=id).first()
        if bcrypt_sha256.verify(password, user.password):
            user.password = bcrypt_sha256.hash(newPassword)
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
    newPost = Posts(text=text, author=author, id=generate_random_id())
    db.session.add(newPost)
    db.session.commit()

    return {
      "msg": "success"
    }

  def delete(self, post, password):
    post = Posts.query.filter_by(id=int(post)).first()
    autor = Users.query.filter_by(username=post.author).first()
    if autor and password == autor.password:
      db.session.delete(post)
      db.session.commit()
      return {
        "msg": "success"
      }
    else:
      return {
        "msg": "incorrect password"
      }


@app.route("/api/delete-post", methods=["GET"])
def deletarPost():
  post = request.args.get("post")
  senha = request.args.get("password")

  return jsonify(Post().delete(post, senha))

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

@app.route("/auth")
def loginPage():
  return render_template("auth.html")

@app.route("/api/auth", methods=["GET"])
def authUser():
  username = request.args.get('username')
  password = request.args.get('password')

  return jsonify(User().auth(username, password))

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

@app.route("/api/change-password", methods=["GET"])
def editInfos():
  data = {
    "newPassword": request.args.get("senha-nova"),
    "password": request.args.get("senha-atual"),
    "user": request.args.get("user")
  }
  return jsonify(User().edit_password(data["newPassword"], data["password"], data["user"]))

@app.route("/perfil/<user>")
def perfilUser(user):
  posts_user = Posts.query.filter_by(author=user).all()
  posts = []
  for post in posts_user:
    posts.append({
      "text": post.text,
      "author": post.author,
      "id": post.id
    })

  return render_template("perfil.html", posts=posts, username=user)

if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0")
