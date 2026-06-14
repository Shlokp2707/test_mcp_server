import random
from fastmcp import FastMCP
import json
mcp =FastMCP("remote_server")
@mcp.tool()
def add_number(x:float,y:float)->float:
    """ Add two numbers together
    arguments:
    x-first number
    y = second number
    return the sum of 2 number"""
    return x+y

@mcp.tool()
def random_number(min_value:int=0,max_value:int =100)->int:
    """ generate random number between the given range
    
    min_value=minimumm value default(0)
    max_value =maximum value default(100)

    return random number within given range
    """
    return random.randint(min_value,max_value)

@mcp.resource("info:server")
def server_info()->str:
    """get information about the server"""
    info ={
        "name":"remote_server",
        "description":"a basic mcp server with math tools.",
        "tool":["add_number","random_number"],
        "author":"shlok"    
    }
    return json.dumps(info,indent=2)

if __name__=="__main__":
    mcp.run(transport="http",host="0.0.0.0",port=8000)
    
