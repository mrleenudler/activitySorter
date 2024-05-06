import pandas as pd
from collections import Counter
import random

df = pd.read_excel('testaktivitet.xlsx')
fulltNavn = df['Fullt navn'].tolist() # unique Identifier
klasse = df['Klasse'].tolist() # Class
larer = df['Mattelærer'].tolist() # Acting as wanted group
priority = df['Prioritet'] # Wishes are sorted by priority
friends = [] # Used to group friends together

prioritetHoy = [tuple(x) for x in df.itertuples(index=False, name=None) if x[3] == "Dette har jeg veldig lyst til"]
prioritetLav = [tuple(x) for x in df.itertuples(index=False, name=None) if x[3] == "Dette har jeg litt lyst til"]
print(prioritetHoy[0], type(prioritetHoy[0]), "\n\n")
# print(prioritetLav[0])

# Setter opp aktiviteter med maks antall deltagere:
fordeling = {"emel": [], "anne marie": [], "sveinung": [], "natasha": [], "elisabeth": [], "andreas": [], "unresolved": []}
fordelingMax = {"emel": 12, "anne marie": 30, "sveinung": 25, "natasha": 50, "elisabeth": 8, "andreas": 100, "unresolved": 1000000}

emelMax = 12
anneMarieMax = 30
sveinungMax = 25
natashaMax = 50
elisabethMax = 8
andreasMax = 100

# Tilfeldig trekning mellom elevønsker
# Elever med få ønsker må prioriteres
# Elever med bare ett "veldig lyst" ønske må prioriteres til "litt lyst"
# sorted() kan sortere etter flere variabler på en gang
# Sorterer elevene i grupper etter antall ønsker - DONE

# Count occurrences of each unique ID (assuming ID is at index 0 in your tuples)
count = Counter(x[0] for x in prioritetHoy) # [(name, count)]
#print(count)

# Creating a dict with students sorted by how many wishes they have
gruppert = {key: [] for key in range(1,11)}
# placing each activity-application(i.e. student name) in their respective wich counts
for student, wishes in count.items(): # trenger jeg lage 'gruppert' eller kan jeg bruke count.items() direkte? -> NEI
    gruppert[wishes].append(student)
# print(gruppert)
# print(gruppert.keys())
# print(gruppert.values()) #dict
#print(gruppert[1]) # TEST: printer alle elever med ett ønske.

#Making a random draw for each activity
# Gruppert viser bare hvor mange ønsker en elev har. Ønskene må hentes fra prioritetHøy

for wishes in range(1,11):
    random.shuffle(gruppert[wishes]) # Randomizes lists
    # Placing students with only one wish
    if wishes == 1:
        # gruppert[1] contains all students with only one wish
        for student in list(gruppert[1]): # type(gruppert) er dict, type(student) er str ; gruppert[1] er studentens navn
            for application in list(prioritetHoy):
                if student == application[0]:
                    #print(gruppert[wishes][student])
                    #print(student, "\n", application)
                    gruppert[wishes].remove(student)
                    if fordeling[application[2].lower].len() < 
                    fordeling[application[2].lower()].append(application)
                    prioritetHoy.remove(application) #redundant (bør løses for senere justeringer)
                    #del gruppert[wishes][student]
                    # Legg application til fordeling
                    # fjern student fra gruppert
                    # fjern application fra prioritetHøy
print(fordeling["emel"], "\n\n\n")
print(gruppert, "\n\n\n")
print(prioritetHoy[0], "\n\n\n")



# Hver elev skal få oppfylt 2-to ønsker. 
# Elevene med 1-2 ønsker, må få sine oppfylt først.
# Det må kontrolleres om elever med 3-4 ønsker har fått sine redusert
# Deretter må resten få oppfylt sitt første ønske
# Ny kontroll må gjennomføres for hver gruppe som blir full
# Til slutt må alle gjenværende elever få oppfylt sitt andre ønske, med prioritet til "Vil mye"
# Advarsel må skrives for hver elev som ikke får oppfylt 2 ønsker

#WARNING: Systemet kan games; ved å oppgi få ønsker, er det større sjanse for å få akkurat hva du ønsker deg.
# Hvis det blir fullt, kan elever settes opp på en tilfeldig aktivitet?

