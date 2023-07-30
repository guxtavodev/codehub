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

class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.String(255), db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.String(255), db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.String(255))

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

  def comentar(self, post, comentario, autor):
    newComment = Comments(post_id=post, user_id=autor, text=comentario)
    db.session.add(newComment)
    db.session.commit()

    return {
      "msg": "success"
    }

  def deletar_comentario(self, comentario, password):
    comentario = Comments.query.filter_by(id=comentario).first()
    autor = Users.query.filter_by(username=comentario.user_id).first()
    if autor and password == autor.password:
      db.session.delete(comentario)
      db.session.commit()
      return {
        "msg": "success"
      }
    else:
      return {
        "msg": "incorrect password"
      }

  def curtir(self, post, autor):
    newCurtida = Likes(post_id=post, user_id=autor)
    db.session.add(newCurtida)
    db.session.commit()
    return {
      "msg": "success"
    }

  def descurtir(self, post, autor):
    curtida = Likes.query.filter_by(post_id=post, user_id=autor).first()
    db.session.delete(curtida)
    db.session.commit()
    return {
      "msg": "success"
    }

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
    user_id = request.args.get("user")
    liked_post_ids = db.session.query(Likes.post_id).filter_by(user_id=user_id).subquery()

    # Recupera todos os posts que não estão na subconsulta dos posts que o usuário curtiu
    posts_not_liked = Posts.query.filter(Posts.id.notin_(liked_post_ids)).all()

    posts_data = []
    for post in posts_not_liked:
        post_data = {
            'id': post.id,
            'text': post.text,
            'author': post.author
        }

        # Consulta para obter os três últimos comentários relacionados a cada post
        last_comments = Comments.query.filter_by(post_id=post.id).order_by(Comments.id.desc()).limit(3).all()

        comments_data = []
        for comment in last_comments:
            comment_data = {
                'id': comment.id,
                'user_id': comment.user_id,
                'text': comment.text
            }
            comments_data.append(comment_data)

        post_data['comments'] = comments_data
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

@app.route("/api/criar-comentario", methods=["POST"])
def criarComentario():
  data = request.get_json()

  return jsonify(Post().comentar(data["post"], data["comentario"], data["user"]))

@app.route("/api/like-post", methods=["POST"])
def likePost():
  data = request.get_json()

  return jsonify(Post().curtir(data["post"], data["user"]))

if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0")