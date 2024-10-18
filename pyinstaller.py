import subprocess
commande = 'PyInstaller --onefile --windowed '
fichier_principal = str(input("Fichier principal :"))
nb_fichier_supplementaire = int(input("nb fichiers élémentaires :"))
fichiers_supplementaires = str(input("fichiers supplémentaires : "))
list_fichiers_supplementaires = list()
while nb_fichier_supplementaire!=len(fichiers_supplementaires.split(", ")):
    fichiers_supplementaires = str(input("fichiers supplémentaires : "))
list_fichiers_supplementaires = fichiers_supplementaires.split(", ")
i = 0
for fic_sup in list_fichiers_supplementaires:
    commande += f"--add-data \"{fic_sup};.\" "
commande +=fichier_principal
#print(commande)
subprocess.run(commande,shell=True)
