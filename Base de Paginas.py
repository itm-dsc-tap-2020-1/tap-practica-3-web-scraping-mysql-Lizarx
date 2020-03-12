#Crear base de datos
"""
> create database Paginas_web;
> use Paginas_web;
> create table pagina(url varchar(70) primary key,status BOOLEAN);
"""


from urllib.request import urlopen
from bs4 import BeautifulSoup
import mysql.connector as mysql
#Funcion para devolver si la base ya tiene verdadero en todos los status
def status_base():
    stat=False
    conexion = mysql.connect( host='localhost', user= 'root', passwd='', db='Paginas_web' )
    operacion = conexion.cursor()
    operacion.execute( "SELECT * FROM pagina" )
    for url, status in operacion.fetchall():
        if(status==0):
            stat=False
            break
        else:
            stat=True
    return stat
conexion = mysql.connect( host='localhost', user= 'root', passwd='', db='Paginas_web' )
operacion = conexion.cursor()
pagina_inicial = input("Ingrese la pagina inicial: ")
operacion.execute((f"INSERT IGNORE INTO pagina values('{pagina_inicial}','{1}')"))
url = urlopen(pagina_inicial)
bs = BeautifulSoup(url.read(), 'html.parser')
while(status_base()==False):
    for enlaces in bs.find_all("a"):
        try:
            lapagina=enlaces.get("href")
            if(lapagina[:4]=="http"):
                operacion.execute((f"INSERT IGNORE INTO  pagina values('{lapagina}','{0}')"))
                conexion.commit()
        except:
            print("")
    operacion.execute( "SELECT * FROM pagina" )
    for url, status in operacion.fetchall():
        if(status==0):
            operacion.execute(f"update pagina set status=1 where url='{url}'")
            break
    try:
        nueva_url = urlopen(url)
        bs = BeautifulSoup(nueva_url.read(), 'html.parser')
    except:
        print("")
conexion.close()