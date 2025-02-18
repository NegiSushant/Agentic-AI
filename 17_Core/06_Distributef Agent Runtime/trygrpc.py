from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntimeHost

host = GrpcWorkerAgentRuntimeHost(address="localhost:50051")
host.start()  #Start a host service in the background.

#The above code starts the host service in the background and accepts worker connections on port 50051.

