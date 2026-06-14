# import random
# from fastmcp import FastMCP
# import json
# mcp =FastMCP("remote_server")
# @mcp.tool()
# def add_number(x:float,y:float)->float:
#     """ Add two numbers together
#     arguments:
#     x-first number
#     y = second number
#     return the sum of 2 number"""
#     return x+y

# @mcp.tool()
# def random_number(min_value:int=0,max_value:int =100)->int:
#     """ generate random number between the given range
    
#     min_value=minimumm value default(0)
#     max_value =maximum value default(100)

#     return random number within given range
#     """
#     return random.randint(min_value,max_value)

# @mcp.resource("info:server")
# def server_info()->str:
#     """get information about the server"""
#     info ={
#         "name":"remote_server",
#         "description":"a basic mcp server with math tools.",
#         "tool":["add_number","random_number"],
#         "author":"shlok"    
#     }
#     return json.dumps(info,indent=2)
import os,sqlite3
from fastmcp import FastMCP 
db_path =os.path.join(os.path.dirname(__file__),"Expanse_Trackers.db") 
mcp =FastMCP(name ="expanse-tracker") 
category_path =os.path.join(os.path.dirname(__file__),"category.json")
def init_db():
    with sqlite3.connect(db_path) as c:
        c.execute("""
        create table if not exists expenses(
                id integer primary key autoincrement,
                e_date text not null,
                amount real not null,
                category text not null,
                subcategory text default "" ,
                note text default ""
                    )
""")
init_db()
@mcp.tool()
def add_expanses(e_date:str,amount:float,category:str,subcategory:str="",note:str=""):
    """ Add a new expense.
    Parameters:
    - e_date: YYYY-MM-DD
    - amount: expense amount
    - category: expense category
    - subcategory: optional
    - note: optional note"""
    with sqlite3.connect(db_path) as c:
        cur =c.execute(
            """
        insert into expenses(e_date,amount,category,subcategory,note) values (?,?,?,?,?)""",
        (e_date,amount,category,subcategory,note)
        )
        return {'status':"ok","id":cur.lastrowid}
@mcp.tool()
def list_expanses(start_date:str,end_date:str):
    """ list all the expanses from the databases"""
    with sqlite3.connect(db_path) as c:
        cur  =c.execute("""select * from expenses where e_date between ? and ? order by id """,(start_date,end_date))
        cols =[d[0] for d in cur.description]
        return [dict(zip(cols,r)) for r in cur.fetchall()]
@mcp.tool()
def summarise_expenses(start_date:str,end_date:str,category:str):
    """ summarise the expanse by catagory within  the  inclusive  date range"""
    with sqlite3.connect(db_path) as c: 
        query=""" select catagory sum(amount) as total_amount from expenses where e_date between ? and ?"""
        params =[start_date,end_date]
        if category :
            query+=" and category =?"
            params.append(category)
            query+="group by category order by category "
            cur  =c.execute( query, params)
            cols =[d[0] for d in cur.description]
            return [dict(zip(cols,r)) for r in cur.fetchall()]
        
@mcp.resource("expanses://category",mime_type="application/json")
def category():
    with open(category_path,"r",encoding="utf-8")as f:
        return f.read()

if __name__=="__main__":
    mcp.run(transport="http",host="0.0.0.0",port=8000)
    
