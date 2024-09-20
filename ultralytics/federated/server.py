import flwr as fl
from typing import List, Dict, Tuple, Optional
import numpy as np
from pathlib import Path

# Define a custom Federated Averaging strategy
class FedAvgStrategy(fl.server.strategy.FedAvg):
    def aggregate_fit(
        self,
        rnd: int,
        results: List[Tuple[fl.server.client_proxy.ClientProxy, fl.common.FitRes]],
        failures: List[BaseException],
    ) -> Tuple[Optional[fl.common.Parameters], Dict[str, fl.common.Scalar]]:
        """Aggregate model weights using weighted average."""
        if not results:
            return None, {}
        
        # Aggregate parameters
        parameters = [fit_res.parameters for _, fit_res in results]
        new_parameters = np.mean(parameters, axis=0)  # Simple average of the parameters

        # Return the new parameters and no metrics
        return new_parameters, {}

    def aggregate_evaluate(
        self,
        rnd: int,
        results: List[Tuple[fl.server.client_proxy.ClientProxy, fl.common.EvaluateRes]],
        failures: List[BaseException],
    ) -> Tuple[Optional[float], Dict[str, fl.common.Scalar]]:
        """Aggregate validation results."""
        if not results:
            return None, {}

        # Extract accuracy from results
        accuracies = [evaluate_res.metrics["accuracy"] for _, evaluate_res in results]
        average_accuracy = np.mean(accuracies)

        # Return the average accuracy and no other metrics
        return average_accuracy, {}

# Initialize and start the Flower server with the custom strategy
def main():
    strategy = FedAvgStrategy(min_available_clients=3)

    # Define SSL credentials
    root_certificate = Path("tls_certs/ca.crt").read_bytes()
    server_certificate = Path("tls_certs/server.crt").read_bytes()
    server_key = Path("tls_certs/server.key").read_bytes()

    # Start server with gRPC configuration for large messages and SSL/TLS
    fl.server.start_server(
        server_address="0.0.0.0:8080",
        strategy=strategy,
        config=fl.server.ServerConfig(num_rounds=10),
        grpc_max_message_length=1024**3,
        certificates=(root_certificate, server_certificate, server_key)
    )

if __name__ == "__main__":
    main()
