import sys
import socket
import ssl
from urllib.parse import urlparse

def monitor_url(url):
    """
    Monitors a single URL by establishing a TCP connection, sending an HTTP GET request,
    and handling any network-related errors.
    """
    try:
        # Parse the URL into components
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        port = parsed_url.port if parsed_url.port else (443 if parsed_url.scheme == 'https' else 80)
        path = parsed_url.path if parsed_url.path else '/'
        
        # Determine if SSL is required
        use_ssl = parsed_url.scheme == 'https'
        
        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 5-second timeout
        
        # Wrap socket with SSL if HTTPS is used
        if use_ssl:
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=host)
        
        # Connect to the server
        sock.connect((host, port))
        
        # Construct HTTP GET request
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        
        # Send the request
        sock.sendall(request.encode())
        
        # Receive the response
        response = b''
        while True:
            try:
                data = sock.recv(4096)
                if not data:
                    break
                response += data
            except socket.timeout:
                break  # Exit the loop if a timeout occurs during reception
        
        # Optionally, process the response as needed
        # For now, we'll just acknowledge success
        print(f"URL: {url}")
        print("Status: Success\n")
        
    except (socket.timeout, socket.error, ssl.SSLError) as e:
        print(f"URL: {url}")
        print("Status: Network Error\n")
        # Optionally, uncomment the following line for detailed error information (useful for debugging)
        # print(f"Error Details: {e}\n")
        
    except Exception as e:
        # Catch-all for any other exceptions
        print(f"URL: {url}")
        print("Status: Network Error\n")
        # Optionally, uncomment the following line for detailed error information (useful for debugging)
        # print(f"Unexpected Error: {e}\n")
        
    finally:
        try:
            sock.close()
        except:
            pass  # Ignore errors in closing the socket

def main():
    """
    Main function to read URLs from a file and monitor each one.
    """
    # Check command-line arguments
    if len(sys.argv) != 2:
        print('Usage: monitor urls_file')
        sys.exit(1)
    
    # Get the URLs file from command-line arguments
    urls_file = sys.argv[1]
    
    # Read URLs from the file
    try:
        with open(urls_file, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: The file '{urls_file}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading '{urls_file}': {e}")
        sys.exit(1)
    
    # Monitor each URL
    for url in urls:
        monitor_url(url)

if __name__ == "__main__":
    main()