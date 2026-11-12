import numpy as np
import json
import matplotlib.pyplot as plt
import os

# Set seed for reproducibility
np.random.seed(42)

# --- SIM AXIOM-1: Trace vs Prototype ---
# N=1000 consumers, 100 epochs. Shock at t=50.
N = 1000
T = 100
t_shock = 50
shock_duration = 10

# Ground truth behavior risk: 0 is good, 1 is bad.
# Starts at 0.1. Shock raises it to 0.8 temporarily, then back to 0.1.
true_risk = np.ones((N, T)) * 0.1
for i in range(N):
    true_risk[i, t_shock:t_shock+shock_duration] = 0.8 + np.random.normal(0, 0.05, shock_duration)
    true_risk[i, t_shock+shock_duration:] = 0.1 + np.random.normal(0, 0.02, T - (t_shock+shock_duration))

# Prototype Underwriter (Kalman Filter-like, slow adaptation)
prototype_score = np.zeros((N, T))
prototype_score[:, 0] = 0.1
alpha_proto = 0.1 # Slow update (prior rigidity)

# Multiple-Trace Underwriter (Similarity-kernel over recent events)
trace_score = np.zeros((N, T))
trace_score[:, 0] = 0.1
alpha_trace = 0.6 # Fast contextual matching

for t in range(1, T):
    obs = true_risk[:, t] + np.random.normal(0, 0.1, N) # Noisy observation
    
    # Prototype gets stuck on historical average
    prototype_score[:, t] = (1 - alpha_proto) * prototype_score[:, t-1] + alpha_proto * obs
    
    # Trace matches current context heavily
    trace_score[:, t] = (1 - alpha_trace) * trace_score[:, t-1] + alpha_trace * obs

# Evaluate False Positives (Denying when ground truth is actually good again)
# Recovery phase is t=60 to 80
recovery_phase = slice(t_shock + shock_duration, t_shock + shock_duration + 20)
# Ground truth is back to ~0.1. We define denial as score > 0.4
proto_denials = np.mean(prototype_score[:, recovery_phase] > 0.4)
trace_denials = np.mean(trace_score[:, recovery_phase] > 0.4)

false_positive_ratio = proto_denials / trace_denials if trace_denials > 0 else float('inf')

# Time to recovery (time until average score drops below 0.2)
proto_t_rec = np.argmax(np.mean(prototype_score[:, t_shock+shock_duration:], axis=0) < 0.2)
trace_t_rec = np.argmax(np.mean(trace_score[:, t_shock+shock_duration:], axis=0) < 0.2)
recovery_ratio = trace_t_rec / proto_t_rec if proto_t_rec > 0 else 1.0

ax1_pass = (false_positive_ratio >= 3.0) and (recovery_ratio <= 0.50)

# --- SIM AXIOM-2: Beinhocker Evolutionary Assembly ---
# F=100 firms, 200 epochs of capital accumulation under resource scarcity shock
F = 100
T_econ = 200
shock_t_econ = 100

# Monolithic firms (gamma_M = 1.0, low ASI)
monolithic_capital = np.ones(F//2) * 100.0
# Decentralized, semi-permeable firms (gamma_M = 0.15, high ASI >= 15)
semiperm_capital = np.ones(F//2) * 100.0

monolithic_history = np.zeros((F//2, T_econ))
semiperm_history = np.zeros((F//2, T_econ))

for t in range(T_econ):
    # Base growth
    growth_m = np.random.normal(1.0, 2.0, F//2)
    growth_s = np.random.normal(1.0, 2.0, F//2)
    
    # Shock at t=100: Resource scarcity & noise
    if t >= shock_t_econ and t < shock_t_econ + 20:
        # Monolithic takes full hit (entropy penetrates 100%)
        growth_m -= np.random.normal(5.0, 3.0, F//2)
        # Semi-permeable buffers the shock (entropy restricted by membrane gamma=0.15)
        growth_s -= np.random.normal(5.0, 3.0, F//2) * 0.15
        
    monolithic_capital += growth_m
    semiperm_capital += growth_s
    
    # Extinction boundary
    monolithic_capital[monolithic_capital <= 0] = 0
    semiperm_capital[semiperm_capital <= 0] = 0
    
    monolithic_history[:, t] = monolithic_capital
    semiperm_history[:, t] = semiperm_capital

mono_survival = np.mean(monolithic_capital > 0)
semi_survival = np.mean(semiperm_capital > 0)
survival_ratio = semi_survival / mono_survival if mono_survival > 0 else float('inf')

mono_reserves = np.mean(monolithic_capital)
semi_reserves = np.mean(semiperm_capital)
delta_reserves = semi_reserves - mono_reserves

ax2_pass = (survival_ratio >= 2.5) and (delta_reserves > 0)


# --- Results Generation ---
results = {
    "Sim_AXIOM_1": {
        "false_positive_ratio": float(false_positive_ratio),
        "recovery_ratio": float(recovery_ratio),
        "criterion_A_pass": bool(false_positive_ratio >= 3.0),
        "criterion_B_pass": bool(recovery_ratio <= 0.50),
        "compound_pass": bool(ax1_pass)
    },
    "Sim_AXIOM_2": {
        "survival_ratio": float(survival_ratio),
        "delta_reserves": float(delta_reserves),
        "criterion_A_pass": bool(survival_ratio >= 2.5),
        "criterion_B_pass": bool(delta_reserves > 0),
        "compound_pass": bool(ax2_pass)
    }
}

with open("sim_axiom_results.json", "w") as f:
    json.dump(results, f, indent=4)

# --- Plotting ---
plt.figure(figsize=(10, 5))
plt.plot(np.mean(true_risk, axis=0), label="Ground Truth Risk", color="black", linestyle="--")
plt.plot(np.mean(prototype_score, axis=0), label="Prototype Underwriter (Rigid)", color="red")
plt.plot(np.mean(trace_score, axis=0), label="Multiple-Trace Underwriter (Adaptive)", color="blue")
plt.axvspan(t_shock, t_shock+shock_duration, color='gray', alpha=0.2, label="Macro Shock")
plt.title("Sim AXIOM-1: Trace vs Prototype Underwriting")
plt.xlabel("Epoch")
plt.ylabel("Assessed Risk Score")
plt.legend()
plt.tight_layout()
plt.savefig("fig_sim_axiom_trace_vs_proto.png")
plt.close()

plt.figure(figsize=(10, 5))
plt.plot(np.mean(monolithic_history, axis=0), label="Monolithic Firms (gamma=1.0)", color="red")
plt.plot(np.mean(semiperm_history, axis=0), label="Semi-Permeable Firms (gamma=0.15)", color="blue")
plt.axvspan(shock_t_econ, shock_t_econ+20, color='gray', alpha=0.2, label="Resource Scarcity Shock")
plt.title("Sim AXIOM-2: Beinhocker Evolutionary Assembly")
plt.xlabel("Epoch")
plt.ylabel("Mean Firm Capital Reserves")
plt.legend()
plt.tight_layout()
plt.savefig("fig_sim_axiom_beinhocker.png")
plt.close()

print("Sim AXIOM Series Executed Successfully.")
print(json.dumps(results, indent=2))
