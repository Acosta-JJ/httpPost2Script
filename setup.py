import os

def setup():
    os.system('adduser limiteduser --no-create-home --disabled-login')
    ruta_http_handler = os.getcwd()
    ruta_service_config = ruta_http_handler + '/' + 'service_config.txt'
    os.chdir('/opt')
    os.system('cp -r ' + ruta_http_handler + ' .')
    os.chdir('/etc/systemd/system')
    os.system('cp ' + ruta_service_config + ' ./Graylog2Script.service')
    os.system('systemctl daemon-reload; systemctl start Graylog2Script')
    print('Graylog2Script is now running')

if __name__ == '__main__':
    try:
        setup()
    except:
        print('Something went wrong try Manual instalation')


