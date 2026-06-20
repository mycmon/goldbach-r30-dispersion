import math
import time
from typing import List, Tuple, Dict

class MonfetteR30Analyzer:
    def __init__(self):
        # Les 8 classes résiduelles fondamentales de la roue de 30 (coprimes à 30)
        self.R30_classes = [1, 7, 11, 13, 17, 19, 23, 29]
        
    def get_admissible_channels(self, N: int) -> List[Tuple[int, int]]:
        """
        Détermine les canaux admissibles (p_mod, q_mod) mod 30 tels que :
        p_mod + q_mod = N (mod 30) avec p_mod, q_mod dans R30.
        Le théorème TH13 garantit qu'il y en a toujours au moins 3 (paires ordonnées).
        """
        N_mod = N % 30
        channels = []
        for p_mod in self.R30_classes:
            q_mod = (N_mod - p_mod) % 30
            if q_mod in self.R30_classes:
                # Évite les doublons non ordonnés pour l'analyse des paires uniques
                if (p_mod, q_mod) not in channels and (q_mod, p_mod) not in channels:
                    channels.append((p_mod, q_mod))
        return channels

    def simple_sieve(self, limit: int) -> List[int]:
        """Génère les petits nombres premiers jusqu'à la limite pour le crible."""
        if limit < 2: return []
        sieve = [True] * (limit + 1)
        for p in range(2, int(math.sqrt(limit)) + 1):
            if sieve[p]:
                for i in range(p*p, limit + 1, p):
                    sieve[i] = False
        return [p for p, is_prime in enumerate(sieve) if is_prime and p > 1]

    def analyze_extinction_risk(self, N: int, sample_size: int = 10000) -> Dict:
        """
        Analyse la survie des candidats dans les canaux admissibles pour un grand N.
        On applique un crible jusqu'à z = sqrt(N).
        """
        start_time = time.time()
        channels = self.get_admissible_channels(N)
        z = int(math.sqrt(N))
        
        # Obtenir les bases de cribles (on ignore 2, 3, 5 car déjà gérés par R30)
        base_primes = [p for p in self.simple_sieve(z) if p > 5]
        
        channel_results = {}
        any_channel_survives = False
        
        print(f"\n" + "="*50)
        print(f"--- Analyse Monfette R30 pour N = {N} ---")
        print(f"Niveau du crible (z = √N) : {z} ({len(base_primes)} facteurs premiers à tester)")
        print(f"Nombre de canaux admissibles identifiés (TH13) : {len(channels)}")
        
        for p_mod, q_mod in channels:
            survivors = 0
            tested = 0
            
            # On cherche des candidats p tel que p = p_mod (mod 30) et q = N - p = q_mod (mod 30)
            current_p = p_mod if p_mod > 5 else p_mod + 30
            
            while current_p <= N // 2 and tested < sample_size:
                current_q = N - current_p
                
                p_eliminated = False
                q_eliminated = False
                
                for pr in base_primes:
                    if pr >= current_p: 
                        break
                    if current_p % pr == 0:
                        p_eliminated = True
                        break
                        
                if not p_eliminated:
                    for pr in base_primes:
                        if pr >= current_q:
                            break
                        if current_q % pr == 0:
                            q_eliminated = True
                            break
                
                # Un candidat couple survit si p ET q passent le crible local
                if not p_eliminated and not q_eliminated:
                    survivors += 1
                
                tested += 1
                current_p += 30
            
            survival_rate = (survivors / tested) * 100 if tested > 0 else 0
            channel_results[f"({p_mod},{q_mod})"] = {
                "tested": tested,
                "survivors": survivors,
                "survival_rate_percent": round(survival_rate, 4)
            }
            
            if survivors > 0:
                any_channel_survives = True
                
        execution_time = time.time() - start_time
        
        # Affichage direct des résultats pour ce nombre
        for channel, data in channel_results.items():
            print(f"  Canal {channel} : {data['survivors']} couples ont survécu sur {data['tested']} testés ({data['survival_rate_percent']}%).")
            
        if any_channel_survives:
            print("Conclusion Expérimentale : VALIDÉE ✅ (Aucune extinction simultanée)")
        else:
            print("Conclusion Expérimentale : ANOMALIE ❌ (Extinction totale détectée)")
            
        print(f"Temps de calcul : {round(execution_time, 3)} secondes.")
        
        return {
            "N": N,
            "channels_data": channel_results,
            "structural_safety_validated": any_channel_survives,
            "execution_time_seconds": round(execution_time, 3)
        }

# --- ZONE D'EXPÉRIMENTATION ---
if __name__ == "__main__":
    analyzer = MonfetteR30Analyzer()
    
    # Nouvelle liste acceptant autant de grands nombres pairs que vous le souhaitez
    liste_N = [
        10_000_012,
        10_000_024,
        10_000_050,
        50_000_000,
        100_000_018,
        500_000_002,
        1_000_000_008,
        1_000_000_024,
        2_000_000_014,
        5_000_000_030
    ]
    
    # Nombre maximal de couples à tester par canal (évite l'explosion du temps sur les milliards)
    taille_echantillon = 5000 
    
    print(f"Début de l'analyse groupée sur {len(liste_N)} nombres.")
    temps_global_start = time.time()
    
    for grand_N in liste_N:
        analyzer.analyze_extinction_risk(grand_N, sample_size=taille_echantillon)
        
    print("\n" + "="*50)
    print(f"Analyse globale terminée en {round(time.time() - temps_global_start, 3)} secondes.")
