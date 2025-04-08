import grpc
from concurrent import futures
import network_and_telnet_pb2
import network_and_telnet_pb2_grpc
import subprocess
class ConnectivityService(network_and_telnet_pb2_grpc.ConnectivityServiceServicer):
    def CheckServerHealth(self, request, context):
        # Here you could implement actual health checking logic
        # For now, just return a mock healthy response
        return network_and_telnet_pb2.NetworkInfoResponse(
            message="Server is healthy",
            is_healthy=True
        )
class TelnetService(network_and_telnet_pb2_grpc.TelnetServiceServicer):
    def ExecuteCommand(self, request, context):
        # Execute the command via subprocess and return the result
        try:
            result = subprocess.run(request.command, shell=True, capture_output=True, text=True)
            return network_and_telnet_pb2.CommandResponse(result=result.stdout)
        except Exception as e:
            return network_and_telnet_pb2.CommandResponse(result=str(e))
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    network_and_telnet_pb2_grpc.add_ConnectivityServiceServicer_to_server(ConnectivityService(), server)
    network_and_telnet_pb2_grpc.add_TelnetServiceServicer_to_server(TelnetService(), server)
    server.add_insecure_port('[::]:50051')
    print("Server is running...")
    server.start()
    server.wait_for_termination()
if __name__ == '__main__':
    serve()