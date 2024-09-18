import grpc
import federatedlearning_pb2
import federatedlearning_pb2_grpc

def run_client():
    channel = grpc.insecure_channel('server_address:50051')
    stub = federatedlearning_pb2_grpc.FederatedLearningStub(channel)

    # Simulate training and get updated model parameters
    local_model = train_local_model()
    response = stub.SendModelUpdate(federatedlearning_pb2.ModelUpdate(model_parameters=local_model))

    # Fetch new global model parameters
    parameters = stub.GetModelParameters(federatedlearning_pb2.Request(client_id='client1'))
    update_local_model(local_model, parameters.model_parameters)

if __name__ == '__main__':
    run_client()
