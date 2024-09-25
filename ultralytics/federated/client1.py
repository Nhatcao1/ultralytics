import flwr as fl
from ultralytics import YOLO
import grpc
import torch

# Configuration for the model and dataset
PRETRAINED_PATH = "yolov8n.pt"
MODEL_PATH = "../cfg/models/v8/yolov8.yaml"
DATA_PATH = "coco8.yaml"
IMG_SIZE = 640

class YoloClient(fl.client.NumPyClient):
    def __init__(self):
        # Load the pre-trained YOLO model
        self.model = YOLO(MODEL_PATH).load(PRETRAINED_PATH).to("cpu")

    def get_parameters(self):
        # Retrieve and return model parameters as a list of NumPy arrays
        return [param.detach().cpu().numpy() for param in self.model.parameters()]

    def set_parameters(self, parameters):
        # Convert parameters from NumPy arrays to tensors and set them to the model
        params_dict = zip(self.model.state_dict().keys(), parameters)
        state_dict = {k: torch.tensor(v, device="cpu") for k, v in params_dict}
        self.model.load_state_dict(state_dict)

    def fit(self, parameters, config):
        # Set received parameters
        self.set_parameters(parameters)
        # Perform training on the specified dataset
        results = self.model.train(data=DATA_PATH, epochs=3, imgsz=IMG_SIZE, device="cpu")
        # Return the updated parameters and the number of examples used
        return self.get_parameters(), len(results)

    def evaluate(self, parameters, config):
        # Set the model parameters to the latest global model
        self.set_parameters(parameters)
        # Validate the model
        metrics = self.model.val(data=DATA_PATH, imgsz=IMG_SIZE, device="cpu")
        # Return loss, the number of evaluation examples used, and accuracy
        loss = metrics['loss']  # Assuming 'loss' is part of the returned metrics
        accuracy = metrics['accuracy']  # Assuming 'accuracy' is part of the returned metrics
        return float(loss), len(metrics), {"accuracy": float(accuracy)}

# Load SSL/TLS certificates for secure gRPC connection
with open("tls_certs/ca.crt", "rb") as f:
    trusted_certs = f.read()
with open("tls_certs/client.key", "rb") as f:
    private_key = f.read()
with open("tls_certs/client.crt", "rb") as f:
    certificate_chain = f.read()

# Create gRPC SSL credentials
grpc_ssl_credentials = grpc.ssl_channel_credentials(
    root_certificates=trusted_certs,
    private_key=private_key,
    certificate_chain=certificate_chain
)

# Create secure gRPC channel to the Flower server
options = [("grpc.max_receive_message_length", 1024**3)]
channel = grpc.secure_channel("master:8080", grpc_ssl_credentials, options)

# Manually handle communication using Flower’s `fl.client.grpc_client` logic
client = YoloClient()

# Perform federated learning manually using the client-side logic
def manual_federated_learning():
    # Simulate the Flower client lifecycle: join, train, report
    response = client.get_parameters()
    print(f"Initial parameters: {response}")
    
    # Perform training and update parameters
    new_params, _ = client.fit(response, config={})
    print(f"Updated parameters: {new_params}")
    
    # Send updated parameters back to server, simulate evaluation
    eval_response = client.evaluate(new_params, config={})
    print(f"Evaluation result: {eval_response}")

# Start the manual client process
manual_federated_learning()
