# Inter-Channel Statistical Analysis and Local Dispersion Indicators

The empirical study of candidate pair distributions along the coordinate axes of the $\mathbb{R}_{30}$ modular structure reveals remarkable geometric and regularity properties. By isolating the local behavior of flows using rolling-window analyses and variance computations, it becomes possible to quantify the robustness of the model against the elimination mechanisms of the sieve.

## 1. Experimental Protocol Description

The model segments the space of even solutions into distinct channels derived from the multiplicative group $(\mathbb{Z}/30\mathbb{Z})^\times$. For a given even integer $N$, the candidates $(p, q)$ satisfying the relation $p + q = N$ are grouped according to their residual congruence classes mod 30.

### Figure 1: Combinatorial Activation Matrix Modulo 30

![](./fig1_activation_matrix.png)

This matrix maps the activation of finite residual classes and illustrates how multiplicative interactions organize themselves for a specific value of $N$. 

- XSG = Not Sophie Germain Number
- SG =  Sophie Germain Number

To finely measure dispersion and local regularity within these channels, the space of each admissible channel is partitioned into $B$ consecutive sub-blocks (for instance, 8 successive blocks each containing a fixed sample of 1,000 candidate pairs). A local sieve process of level $z = \sqrt{N}$ is applied to each block to evaluate the survival rate of the pairs.

### Figure 2: Circular Projection of the Phase Circle $\mathbb{R}_{30}$

![](./fig2_circle_R30.png)

Geometric visualization of the $\mathbb{R}_{30}$ phase space, highlighting the rigid symmetries of the 8 prime number classes.

The following statistical indicators are systematically computed for each channel:

- **Local mean ($\mu$):** The average survival rate across all blocks.
- **Standard deviation ($\sigma$) and Variance ($\sigma^2$):** Measuring the rate fluctuation from one block to another.
- **Dispersion Index (or Fano Factor, $I_D = \sigma^2 / \mu$):** Characterizing the mathematical nature of the underlying statistical distribution.

## 2. Analysis of Statistical Indicators and Interpretation

Data collected over several orders of magnitude (from $10^8$ up to $5 \times 10^9$) reveal three major characteristics of the modular organization.

### Figure 3: Spectral Envelope and Sieve Waves

![](./fig3_spectral_envelope.png)

Illustration of the sieve's exclusion forces and their harmonic modulations at a macroscopic scale.

### A. Extreme Under-Dispersion and the Fano Factor

The most significant indicator lies in the systematic suppression of the dispersion index ($I_D$). In a purely stochastic model—where the distribution of prime numbers would follow a Poisson process disconnected from any modular constraint—the dispersion index would fluctuate around $1.0$. However, empirical observations show uniformly low values, frequently dropping below the $0.1$ threshold.

### Plot B: Dispersion Index Analysis (Fano Factor) per Channel vs. Pure Randomness

The chart below illustrates this structural gap: while pure randomness sits on the red dashed line ($1.0$), the indexes of the actual channels remain crushed near the bottom, confirming a strict mathematical under-dispersion.

The alignment of sieve waves with the geometry of the 30-wheel generates a smoothing effect: candidate eliminations do not cluster chaotically, preventing the local emergence of large empty gaps or absolute "deserts" within the channel.

![](./monfette_dispersion_1000000008.png)

### B. Equidistribution of Simultaneous Channels

Examining the survival means ($\mu$) among the different channels of the same even target $N$ shows remarkable homogeneity. At the scale of $N = 1$ Billion, the channels configured for this point deploy with nearly identical survival averages: **7.12%** for the $(1,17)$ channel, **6.73%** for the $(7,11)$ channel, and **7.02%** for the $(19,29)$ channel.

### Plot A: Local Evolution of the Survival Rate per Consecutive Block

The plot below graphically displays the smooth and parallel trajectories of these flows across successive candidate blocks, ruling out any local anomalies or unexpected drops.

This observation validates the steady behavior of Dirichlet characters associated with the residual classes of the 30-wheel. The exclusion forces of the sieve are applied equitably, without introducing any major distortion or bias in favor of a specific tunnel.

![](./monfette_taux_survie_1000000008.png)

### Figure 4: The Goldbach Comet and its Macroscopic Distribution

Classical macroscopic perspective of the pair distribution, serving as a global baseline comparison for the microscopic regularity observed within the channels.

![](./fig4_goldbach_comet.png)

### C. The Global Non-Extinction Mechanism

The asymptotic trajectory analyzed up to 5 Billion ($N = 5\,000\,000\,030$) confirms the geometric robustness of the framework. Despite a drastic increase in the number of tested prime factors (moving from 1,226 to 7,001 factors), the standard deviation ($\sigma$) remains confined to around **1%**.

### Figure 5: Phase Duality Diagram of Candidates

Mapping of the symmetries and phase duality relations between the even and odd components of the model.

Even within the sub-blocks most exposed to cross-eliminations, the absolute number of surviving pairs remains significantly greater than zero. The decay of variance as $N$ grows renders the probability of a simultaneous fluctuation across all admissible channels extremely improbable.

![](./fig5_duality_diagram.png)

### Figure 6: Histogram of Kappa ($\kappa$) Regularity Indexes

Empirical statistical distribution validating the regularity indexes measured across the entire computational campaign.

![](./fig6_kappa_histogram.png)

## 3. Summary of Numerical Observations

The table below summarizes the evolution of the dispersion indicators and confirms the stabilization of flows across the tested configurations:

| **Value of N**         | **Sieve Level (z)** | **Number of Primes** | **Modular Channel**         | **Mean (μ)**                  | **Standard Dev. (σ)**   | **Dispersion Index (ID)**      |
| ---------------------- | ------------------- | -------------------- | --------------------------- | ----------------------------- | ----------------------- | ------------------------------ |
| **$100\,000\,018$**    | $10\,000$           | 1,226                | $(11,17)$ $(29,29)$         | $6.812\%$ $6.775\%$           | $0.936$ $0.772$         | $0.1286$ **$0.0881$**          |
| **$1\,000\,000\,008$** | $31\,622$           | 3,398                | $(1,17)$ $(7,11)$ $(19,29)$ | $7.125\%$ $6.738\%$ $7.025\%$ | $1.036$ $0.583$ $0.808$ | $0.1508$ **$0.0504$** $0.0931$ |
| **$5\,000\,000\,030$** | $70\,710$           | 7,001                | $(1,19)$ $(7,13)$           | $5.225\%$ $5.050\%$           | $1.062$ $0.886$         | $0.2161$ $0.1554$              |

## 4. Provisional Conclusion

The dispersion indicator approach shows that the simultaneous extinction of channels is counteracted by two empirical factors: a very low inter-block variance and a minimal Fano factor value. These observations suggest that the modular geometric structure imposes an internal regularity constraint, guaranteeing the maintenance of active candidate flows for any sampled even $N$.

### Figure 7: $3 \times 3 \times 3$ Topological Cube of Minimal Configurations

Three-dimensional modeling of non-empty overlap constraints (discussed in the appendices or in connection with the Lean 4 formalization).

![](./fig7_cube_3x3x3.png)
