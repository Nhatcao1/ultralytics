import flwr as fl
from ultralytics import YOLO
import torch
from pathlib import Path
import grpc 

# Configuration for the model and dataset
MODEL_PATH = "yolov8n.pt"
DATA_PATH = "coco8.yaml"
IMG_SIZE = 640

class YoloClient(fl.client.NumPyClient):
    def __init__(self):
        # Load the pre-trained YOLO model to run on CPU
        self.model = YOLO(MODEL_PATH).to("cpu")

    def get_parameters(self, **kwargs):
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
        # Retrieve dataset size from the training results
        num_examples = len(results.dataset)  # Number of examples used in training
        # Return the updated parameters and the number of examples used
        return self.get_parameters(), num_examples, {}

    def evaluate(self, parameters, config):
        # Set the model parameters to the latest global model
        self.set_parameters(parameters)
        # Validate the model
        metrics = self.model.val(data=DATA_PATH, imgsz=IMG_SIZE, device="cpu")
        # YOLO's validation results come as a dict with keys like "metrics/mAP50"
        loss = metrics.box_loss  # Adjust this depending on the actual YOLO metrics
        accuracy = metrics.results[0]  # You can adjust based on specific metric type
        return float(loss), len(metrics.dataset), {"accuracy": float(accuracy)}

# Start the Flower client with SSL/TLS
fl.client.start_client(
    server_address="192.168.124.2:8080",  # Replace with the actual server address
    client=YoloClient(),           # Use the YOLO client
    root_certificates=Path("tls_certs/server.pem").read_bytes()  # Use the server.pem file as the certificate
)
