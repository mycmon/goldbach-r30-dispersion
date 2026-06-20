import math
import time
import numpy as np
from typing import List, Tuple, Dict

class MonfetteR30StatisticalAnalyzer:
    def __init__(self):
        # Les 8 classes résiduelles fondamentales de la roue de 30
        self.R30_classes = [1, 7, 11, 13, 17, 19, 23, 29]
        
    def get_admissible_channels(self, N: int) -> List[Tuple[int, int]]:
        """Détermine les canaux admissibles mod 30."""
        N_mod = N % 30
        channels = []
        for p_mod in self.R30_classes:
            q_mod = (N_mod - p_mod) % 30
            if q_mod in self.R30_classes:
                if (p_mod, q_mod) not in channels and (q_mod, p_mod) not in channels:
                    channels.append((p_mod, q_mod))
        return channels

    def simple_sieve(self, limit: int) -> List[int]:
        """Génère les facteurs premiers jusqu'à la limite du crible."""
        if limit < 2: return []
        sieve = [True] * (limit + 1)
        for p in range(2, int(math.sqrt(limit)) + 1):
            if sieve[p]:
                for i in range(p*p, limit + 1, p):
                    sieve[i] = False
        return [p for p, is_prime in enumerate(sieve) if is_prime and p > 5]

    def analyze_variance_and_dispersion(self, N: int, num_blocks: int = 10, block_size: int = 1000) -> Dict:
        """
        Analyse la variance du taux de survie à travers plusieurs blocs consécutifs
        pour chaque canal admissible afin de détecter les anomalies ou la régularité locale.
        """
        start_time = time.time()
        channels = self.get_admissible_channels(N)
        z = int(math.sqrt(N))
        base_primes = self.simple_sieve(z)
        
        print(f"\n" + "="*70)
        print(f"--- ANALYSE STATISTIQUE AVANCÉE R30 | N = {N} ---")
        print(f"Crible (z = √N) : {z} ({len(base_primes)} premiers) | Configuration : {num_blocks} blocs de {block_size} paires")
        
        channel_statistics = {}
        
        for p_mod, q_mod in channels:
            block_rates = []
            current_p = p_mod if p_mod > 5 else p_mod + 30
            
            # Boucle à travers les différents blocs pour mesurer la variance locale
            for b in range(num_blocks):
                survivors = 0
                tested = 0
                
                while tested < block_size and current_p <= N // 2:
                    current_q = N - current_p
                    p_eliminated = False
                    q_eliminated = False
                    
                    for pr in base_primes:
                        if pr >= current_p: break
                        if current_p % pr == 0:
                            p_eliminated = True
                            break
                            
                    if not p_eliminated:
                        for pr in base_primes:
                            if pr >= current_q: break
                            if current_q % pr == 0:
                                q_eliminated = True
                                break
                                
                    if not p_eliminated and not q_eliminated:
                        survivors += 1
                        
                    tested += 1
                    current_p += 30
                
                if tested > 0:
                    rate = (survivors / tested) * 100
                    block_rates.append(rate)
                else:
                    break # On a dépassé N // 2
            
            # Calcul des indicateurs de variance si on a des blocs complets
            if block_rates:
                mean_rate = np.mean(block_rates)
                variance_rate = np.var(block_rates)
                std_dev_rate = np.std(block_rates)
                
                # Facteur de Fano local (Variance / Moyenne) normalisé (sur les effectifs bruts sous-jacents)
                # Utile pour valider la non-extinction structurelle face au hasard pur
                fano_factor = variance_rate / mean_rate if mean_rate > 0 else 0
                
                channel_name = f"({p_mod},{q_mod})"
                channel_statistics[channel_name] = {
                    "rates_per_block": [round(r, 2) for r in block_rates],
                    "mean_%": round(mean_rate, 3),
                    "variance": round(variance_rate, 4),
                    "std_dev": round(std_dev_rate, 4),
                    "fano_index": round(fano_factor, 4)
                }
                
                # Affichage des métriques pour ce canal
                print(f"\n  Canal {channel_name} :")
                print(f"    Taux par bloc : {channel_statistics[channel_name]['rates_per_block']}")
                print(f"    Moyenne (μ)    : {channel_statistics[channel_name]['mean_%']}%")
                print(f"    Écart-type (σ) : {channel_statistics[channel_name]['std_dev']}")
                print(f"    Variance (σ²)  : {channel_statistics[channel_name]['variance']}")
                print(f"    Indice Dispersion : {channel_statistics[channel_name]['fano_index']} " + 
                      ("-> [HAUTE RÉGULARITÉ STRUCTURALE 🛡️]" if fano_factor < 0.1 else "-> [COMPORTEMENT FLUIDE]"))
        
        execution_time = time.time() - start_time
        print(f"\nTemps d'exécution : {round(execution_time, 3)} secondes.")
        return channel_statistics

# --- EXTENSION DE L'EXPÉRIENCE ---
if __name__ == "__main__":
    analyzer = MonfetteR30StatisticalAnalyzer()
    
    # Nous testons ici 3 ordres de grandeur différents pour analyser la dynamique de la variance asymptotique
    target_numbers = [
        100_000_018,    # 100 Millions
        1_000_000_008,  # 1 Milliard
        5_000_000_030   # 5 Milliards
    ]
    
    for N in target_numbers:
        # On découpe l'analyse locale en 8 blocs successifs de 1000 paires chacun
        analyzer.analyze_variance_and_dispersion(N, num_blocks=8, block_size=1000)
