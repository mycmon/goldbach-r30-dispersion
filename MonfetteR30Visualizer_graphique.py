import math
import numpy as np
import matplotlib.pyplot as plt

class MonfetteR30Visualizer:
    def __init__(self):
        self.R30_classes = [1, 7, 11, 13, 17, 19, 23, 29]
        
    def get_admissible_channels(self, N: int):
        N_mod = N % 30
        channels = []
        for p_mod in self.R30_classes:
            q_mod = (N_mod - p_mod) % 30
            if q_mod in self.R30_classes:
                if (p_mod, q_mod) not in channels and (q_mod, p_mod) not in channels:
                    channels.append((p_mod, q_mod))
        return channels

    def simple_sieve(self, limit: int):
        if limit < 2: return []
        sieve = [True] * (limit + 1)
        for p in range(2, int(math.sqrt(limit)) + 1):
            if sieve[p]:
                for i in range(p*p, limit + 1, p):
                    sieve[i] = False
        return [p for p, is_prime in enumerate(sieve) if is_prime and p > 5]

    def generate_plots(self, N: int, num_blocks: int = 8, block_size: int = 1000):
        channels = self.get_admissible_channels(N)
        z = int(math.sqrt(N))
        base_primes = self.simple_sieve(z)
        
        all_channel_rates = {}
        fano_indices = {}
        means = {}
        
        # Collecte des données
        for p_mod, q_mod in channels:
            block_rates = []
            current_p = p_mod if p_mod > 5 else p_mod + 30
            channel_name = f"({p_mod},{q_mod})"
            
            for b in range(num_blocks):
                survivors = 0
                tested = 0
                while tested < block_size and current_p <= N // 2:
                    current_q = N - current_p
                    p_eliminated = q_eliminated = False
                    
                    for pr in base_primes:
                        if pr >= current_p: break
                        if current_p % pr == 0: p_eliminated = True; break
                    if not p_eliminated:
                        for pr in base_primes:
                            if pr >= current_q: break
                            if current_q % pr == 0: q_eliminated = True; break
                                
                    if not p_eliminated and not q_eliminated:
                        survivors += 1
                    tested += 1
                    current_p += 30
                
                if tested > 0:
                    block_rates.append((survivors / tested) * 100)
            
            if block_rates:
                all_channel_rates[channel_name] = block_rates
                mean_rate = np.mean(block_rates)
                variance_rate = np.var(block_rates)
                means[channel_name] = mean_rate
                fano_indices[channel_name] = variance_rate / mean_rate if mean_rate > 0 else 0

        # --- TRACÉ DU GRAPHIQUE A : Taux de Survie par Bloc ---
        plt.figure(figsize=(10, 5.5))
        blocs_x = np.arange(1, len(block_rates) + 1)
        
        for channel, rates in all_channel_rates.items():
            plt.plot(blocs_x, rates, marker='o', linewidth=2, label=f"Canal {channel} (μ={means[channel]:.2f}%)")
            
        plt.title(f"Évolution locale du Taux de Survie par Bloc consécutif (N = {N})", fontsize=12, fontweight='bold')
        plt.xlabel("Index du Bloc de candidats (1000 paires par bloc)", fontsize=10)
        plt.ylabel("Taux de Survie aux ondes du Crible (%)", fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.6)
        
        val_max = max([max(r) for r in all_channel_rates.values()])
        plt.ylim(0, val_max + 5.0)
        plt.legend(loc="upper right", fancybox=True, shadow=True, fontsize=9)
        
        plt.tight_layout()
        filename_a = f"monfette_taux_survie_{N}.png"
        plt.savefig(filename_a, dpi=300)
        plt.close()
        print(f"✅ Graphique A enregistré : {filename_a}")

        # --- TRACÉ DU GRAPHIQUE B : Indice de Dispersion (CORRIGÉ AU MILIEU) ---
        plt.figure(figsize=(8, 5))
        channels_list = list(fano_indices.keys())
        indices_list = list(fano_indices.values())
        
        # Ligne rouge à y = 1.0
        plt.axhline(y=1.0, color='r', linestyle='--', linewidth=2, label="Modèle Aléatoire Pur / Poisson (Limite = 1.0)")
        
        # Barres vertes pour vos données
        bars = plt.bar(channels_list, indices_list, color='#2ca02c', alpha=0.8, edgecolor='black', width=0.4)
        
        # Zone verte translucide de haute régularité
        plt.axhspan(0, 0.25, color='green', alpha=0.1, label="Zone de Haute Régularité Structurelle R30")
        
        plt.title(f"Indice de Dispersion (Facteur de Fano) par Canal vs Hasard Pur", fontsize=12, fontweight='bold')
        plt.xlabel("Canaux Modulaires admissibles mod 30", fontsize=10)
        plt.ylabel("Indice de Dispersion (σ² / μ)", fontsize=10)
        plt.ylim(0, 1.2)
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        
        # CORRECTION : La légende est maintenant déplacée au centre du graphique (x=0.5, y=0.6)
        # Elle occupe l'espace vide idéal entre le haut des barres vertes et la ligne rouge de 1.0
        plt.legend(loc="center", bbox_to_anchor=(0.5, 0.60), fancybox=True, shadow=True, fontsize=9)
        
        # Affichage des valeurs numériques au-dessus de chaque barre verte
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f"{yval:.4f}", ha='center', va='bottom', fontweight='bold')
            
        plt.tight_layout()
        filename_b = f"monfette_dispersion_{N}.png"
        plt.savefig(filename_b, dpi=300)
        plt.close()
        print(f"✅ Graphique B corrigé (Légende au centre) enregistré : {filename_b}")

# --- CONFIGURATION DU TEST ---
if __name__ == "__main__":
    visualizer = MonfetteR30Visualizer()
    N_illustration = 1_000_000_008
    visualizer.generate_plots(N_illustration, num_blocks=8, block_size=1000)
