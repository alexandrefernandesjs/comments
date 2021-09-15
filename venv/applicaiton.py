from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://dbUser:dbPassword@dbadrress:dbPort/comments"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)


class CommentsModel(db.Model):
    __tablename__ = 'table_comments'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String())
    mensagem = db.Column(db.String())

    def __init__(self, nome, mensagem):
        self.nome = nome
        self.mensagem = mensagem

    def __repr__(self):
        return f"<Comments {self.nome}>"


@app.route('/comments', methods=['POST', 'GET'])
def handle_comments():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_comment = CommentsModel(
                nome=data['nome'], mensagem=data['mensagem'])
            db.session.add(new_comment)
            db.session.commit()
            return {"message": f"comment {new_comment.nome} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        comments = CommentsModel.query.all()
        results = [
            {
                "id": comment.id,
                "nome": comment.nome,
                "mensagem": comment.mensagem,
            } for comment in comments]
        print(results)

        return jsonify(results)


@app.route('/comments/<comment_id>', methods=['PUT', 'DELETE'])
def handle_comment(comment_id):
    comment = CommentsModel.query.get_or_404(comment_id)
    if request.method == 'PUT':
        data = request.get_json()
        comment.id = data['id']
        comment.nome = data['nome']
        comment.mensagem = data['mensagem']

        db.session.add(comment)
        db.session.commit()

        return {"message": f"comentario {comment.id} atualizado"}

    elif request.method == 'DELETE':
        db.session.delete(comment)
        db.session.commit()

        return {"message": f"comentario {comment.id} deletado"}

app.run()