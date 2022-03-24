#!/usr/bin/env python3
#Esto es un script de ejemplo, al llamarse test.py lo tendremos que ubicar en el
#directorio /opt/http_request_handler/scripts/test/test.py además de contar con los permisos 775
#Además en necesario poner el nombre del script únicamente en la descripción del evento por ejemplo test.py
#crear usuario de servicio que se llame limiteduser con: adduser limiteduser --no-create-home --disabled-login 
import json

def example():
    #Como leer el json
    with open('json_data.json') as json_file:
        data = json.load(json_file)
    print('Json open')
    #como acceder a sus variables
    print(data["event_definition_description"])

if __name__ == '__main__':
    print("Success Executing on POST METHOD")
    example()
