import flwr as fl
from ultralytics import YOLO

# Configuration for the model and dataset
MODEL_PATH = "yolov8n.pt"
DATA_PATH = "coco8.yaml"
IMG_SIZE = 640

class YoloClient(fl.client.NumPyClient):
    def __init__(self):
        # Load the pre-trained YOLO model
        self.model = YOLO(MODEL_PATH)
    
    def get_parameters(self):
        # Retrieve and return model parameters
        return self.model.parameters()
    
    def set_parameters(self, parameters):
        # Set model parameters received from the server
        self.model.parameters(parameters)
    
    def fit(self, parameters, config):
        # Set received parameters
        self.set_parameters(parameters)
        
        # Perform training on the specified dataset
        results = self.model.train(data=DATA_PATH, epochs=3, imgsz=IMG_SIZE, device="auto")
        
        # Return the updated parameters and the number of examples used
        return self.get_parameters(), len(results)
    
    def evaluate(self, parameters, config):
        # Set the model parameters to the latest global model
        self.set_parameters(parameters)
        
        # Validate the model
        metrics = self.model.val(data=DATA_PATH, imgsz=IMG_SIZE)
        
        # Return accuracy and the number of evaluation examples used
        loss = metrics['loss']  # Assuming 'loss' is part of the returned metrics
        accuracy = metrics['accuracy']  # Assuming 'accuracy' is part of the returned metrics
        return float(loss), len(metrics), {"accuracy": float(accuracy)}

# Start the Flower client
fl.client.start_numpy_client(server_address="localhost:8080", client=YoloClient())
