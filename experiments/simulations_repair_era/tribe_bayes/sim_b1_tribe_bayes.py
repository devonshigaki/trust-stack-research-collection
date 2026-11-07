#!/usr/bin/env python3
import json
import numpy as np

def run_tribe_bayes_stream(N=1000, T=10, seed=42):
    np.random.seed(seed)
    
    # Ground truth storage
    true_S = np.zeros((N, T))
    true_lambda = np.zeros((N, T))
    
    # Filter tracking storage
    base_S = np.zeros((N, T))
    aug_S = np.zeros((N, T))
    aug_lambda = np.zeros((N, T))
    
    for i in range(N):
        S = 0.5
        lam = 0.5
        
        # Filter states
        x_base = np.array([0.5])
        P_base = 0.1
        
        x_aug = np.array([0.5, 0.5]) # [S, lambda]
        P_aug = np.eye(2) * 0.1
        
        for t in range(T):
            # 1. Ground truth dynamics
            # Lambda drifts heavily
            lam = np.clip(lam + np.random.normal(0, 0.2), 0.1, 0.9)
            
            # Interaction: environment offers E, delivers V
            E = np.random.uniform(0.2, 0.8)
            V = E + np.random.normal(0, 0.2)
            eps = V - E
            
            # Update state
            S = np.clip(S + lam * eps, 0, 1)
            
            true_S[i, t] = S
            true_lambda[i, t] = lam
            
            # 2. Observations
            y_behav = eps  # behavioral proxy
            # In-silico DMN BOLD proxy: tracks the true sensitivity to the offer
            y_bold = lam + np.random.normal(0, 0.02) 
            
            # 3. Baseline Kalman Filter (Tracks S, assumes fixed lambda=0.5)
            # Predict
            x_base_pred = x_base + 0.5 * eps
            P_base_pred = P_base + 0.1
            # Update (only observes behavioral proxy, which gives noisy hint about S drift)
            y_state_noisy = S + np.random.normal(0, 0.6)
            K_base = P_base_pred / (P_base_pred + 0.6**2)
            x_base = x_base_pred + K_base * (y_state_noisy - x_base_pred)
            P_base = (1 - K_base) * P_base_pred
            
            base_S[i, t] = x_base[0]
            
            # 4. Augmented Kalman Filter (Tracks S and Lambda using BOLD)
            # Predict
            x_aug_pred = np.array([x_aug[0] + x_aug[1] * eps, x_aug[1]])
            # Jacobian of f(x) = [S + lam*eps, lam]
            F = np.array([[1, eps], [0, 1]])
            Q = np.array([[0.01, 0], [0, 0.05**2]])
            P_aug_pred = F @ P_aug @ F.T + Q
            
            # Update using y = [y_state_noisy, y_bold]
            H = np.array([
                [1, 0],
                [0, 1]
            ])
            R = np.array([[0.4**2, 0], [0, 0.02**2]])
            
            S_mat = H @ P_aug_pred @ H.T + R
            K_aug = P_aug_pred @ H.T @ np.linalg.inv(S_mat)
            
            y_vec = np.array([y_state_noisy, y_bold])
            hx = np.array([x_aug_pred[0], x_aug_pred[1]])
            
            x_aug = x_aug_pred + K_aug @ (y_vec - hx)
            P_aug = (np.eye(2) - K_aug @ H) @ P_aug_pred
            
            x_aug[0] = np.clip(x_aug[0], 0, 1)
            x_aug[1] = np.clip(x_aug[1], 0.1, 0.9)
            
            aug_S[i, t] = x_aug[0]
            aug_lambda[i, t] = x_aug[1]
            
    # Calculate Metrics
    mse_base = np.mean((true_S - base_S)**2)
    mse_aug = np.mean((true_S - aug_S)**2)
    mse_reduction = (mse_base - mse_aug) / mse_base
    
    # Flatten arrays for correlation
    r_lambda = np.corrcoef(true_lambda.flatten(), aug_lambda.flatten())[0, 1]
    
    # Verdicts
    c1_pass = mse_reduction >= 0.40
    c2_pass = r_lambda >= 0.85
    
    verdict = "COMPOUND PASS" if (c1_pass and c2_pass) else "FAIL"
    
    results = {
        "mse_baseline": mse_base,
        "mse_augmented": mse_aug,
        "mse_reduction_pct": mse_reduction * 100,
        "lambda_correlation": r_lambda,
        "C1_pass": bool(c1_pass),
        "C2_pass": bool(c2_pass),
        "verdict": verdict
    }
    
    with open("results/b1_results.json", "w") as f:
        json.dump(results, f, indent=2)
        
    print(f"TRIBE-BAYES-STREAM Results:")
    print(f"MSE Reduction: {mse_reduction*100:.1f}% (Req >= 40.0%) -> {'PASS' if c1_pass else 'FAIL'}")
    print(f"Lambda Tracking Correlation: {r_lambda:.3f} (Req >= 0.85) -> {'PASS' if c2_pass else 'FAIL'}")
    print(f"Verdict: {verdict}")

if __name__ == "__main__":
    import os
    os.makedirs("results", exist_ok=True)
    run_tribe_bayes_stream()
