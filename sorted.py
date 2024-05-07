import pandas as pd
from collections import Counter
import random

df = pd.read_excel('testaktivitet.xlsx')
fulltNavn = df['Fullt navn'].tolist() # unique Identifier
klasse = df['Klasse'].tolist() # Class
larer = df['Aktivitet'].tolist() # Acting as wanted group
priority = df['Prioritet'] # Wishes are sorted by priority
friends = [] # Used to group friends together

maxActivitiesPerStudent = 2
allePaameldteElever = set(fulltNavn)
# All applications are sorted into groups according to priority (kan programmet endres til numerisk prioritet?)
prioritetHoy = [tuple(x) for x in df.itertuples(index=False, name=None) if x[3] == "Dette har jeg veldig lyst til"]
prioritetLav = [tuple(x) for x in df.itertuples(index=False, name=None) if x[3] == "Dette har jeg litt lyst til"]
# print(prioritetHoy[0], type(prioritetHoy[0]), "\n\n")
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

# May want this as a function
# Count occurrences of each unique ID (assuming ID is at index 0 in your tuples)
countHoy = Counter(x[0] for x in prioritetHoy) # [(name, count)]
# Creating a dict with students sorted by how many wishes they have (High priority)
gruppertHoy = {key: [] for key in range(0,11)}
# placing each activity-application(i.e. student name) in their respective wich counts
for student, wishes in countHoy.items(): # trenger jeg lage 'gruppertHoy' eller kan jeg bruke count.items() direkte? -> NEI
    gruppertHoy[wishes].append(student)
# repeating for low priority
countLav = Counter(x[0] for x in prioritetLav) # [(name, count)]
gruppertLav = {key: [] for key in range(0,11)}
for student, wishes in countLav.items():
    gruppertLav[wishes].append(student)
# print(gruppertHoy[3])
# print(gruppertLav[3])
# print(gruppertHoy.keys())
# print(gruppertHoy.values()) #dict
#print(gruppertHoy[1]) # TEST: printer alle elever med ett ønske.

noWishList = list(allePaameldteElever)

# Creating list of students with no high-priority applications
for elev in allePaameldteElever:
    for wishes in range(1,11):
        if elev in gruppertHoy[wishes]:
            noWishList.remove(elev) # funker, elever som ikke har noen høy-prioritet ønsker blir igjen i listen
# Moving students without high-priority wishes, and only one low priority wish to high-priority list
# Kan denne generaliseres? Kanskje som en function? Ta inn wishes som argument?
for elev in list(noWishList):
    if elev in gruppertLav[1]:
        gruppertHoy[1].append(elev)
        gruppertLav[1].remove(elev)
        noWishList.remove(elev) # ser ut til å funke
        #print(f"elev {elev} flyttes")
#print(noWishList)
#print("\n\n", gruppertLav[1])
# NB: Dette skjer før fordelingen





#Making a random draw for each activity
# Gruppert viser bare hvor mange ønsker en elev har. Ønskene må hentes fra prioritetHøy

# Students without high-priority wishes are collected from low-priority
# lage function av denne?
for elev in allePaameldteElever:
    #elev må sjekkes mot hele prioritetHøy eller gruppertHøy
    for application in prioritetHoy:
        if elev == application[0]:
            pass
    for navn in prioritetHoy:
        if elev in navn[0] and elev in gruppertHoy[1]:
            pass
            #print("\t", elev)
                
        # elev ikke i prioritetHøy/gruppertHøy
    for navn in prioritetLav:
        if elev in navn[0] and elev in gruppertLav[1]:
            pass
            #print(elev)


for wishes in range(1,11):
    random.shuffle(gruppertLav[wishes]) # Randomizes lists
    random.shuffle(gruppertHoy[wishes]) # Randomizes lists
    # Placing students with only one wish
    if wishes == 1:
        # gruppertHoy[1] contains all students with only one high-priority wish
        for student in list(gruppertHoy[1]): # type(gruppertHoy) er dict, type(student) er str ; gruppertHoy[1] er studentens navn
            for application in list(prioritetHoy):
                if student == application[0]:
                    #print(gruppertHoy[wishes][student])
                    #print(student, "\n", application)
                    gruppertHoy[wishes].remove(student)
                    #print("\t TEST", type(prioritetHoy.index(application)))
                    #print("\t", application[2].lower()) #ønsket aktivitet
                    #print(len(fordeling[application[2].lower()])) # 
                    #print("\t TEST: ", len(fordeling[application[2].lower()]), fordelingMax[application[2]])
                    # Move application into activity group, if not full
                    if len(fordeling[application[2].lower()]) < fordelingMax[application[2].lower()]:
                        fordeling[application[2].lower()].append(application)
                    else:
                        # If desired group is full
                        fordeling["unresolved"].append(application)
                    prioritetHoy.remove(application) #redundant (bør løses for senere justeringer)
                    #del gruppertHoy[wishes][student]
                    # Legg application til fordeling
                    # fjern student fra gruppertHoy
                    # fjern application fra prioritetHøy

# print(fordeling["emel"], "\n\n\n")
# print(gruppertHoy, "\n\n\n")
# print(prioritetHoy[0], "\n\n\n")




# Hver elev skal få oppfylt 2-to ønsker. 
# Elevene med 1-2 ønsker, må få sine oppfylt først.
# Det må kontrolleres om elever med 3-4 ønsker har fått sine redusert
# Deretter må resten få oppfylt sitt første ønske
# Ny kontroll må gjennomføres for hver gruppe som blir full
# Til slutt må alle gjenværende elever få oppfylt sitt andre ønske, med prioritet til "Vil mye"
# Advarsel må skrives for hver elev som ikke får oppfylt 2 ønsker

#WARNING: Systemet kan games; ved å oppgi få ønsker, er det større sjanse for å få akkurat hva du ønsker deg.
# Hvis det blir fullt, kan elever settes opp på en tilfeldig aktivitet?

