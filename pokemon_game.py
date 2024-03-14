from rich.console import Console
from rich.table import Table

class Attaque:
    def __init__(self, nom, type_attaque, categorie, precision, puissance, pp):
        self.nom = nom
        self.type_attaque = type_attaque
        self.categorie = categorie
        self.precision = precision
        self.puissance = puissance
        self.pp = pp

    def afficher(self):
        return f"{self.nom} ({self.type_attaque}, {self.categorie}, PP: {self.pp})"

class Pokemon:
    def __init__(self, nom, prix, types, pv, niveau, attaque, attaque_speciale, defense, defense_speciale, vitesse, attaques):
        self.nom = nom
        self.prix = prix
        self.types = types
        self.pv = pv
        self.niveau = niveau
        self.attaque = attaque
        self.attaque_speciale = attaque_speciale
        self.defense = defense
        self.defense_speciale = defense_speciale
        self.vitesse = vitesse
        self.attaques = attaques

    def est_ko(self):
        return self.pv <= 0

    def ajouter_attaque(self, attaque):
        self.attaques.append(attaque)

    def attaquer(self, cible, attaque):
        if attaque.categorie == "Physique":
            degats = ((2 * self.niveau / 5 + 2) * attaque.puissance * (self.attaque / cible.defense) / 50 + 2) 
        elif attaque.categorie == "Spéciale":
            degats = ((2 * self.niveau / 5 + 2) * attaque.puissance * (self.attaque_speciale / cible.defense_speciale) / 50 + 2)
        else:
            degats = 0
        
        cible.pv -= degats
        
        print(f"{self.nom} utilise {attaque.nom}!")
        print(f"{attaque.nom} inflige {degats} points de dégâts à {cible.nom}!")
        print(f"{cible.nom} a maintenant {cible.pv} points de vie restants.")

        if cible.est_ko():
            print(f"{cible.nom} est mis K.O.!")


    def afficher_attaques(self):
        return [attaque.afficher() for attaque in self.attaques]

    def afficher(self):
        return f"{self.nom} (Niveau: {self.niveau}, PV: {self.pv}, Types: {', '.join(self.types)})"

class Joueur:
    def __init__(self, nom, argent):
        self.nom = nom
        self.manche_gagnee = 0
        self.argent = argent
        self.pokemons = []

    def ajouter_argent(self, montant):
        self.argent += montant
        
    def ajouter_manche_gagnee(self):
        self.manche_gagnee += 1
        
    def choisir_pokemon(self, pokemons_disponibles):
        console = Console()
        table = Table(title=f"{self.nom}, choisissez vos Pokémons:")
        table.add_column("Numéro", style="cyan")
        table.add_column("Nom", style="cyan")
        table.add_column("Types", style="cyan")
        table.add_column("PV", style="cyan")
        table.add_column("Niveau", style="cyan")
        table.add_column("Attaques", style="cyan")

        for i, pokemon in enumerate(pokemons_disponibles, 1):
            table.add_row(
                str(i),
                pokemon.nom,
                ', '.join(pokemon.types),
                str(pokemon.pv),
                str(pokemon.niveau),
                ', '.join(pokemon.afficher_attaques())
            )

        console.print(table)

        choix = input("Choisissez vos Pokémons (séparés par des virgules, ex: 1,2,3): ")
        choix_numeros = [int(num.strip()) - 1 for num in choix.split(',')]
        pokemons_choisis = [pokemons_disponibles[num] for num in choix_numeros]
        
        for pokemon in pokemons_choisis:
            self.ajouter_pokemon(pokemon)

    def ajouter_pokemon(self, pokemon):
        self.pokemons.append(pokemon)

    def choisir_attaque(self, pokemon):
        console = Console()
        while True:
            console.print(f"{self.nom}, choisissez une attaque pour {pokemon.nom}:")
            for i, attaque in enumerate(pokemon.attaques, 1):
                console.print(f"{i}. {attaque.nom}")

            choix = input("Choisissez une attaque (numéro): ")
            if choix.isdigit():
                choix = int(choix)
                if 1 <= choix <= len(pokemon.attaques):
                    return pokemon.attaques[choix - 1]
                else:
                    console.print("Numéro d'attaque invalide. Veuillez choisir un numéro valide.\n")
            else:
                console.print("Entrée invalide. Veuillez entrer un numéro valide.\n")


    def recuperer_pokemon(self, numero):
        return self.pokemons[numero - 1]

    def afficher_pokemons(self):
        return [pokemon.afficher() for pokemon in self.pokemons]

    def afficher(self):
        return f"{self.nom} (Manches gagnées: {self.manche_gagnee}, Argent: {self.argent})"


class Jeu:
    def __init__(self):
        self.joueurs = []


    def jouer(self):
        console = Console()
        nombre_manches = 3
        
        for i in range(2):
            nom_joueur = input(f"Joueur {i + 1}, entrez votre nom: ")
            argent_joueur = int(input(f"Joueur {i + 1}, vous avez 1000 Pokédollars. Combien d'argent voulez-vous dépenser pour vos Pokémons? "))
            
            joueur = Joueur(nom_joueur, argent_joueur)
            
            pokemons_disponibles = [
                        Pokemon("Pikachu", 200, ["Electrique"], 100, 10, 30, 35, 20, 25, 50, [
                            Attaque("Éclair", "Electrique", "Physique", 90, 40, 10),
                            Attaque("Charge", "Normal", "Physique", 100, 35, 15)
                        ]),
                        Pokemon("Bulbasaur", 180, ["Plante", "Poison"], 120, 12, 25, 30, 30, 35, 40, [
                            Attaque("Fouet Lianes", "Plante", "Physique", 95, 35, 15),
                            Attaque("Vampigraine", "Plante", "Spéciale", 90, 25, 20)
                        ]),
                        Pokemon("Charmander", 160, ["Feu"], 90, 8, 28, 30, 18, 25, 60, [
                            Attaque("Flamme", "Feu", "Spéciale", 85, 38, 10),
                            Attaque("Griffe", "Normal", "Physique", 95, 32, 15)
                        ]),
                        Pokemon("Squirtle", 170, ["Eau"], 110, 11, 25, 32, 28, 35, 45, [
                            Attaque("Pistolet à O", "Eau", "Spéciale", 90, 30, 15),
                            Attaque("Coup de Tête", "Normal", "Physique", 95, 33, 20)
                        ]),
                        Pokemon("Jigglypuff", 150, ["Fée", "Normal"], 80, 9, 22, 18, 25, 35, 20, [
                            Attaque("Charme", "Fée", "Spéciale", 80, 20, 15),
                            Attaque("Roulade", "Normal", "Physique", 100, 28, 20)
                        ]),
                        Pokemon("Geodude", 140, ["Roche", "Sol"], 120, 10, 28, 22, 40, 25, 10, [
                            Attaque("Jet-Pierres", "Roche", "Physique", 90, 38, 10),
                            Attaque("Charge", "Normal", "Physique", 100, 35, 15)
                        ]),
                        Pokemon("Abra", 130, ["Psy"], 60, 7, 15, 30, 10, 20, 90, [
                            Attaque("Choc Mental", "Psy", "Spéciale", 85, 22, 15),
                            Attaque("Reflet", "Normal", "Statut", 100, 0, 20)
                        ]),
                        Pokemon("Machop", 140, ["Combat"], 100, 11, 32, 25, 20, 18, 35, [
                            Attaque("Balayage", "Combat", "Physique", 90, 40, 10),
                            Attaque("Vive-Attaque", "Normal", "Physique", 100, 28, 15)
                        ]),
                        Pokemon("Gastly", 160, ["Spectre", "Poison"], 70, 9, 18, 25, 20, 20, 80, [
                            Attaque("Ombre Nocturne", "Spectre", "Spéciale", 85, 30, 10),
                            Attaque("Dévorêve", "Psy", "Spéciale", 90, 22, 15)
                        ]),
                        Pokemon("Eevee", 180, ["Normal"], 80, 10, 28, 25, 22, 25, 55, [
                            Attaque("Charge", "Normal", "Physique", 100, 35, 15),
                            Attaque("Morsure", "Normal", "Physique", 95, 32, 20)
                        ]),
                    ]
            
            joueur.choisir_pokemon(pokemons_disponibles)
            self.joueurs.append(joueur)

        scores = {joueur: 0 for joueur in self.joueurs}

        for manche in range(nombre_manches):
            console.print(f"\n--- Combat {manche + 1} ---\n")
            points_gagnes = self.combat(manche)
            for joueur, points in points_gagnes.items():
                scores[joueur] += points

        gagnant = max(scores, key=scores.get)
        console.print(f"\n--- Fin du jeu ---")
        console.print(f"Le vainqueur est {gagnant.nom} avec {scores[gagnant]} points!")

    def combat(self, manche):
        console = Console()
        points_gagnes = {joueur: 0 for joueur in self.joueurs}
        
        for joueur in self.joueurs:
            console.print(f"\n{joueur.nom}, c'est à toi!")

            pokemon_actif = joueur.recuperer_pokemon(manche + 1)
            console.print(f"Votre Pokémon actif est {pokemon_actif.nom}")

            adversaire = self.joueurs[1] if joueur == self.joueurs[0] else self.joueurs[0]
            adversaire_pokemon = adversaire.recuperer_pokemon(manche + 1)
            console.print(f"Votre adversaire est {adversaire.nom}, avec son Pokémon {adversaire_pokemon.nom}")

            while not pokemon_actif.est_ko() and not adversaire_pokemon.est_ko():
                attaque_choisie = joueur.choisir_attaque(pokemon_actif)
                pokemon_actif.attaquer(adversaire_pokemon, attaque_choisie)

                if adversaire_pokemon.est_ko():
                    console.print(f"{adversaire.nom}'s {adversaire_pokemon.nom} a été mis K.O.!")
                    points_gagnes[joueur] += 1

                    adversaire_pokemon = adversaire.recuperer_pokemon(manche + 1)
                    console.print(f"Votre adversaire envoie {adversaire_pokemon.nom}.")

                else:
                    attaque_choisie = adversaire.choisir_attaque(adversaire_pokemon)
                    adversaire_pokemon.attaquer(pokemon_actif, attaque_choisie)

                    if pokemon_actif.est_ko():
                        console.print(f"{joueur.nom}'s {pokemon_actif.nom} a été mis K.O.!")
                        adversaire_pokemon = adversaire.recuperer_pokemon(manche + 1)
                        console.print(f"Votre adversaire envoie {adversaire_pokemon.nom}.")

        console.print(f"\n--- Fin du combat ---")
        return points_gagnes

if __name__ == "__main__":
    jeu = Jeu()
    jeu.jouer()
