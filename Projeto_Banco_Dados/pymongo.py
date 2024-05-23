import pymongo as pyM

client = pyM.MongoClient("")
db = client.test
collection = db.test_collection

cliente = {
    "nome":"pedro",
    "cpf":123456789,
    "agencia" :"0001",
    "tipo" :"conta-corrente",
    "num" :1234,
    "saldo" : 1200.00
}

posts = db.posts
post_id = posts.insert_one(cliente).inserted_id

pprint.pprint(db.posts.find_one())

novos_clientes = [{
    "nome":"angela",
    "cpf":987654321,
    "agencia" :"0001",
    "tipo" :"conta-salario",
    "num" :4321,
    "saldo" : 1500.00
},{
    "nome":"cesar",
    "cpf":132457689,
    "agencia" :"0002",
    "tipo" :"conta-poupança",
    "num" :1324,
    "saldo" : 12340.00
}]

result = posts.insert_many(novos_clientes)
print(result.inserted_ids)

for posts in posts.find():
    pprint.pprint(cliente)

print(posts.count_docuemnes({}))
print(posts.count_docuemnes({"nome":"angela"}))
print(posts.count_docuemnes({"agencia":"0002"}))

for posts in posts.find().sort("nome"):
    pprint.pprint(cliente)

