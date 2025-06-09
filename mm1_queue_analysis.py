import numpy as np
import matplotlib.pyplot as plt
from mm1_queue_simulation import simulate_mm1_queue

# Define scenarios for different utilization factors
scenarios = [
    {"label": "ρ = 0.5", "arrival_rate": 6, "service_rate": 12},
    {"label": "ρ = 0.8", "arrival_rate": 9.6, "service_rate": 12},
    {"label": "ρ = 0.9", "arrival_rate": 10.8, "service_rate": 12},
]

simulation_time = 20000  # Long enough for stability
seed = 42

rhos = []
sim_wqs = []

for scenario in scenarios:
    arrival_rate = scenario["arrival_rate"]
    service_rate = scenario["service_rate"]
    rho = arrival_rate / service_rate
    rhos.append(rho)
    results = simulate_mm1_queue(arrival_rate, service_rate, simulation_time, seed)
    sim_wqs.append(results["average_queue_time"])  # in minutes

# Theoretical Wq curve for a range of rho
mu = 12
rho_curve = np.linspace(0.01, 0.99, 100)
wq_theoretical = rho_curve / (mu * (1 - rho_curve))

plt.figure(figsize=(8, 5))
plt.plot(rho_curve, wq_theoretical, label="Theoretical $W_q$")
plt.scatter(rhos, sim_wqs, color="red", zorder=5, label="Simulated $W_q$")
for i, scenario in enumerate(scenarios):
    plt.annotate(scenario["label"], (rhos[i], sim_wqs[i]), textcoords="offset points", xytext=(0,10), ha='center')
plt.xlabel("Utilization $\\rho$")
plt.ylabel("Average waiting time in queue $W_q$ (minutes)")
plt.title("M/M/1 Queue: Simulated vs Theoretical $W_q$")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

print("Observation: As utilization (ρ) approaches 1, the average waiting time in the queue ($W_q$) increases rapidly, diverging to infinity. This matches the theoretical prediction for M/M/1 queues, where the system becomes unstable as ρ → 1.")
