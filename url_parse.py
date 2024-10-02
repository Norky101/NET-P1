# http://www.someSchool.edu/someDepartment/picture.gif

# • http:// Indicates that the protocol is HTTP, and hence the web server is
# listening at the port 80. If the URL starts with https:// instead, the protocol
# will be HTTPS, and the web server will be listening at the port 443;

# • www.someSchool.edu is the host name, which will be translated to an IP
# address where the web monitor should connect to;

# • /someDepartment/picture.gif is path of the requested object on the
# server, which must be presented in the HTTP request message sent to the server.

"""
Extract the protocol, host, and path from a URL.
"""

def parse_url(url):
    # Split the URL into protocol and the rest
    protocol, rest = url.split("://", 1)

    #define the port
    if protocol == "http":
        port = 80
    elif protocol == "https":
        port = 443
    else:
        print("Invalid protocol")
        return None, None, None
    
    # Find the first slash to separate the host and path
    slash_index = rest.find("/")
    
    if slash_index == -1:
        # If there's no slash, the entire rest is the host, and path is "/"
        host = rest
        path = "/"
    else:
        # Split the rest into host and path
        host = rest[:slash_index]
        path = rest[slash_index:]
    
    return protocol, host, path

:
# url = "http://www.someSchool.edu/someDepartment/picture.gif"
# protocol, host, path = parse_url(url)
# print(f"Protocol: {protocol}")
# print(f"Host: {host}")
# print(f"Path: {path}")