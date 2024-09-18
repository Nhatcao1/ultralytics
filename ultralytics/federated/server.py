import flwr as fl
from typing import List, Dict, Tuple
import numpy as np

# Define a custom Federated Averaging strategy
class FedAvgStrategy(fl.server.strategy.FedAvg):
    def aggregate_fit(
        self,
        rnd: int,
        results: List[Tuple[fl.common.ClientProxy, fl.common.FitRes]],
        failures: List[BaseException],
    ) -> Tuple[Optional[fl.common.Weights], Dict[str, fl.common.Scalar]]:
        """Aggregate model weights using weighted average."""
        if not results:
            return None, {}
        
        # Aggregate weights
        weights = [parameters for client, parameters in results]
        new_weights = np.mean(weights, axis=0)  # Simple average of the weights

        # Return the new weights and no metrics
        return new_weights, {}

    def aggregate_evaluate(
        self,
        rnd: int,
        results: List[Tuple[fl.common.ClientProxy, fl.common.EvaluateRes]],
        failures: List[BaseException],
    ) -> Tuple[Optional[float], Dict[str, fl.common.Scalar]]:
        """Aggregate validation results."""
        if not results:
            return None, {}

        # Extract accuracy from results
        accuracies = [accuracy for client, accuracy in results]
        average_accuracy = np.mean(accuracies)

        # Return the average accuracy and no other metrics
        return average_accuracy, {}

# Initialize and start the Flower server with the custom strategy
def main():
    # Initialize strategy with the minimum number of clients set to 3
    strategy = FedAvgStrategy(min_available_clients=3)
    
    # Start server and listen for client connections to coordinate training and validation
    fl.server.start_server(server_address="0.0.0.0:8080", config={"num_rounds": 10}, strategy=strategy)

if __name__ == "__main__":
    main()
