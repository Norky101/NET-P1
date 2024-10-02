import socket
import url_parse
"""
Create a TCP connection to a web server and send an HTTP GET request.
"""

try:
    # create an INET, STREAMing socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    #coonect the the hostname and relevant port
    protocol, port, host, path = url_parse.parse_url(url) # exstract the relevet info from webaddress

    sock.connect((host, port))

except Exception as e:
    #formats the error correctly
    print(f'URL: {url}')
    print('Status: Network Error')


sock.close()



