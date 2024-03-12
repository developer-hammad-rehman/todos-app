from typing import Annotated, Optional
from fastapi import Body, FastAPI
from sqlmodel import Session , Field  , create_engine , SQLModel , select
from pydantic import BaseModel
app = FastAPI()
class Todos(SQLModel , table=True):
    id  : Optional[int] = Field(default=None , primary_key=True)
    content : str
class Insert_Todos(BaseModel):
   content : str
db_url : str = 'postgresql://developer-hammad-rehman:8bprnOJV0dxm@ep-quiet-lab-a590cace.us-east-2.aws.neon.tech/todoapp?sslmode=require'
engine =  create_engine(db_url , echo=True)
def create_table():
    SQLModel.metadata.create_all(engine)
def insert_data(content : str ):
    with Session(engine) as session:
     data = Todos(content=content) 
     session.add(data)
     session.commit()
def delete_from_table(content):
   with Session(engine) as session:
     statment = select(Todos).where(Todos.content == content)
     result = session.exec(statment).all()
     for i in result:
        session.delete(i)
        break
     session.commit()
@app.get('/')
def root_route():
    return {"message" : "Hello Welcome To My Todos App"}
@app.get('/todos')
def todos_route():
   session = Session(engine)
   statment = select(Todos)
   result = session.exec(statment)
   return list(result)
@app.post('/todos')
def todos_post_route(content : Insert_Todos):
   insert_data(content.content)
   return {"content" : content.content}
@app.delete('/todos')
def delete_route(content  : Insert_Todos):
   delete_from_table(content.content)
   return {"message" : 'Data Delete Sucessfully ' + content.content}      