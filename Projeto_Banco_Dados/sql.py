from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Decimal
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import Interger
from sqlalchemy import String
from sqlalchemy import ForeignKey

Base = declarative_base()

class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(Interger, primary_key=True)
    nome = Column(String)
    cpf = Column(String(9))
    endereco = Column(String(9))
    
    conta = relationship(
        "Conta", back_populates="cliente"
    )

    def __repr__(self):
        return f"cliente id={self.id}, nome={self.nome}, CPF={self.cpf}, endereco={self.endereco}"


class Conta(Base):
    __tablename__ = "conta"

    id = Column(Interger, primary_key=True)
    tipo = Column(String)
    agencia= Column(String)
    num = Column(Interger)
    saldo = Column(Decimal)
    id_cliente = Column(Interger, ForeignKey("cliente.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="conta")

    def __repr__(self):
        return f"Conta id={self.id}, tipo={self.tipo}, agencia={self.agencia}, numero_conta={self.num}"


engine = create_engine("sqlite://")

Base.metadata.create_all(engine)

inspetor_engine = inspect(engine)
print(inspetor_engine.get_table_names())


with Session(engine) as session:
    pedro = Cliente(
        nome= "pedro"
        cpf=123456789
        agencia = [Conta(agencia="0001")]
        tipo = [Conta(tipo="conta-corrente")]
        num = [Conta(num=1234)]
        saldo = [Conta(saldo=1200.00)]
    )

    angela = Cliente(
        nome= "angela"
        cpf=987654321
        agencia = [Conta(agencia="0001")]
        tipo = [Conta(tipo="conta-corrente"),
                Conta(tipo="conta_poupança")]
        num = [Conta(num=4321)]
         saldo = [Conta(saldo=4044.00)]
    )

    cesar = Cliente(
        nome= "cesar"
        cpf=132457689
        agencia = [Conta(agencia="0002")]
        tipo = [Conta(tipo="conta-salario")]
        num = [Conta(num=1324)]
         saldo = [Conta(saldo=12200.20)]
    )

    session.add_all([pedro, angela, cesar])

    session.commit()


stmt = select(Cliente).where(Cliente.nome.in_(["pedro", "angela"]))
for clientes in session.scalars(stmt):
    print(clientes)

stmt_conta = select(Conta).where(Conta.id_cliente.in_([2]))
for contas in session.scalars(stmt_conta):
    print(contas)

stmt_order = select(Cliente).order_by(Cliente.nome.desc())
for resultado in session.scalars(stmt_order):
    print(resultado)

stmt_join = select(Cliente.nome, Conta.tipo).join_from(Conta, Cliente)
for resultado in session.scalars(stmt_join):
    print(resultado)

stmt_count = select(func.count('*')).select_from(Cliente)
for resultado in session.scalars(stmt_count):
    print(resultado)

session.close()

