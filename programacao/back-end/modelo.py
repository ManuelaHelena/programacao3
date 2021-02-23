from config import *
from config import db

class Cachorro(db.Model):
    # atributos da cachorro
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(254))
    raca = db.Column(db.String(254))
    porte = db.Column(db.String(254))
    pelagem = db.Column(db.String(254))


    # método para expressar a cachorro em forma de texto
    def __str__(self):
        # return str(self.id)+") "+ self.nome + ", " +\
        #     self.email + ", " + self.telefone
        return f'''
                --- Cachorro [{self.id}] --- 
                Nome [{self.nome}]      
                raca [{self.raca}]    
                Porte [{self.porte}]        
                Pelagem [{self.pelagem}]    
                __________________________
                '''
    # expressao da classe no formato json
    def json(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "raca": self.raca,
            "porte": self.porte,
            "pelagem": self.pelagem
        }
    
class exameRealizado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(254)) # data do exame
    resultado = db.Column(db.String(254)) # apenas o valor

    # cachorro que fez o exame; não pode ser nulo (composição!)
    cachorro_id = db.Column(db.Integer, db.ForeignKey(Cachorro.id), nullable=False)
    cachorro = db.relationship("Cachorro")

    def __str__(self): # expressão da classe em forma de texto
        return f"{self.data}, {self.resultado}, " + \
            f"{str(self.cachorro)}"

    def json(self):
        return {
            "id":self.id,
            "data":self.data,
            "resultado":self.resultado,
            "cachorro_id":self.cachorro_id,
            "cachorro":self.cachorro.json(),
        }

class hospedarCachorro(db.Model):
    id = db.Column(db.Integer, primary_key=True) # id interno
    codigo = db.Column(db.String(254)) # código do equipamento
    data_aquisicao = db.Column(db.String(254))
    data_hospedagem = db.Column(db.String(254)) # Hospedado? se sim, desde quando?

    # atributo de chave estrangeira
    cachorro_id = db.Column(db.Integer, db.ForeignKey(Cachorro.id))
    # atributo de relacionamento, para acesso aos dados via objeto
    cachorro = db.relationship("Cachorro")

    def __str__(self): # expressão da classe em forma de texto
        s = f"HospedarCachorro {self.codigo} adquirido em {self.data_aquisicao}"
        if self.cachorro != None:
            s += f", emprestado para {self.cachorro} desde {self.data_aquisicao}"
        return s

    def json(self):
        if self.cachorro is None: # o cachorro não está emprestado?
            cachorro_id = ""
            cachorro = ""
            data_hospedagem = ""
        else: # o cachorro está emprestado!! :-)
            cachorro_id = self.cachorro_id
            cachorro = self.cachorro.json()
            data_hospedagem = self.data_hospedagem

        return {
            "id": self.id,
            "codigo": self.codigo,
            "data_aquisicao": self.data_aquisicao,
            "cachorro_id": cachorro_id,
            "Cachorro": Cachorro,
            "data_hospedagem": data_hospedagem
        } 

# teste    
if __name__ == "__main__":
    # apagar o arquivo, se houver
    if os.path.exists(arquivobd):
        os.remove(arquivobd)

    # criar tabelas
    db.create_all()

    # teste da classe Cachorro
    m1 = Cachorro(nome= "Molly",raca="Samoieda",porte="Grande",pelagem="Longa")
    m2 = Cachorro(nome= "Geraldo",raca="Hottweiller",porte="Gigantesco",pelagem="Curta")     
    
    # persistir
    db.session.add(m1)
    db.session.add(m2)
    db.session.commit()
     
    # exibir o cachorro
    print(m2)

    # exibir o cachorro no format json
    print(m2.json())

 # criar resultado de exame
    e1 = hospedarCachorro(data_hospedagem="29/03/2018",
         codigo="p1")
    db.session.add(e1)
    db.session.commit()
    print(f"Exame realizado: {e1}")
    print(f"Exame realizado em json: {e1.json()}")