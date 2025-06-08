import numpy as np
from collections import deque
import random

def simulate_mm1_queue(arrival_rate, service_rate, simulation_time, seed=None):
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)

    # Initialize simulation variables
    current_time = 0.0
    server_busy = False
    server_start_time = 0.0
    next_departure_time = float('inf')
    queue = deque()  # Queue of customer arrival times

    # Statistics collection
    customer_stats = []  # List of (arrival_time, service_start_time, departure_time)
    last_event_time = 0.0
    state_time = {0: 0.0}  # Time spent with n customers in system
    current_state = 0  # Current number of customers in system

    # Generate first arrival
    next_arrival_time = np.random.exponential(scale=1.0/arrival_rate)

    # Event simulation loop
    while current_time < simulation_time:
        # Determine next event (arrival or departure)
        if next_arrival_time <= next_departure_time:
            # Process an arrival

            # Update time spent in current state
            state_time[current_state] = state_time.get(current_state, 0) + (next_arrival_time - last_event_time)
            last_event_time = next_arrival_time
            current_time = next_arrival_time

            # Schedule next arrival
            next_arrival_time = current_time + np.random.exponential(scale=1.0/arrival_rate)

            if not server_busy:
                # Server is idle, start service immediately
                server_busy = True
                server_start_time = current_time
                service_time = np.random.exponential(scale=1.0/service_rate)
                next_departure_time = current_time + service_time
                customer_stats.append((current_time, current_time, next_departure_time))
            else:
                # Server is busy, join the queue
                queue.append(current_time)

            # Increment state (customer count)
            current_state += 1

        else:
            # Process a departure

            # Update time spent in current state
            state_time[current_state] = state_time.get(current_state, 0) + (next_departure_time - last_event_time)
            last_event_time = next_departure_time
            current_time = next_departure_time

            # Decrement state (customer count)
            current_state -= 1

            if queue:
                # Get next customer from queue
                arrival_time = queue.popleft()
                service_time = np.random.exponential(scale=1.0/service_rate)
                next_departure_time = current_time + service_time
                customer_stats.append((arrival_time, current_time, next_departure_time))
                server_start_time = current_time
            else:
                # No more customers to serve
                server_busy = False
                next_departure_time = float('inf')

    # Final update for time in last state
    state_time[current_state] = state_time.get(current_state, 0) + (simulation_time - last_event_time)

    # Calculate statistics
    total_customers = len(customer_stats)

    # Consider only customers who completed service
    completed_customers = sum(1 for _, _, departure_time in customer_stats if departure_time <= simulation_time)

    # Calculate system time and queue time for completed customers
    system_times = []
    queue_times = []
    server_busy_time = 0

    for arrival_time, service_start_time, departure_time in customer_stats:
        if departure_time <= simulation_time:
            system_time = departure_time - arrival_time
            queue_time = service_start_time - arrival_time
            system_times.append(system_time)
            queue_times.append(queue_time)
            server_busy_time += (departure_time - service_start_time)

    # Add time for last customer being served if simulation ended while serving
    if server_busy and next_departure_time > simulation_time:
        server_busy_time += (simulation_time - server_start_time)

    # Calculate averages
    avg_system_time = np.mean(system_times) if system_times else 0
    avg_queue_time = np.mean(queue_times) if queue_times else 0
    server_utilization = server_busy_time / simulation_time

    # Calculate time-averaged number of customers
    total_simulation_time = simulation_time
    avg_system_length = sum(n * t for n, t in state_time.items()) / total_simulation_time
    avg_queue_length = sum(max(0, n-1) * t for n, t in state_time.items()) / total_simulation_time

    # Calculate state probabilities
    state_probabilities = {n: t / total_simulation_time for n, t in state_time.items()}

    return {
        "total_customers": total_customers,
        "completed_customers": completed_customers,
        "total_system_time": sum(system_times),
        "total_queue_time": sum(queue_times),
        "server_busy_time": server_busy_time,
        "average_system_time": avg_system_time,
        "average_queue_time": avg_queue_time,
        "server_utilization": server_utilization,
        "average_system_length": avg_system_length,
        "average_queue_length": avg_queue_length,
        "state_probabilities": state_probabilities
    }

def run_mm1_simulation(arrival_rate=4, service_rate=12, simulation_time=20000, seed=42):
    """
    Run an M/M/1 queue simulation with specified parameters and display results.
    """
    # Run the simulation
    results = simulate_mm1_queue(arrival_rate, service_rate, simulation_time, seed)

    # Display results
    print(f"M/M/1 Queue Simulation Results")
    print(f"==============================")
    print(f"Parameters:")
    print(f"  λ (arrival rate): {arrival_rate} customers/minute")
    print(f"  μ (service rate): {service_rate} customers/minute")
    print(f"  ρ (traffic intensity): {arrival_rate/service_rate:.4f}")
    print(f"  Simulation duration: {simulation_time} minutes")
    print(f"  Random seed: {seed}")
    print()
    print(f"Results:")
    print(f"  Total customers arrived: {results['total_customers']}")
    print(f"  Total customers served: {results['completed_customers']}")
    print(f"  Total time spent in system: {results['total_system_time']:.2f} minutes")
    print(f"  Total time spent in queue: {results['total_queue_time']:.2f} minutes")
    print(f"  Total server busy time: {results['server_busy_time']:.2f} minutes")
    print(f"  Average time in system: {results['average_system_time']*60:.4f} minutes")
    print(f"  Average time in queue: {results['average_queue_time']*60:.4f} minutes")
    print(f"  Server utilization: {results['server_utilization']:.4f}")
    print(f"  Time-averaged number of customers in system: {results['average_system_length']:.4f}")
    print(f"  Time-averaged number of customers in queue: {results['average_queue_length']:.4f}")

    print("\nProportion of time with n customers in system:")
    max_state = max(results['state_probabilities'].keys())
    for i in range(max_state + 1):
        prob = results['state_probabilities'].get(i, 0)
        print(f"  n = {i}: {prob:.4f}")

    return results

if __name__ == "__main__":
    # Fixed parameters based on user's request
    arrival_rate = 10  # λ = 4 customers per minute
    service_rate = 12  # μ = 12 customers per minute
    simulation_time = 10000  # Increased from 10000 to 20000 minutes for better stability
    seed = 42  # Fixed seed for reproducibility

    # Run the simulation
    results = run_mm1_simulation(arrival_rate, service_rate, simulation_time, seed)