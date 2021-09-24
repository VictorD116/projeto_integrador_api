from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/pse'
db = SQLAlchemy(app)


class Pse(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    data = db.Column(db.Date, nullable=False)
    pse = db.Column(db.String(2), nullable=False)
    tipo_treino = db.Column(db.String(20), nullable=False)
    duracao = db.Column(db.String(3), nullable=False)

    def to_json(self):
        data = self.data.strftime("%m/%d/%Y")
        return {"id": self.id, "nome": self.nome,
                "data": data, "pse": self.pse,
                "tipo_treino": self.tipo_treino,
                "duracao": self.duracao}


# Get
# Selecionar todos
@app.route("/tdspse", methods=["GET"])
def seleciona_pse():
    pse_objetos = Pse.query.all()
    pse_json = [pse.to_json() for pse in pse_objetos]
    print(pse_json)
    return gera_response(200, "Pse", pse_json)


# Selecionar Um
@app.route("/tdspse/<id>", methods=["GET"])
def seleciona_um_pse(id):
    pse_objeto = Pse.query.filter_by(id=id).first()
    pse_json = pse_objeto.to_json()

    return gera_response(200, "Pse", pse_json)


# Cadastrar
@app.route("/pse", methods=["POST"])
def cria_pse():
    body = request.get_json()
    try:
        pse = Pse(nome=body["nome"], data=body["data"], pse=body["pse"],
                  tipo_treino=body["tipo_treino"], duracao=body["duracao"])
        db.session.add(pse)
        db.session.commit()
        return gera_response(201, "pse", pse.to_json(), "Criado com sucesso")
    except Exception as e:
        print('ERRO', e)
        return gera_response(400, "pse", {}, "Erro ao cadastrar")


# Atualizar
@app.route("/pse/<id>", methods=["PUT"])
def atualiza_pse(id):
    pse_objeto = Pse.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if ('nome' in body):
            usuario_objeto.nome = body['nome']
        if ('data' in body):
            usuario_objeto.email = body['data']
        if ('pse' in body):
            usuario_objeto.email = body['pse']
        if ('tipo_treino' in body):
            usuario_objeto.email = body['tipo_treino']
        if ('duracao' in body):
            usuario_objeto.email = body['duracao']

        db.session.add(pse_objeto)
        db.session.commit()
        return gera_response(200, "pse", pse_objeto.to_json(), "Atualizado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "pse", {}, "Erro ao atualizar")

# Deletar
@app.route("/pse/<id>", methods=["DELETE"])
def deleta_pse(id):
    pse_objeto = Pse.query.filter_by(id=id).first()

    try:
        db.session.delete(pse_objeto)
        db.session.commit()
        return gera_response(200, "pse", pse_objeto.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao deletar")


def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if (mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body), status=status, mimetype="application/json")


app.run()
