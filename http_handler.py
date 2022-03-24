#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler,HTTPServer
from sys import argv
import os
import json
import re


def json_write(json_info):
    with open('json_data.json','w') as outfile:
        json.dump(json_info, outfile)


#Las funciones se tienen que llamar do_* ya que la función handle busca segun ese nombre el método de respuesta(Documentacion)
class http_request_handler(BaseHTTPRequestHandler): 

    def _set_response(self):

        self.send_response(200) #Respondemos un "200 OK"
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_POST(self):

        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        script_params = json.loads(post_body)
        current_working_directory = '/opt/http_request_handler'
        folder_name = str(script_params["event_definition_description"]).split(".")[0] #Sacamos el nombre del directorio
        scripts_directory = current_working_directory + '/scripts' + '/' + str(folder_name)

        try:

            os.chdir(scripts_directory)

        except:

            print("El script indicado no existe ruta: " + scripts_directory + ' ' )
            f = open("logs.txt", "a")
            f.write('\n#####################################################################################################\n')
            f.write(str(self.requestline) +
            ' | Script ejecutado: ' + scripts_directory + ' ' + 'No se ha podido ejecutar el script' +
            ' | ' + self.client_address[0] + ':' + str(self.client_address[1]) + '\n')
            f.close()
            return

        json_write(script_params)

        filter_regex = re.compile('[^a-zA-Z.]') #Filtro para evitar el mal uso del script para escalar privilegios
        filter_regex = filter_regex.sub('', script_params["event_definition_description"])

        status = os.system('sudo -u limiteduser ./' + filter_regex)
        os.chdir(current_working_directory)
        
        f = open("logs.txt", "a") #Guardamos los logs formateados
        f.write('\n#####################################################################################################\n')
        f.write(str(self.requestline) +
        ' | Script ejecutado: ' + scripts_directory +'/'+script_params["event_definition_description"] + ' ' + str(status) +
        ' | ' + self.client_address[0] + ':' + str(self.client_address[1]) + '\n')
        f.close()

        #self._set_response() #Respondemos a la petición


def http_server(server_class=HTTPServer, port=4000, handler=http_request_handler): #El puerto por defecto es el 4000 ya que hay otros ocupados por otros servicios

    server_address=('127.0.0.1',port) #En caso de querer exponerlo fuera de intranet cambiar IP
    httpd = server_class(server_address, handler)

    try:
        print('\033[93m' + 'Running http_handler, use ctrl + c to stop it' + '\033[0m')
        httpd.serve_forever()

    except KeyboardInterrupt:
        httpd.server_close()
        print('\n' + '\033[93m' + 'http_handler closed' + '\033[0m')


if __name__ == '__main__':
    if len(argv) == 2:
        if (argv[1] == '-h' or argv[1] == '--help'):
            print('Use : ./http_handler.py [port]')
            print('python3 http_handler.py [port]')
            print('Default use : python3 http_handler.py')
            print('Default port:4000')
            print('Documentation: https://docs.python.org/3/library/http.server.html')
        else:
            http_server(port=int(argv[1])) #utiliza el puerto pasado por consola
    else:
        http_server() #utiliza el puerto por defecto: 4000


