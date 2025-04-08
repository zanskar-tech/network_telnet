import grpc
import network_and_telnet_pb2
import network_and_telnet_pb2_grpc

# Client to check server health
class ConnectivityClient:
    def __init__(self, address='localhost:50051'):
        self.address = address

    def check_server_health(self, client_ip: str):
        with grpc.insecure_channel(self.address) as channel:
            stub = network_and_telnet_pb2_grpc.ConnectivityServiceStub(channel)
            request = network_and_telnet_pb2.NetworkInfoRequest(client_ip=client_ip)
            response = stub.CheckServerHealth(request)
            print(f"Server Health Check: {response.message}, Healthy: {response.is_healthy}")
            return response.is_healthy

# Client to execute Telnet commands
class TelnetClient:
    def __init__(self, address='localhost:50051'):
        self.address = address
        self.channel = grpc.insecure_channel(self.address)
        self.stub = network_and_telnet_pb2_grpc.TelnetServiceStub(self.channel)

    def execute_command(self, command: str):
         with grpc.insecure_channel(self.address) as channel:
            stub = network_and_telnet_pb2_grpc.TelnetServiceStub(channel)
            request = network_and_telnet_pb2.CommandRequest(command=command)
            response = stub.ExecuteCommand(request)
            print(f"Command Result: {response.result}")
            return response.result

def run():
    server_address = '192.168.0.216:50051'  # Replace with your server address
    client_ip = '192.168.0.118'  # Replace with your client IP

    # Check server health
    connectivity_client = ConnectivityClient(server_address)
    if connectivity_client.check_server_health(client_ip):
        print("Server is healthy!")
    else:
        print("Server is not healthy!")

    # Execute a Telnet command (e.g., 'ls')
    telnet_client = TelnetClient(server_address)
    
    try:
        while True:
            # Accept user input for commands to send via Telnet
            command = input("Enter Telnet command (or type 'exit' to quit): ")
            if command.lower() == 'exit':
                print("Exiting Telnet session.")
                break
            telnet_client.execute_command(command)
    except KeyboardInterrupt:
        print("\nSession interrupted.")
    finally:
        telnet_client.close()

if __name__ == '__main__':
    run()



