import pandas as pd
from collections import Counter
import random

# def __init__

# target Excelark bør være userInput
df = pd.read_excel('testaktivitet.xlsx')
fulltNavn = df['Fullt navn'].tolist() # unique Identifier
klasse = df['Klasse'].tolist() # Class
larer = df['Aktivitet'].tolist() # Acting as wanted group
priority = df['Prioritet'] # Wishes are sorted by priority
friends = [] # Used to group friends together

# Flere verdier kan være userInput -> GUI vurderes etter hvert
highPriorityString = "Dette har jeg veldig lyst til"
lowPriorityString = "Dette har jeg litt lyst til"
maxActivitiesPerStudent = 2 # Bør være userInput
# Bør hentes fra Excelark
maxApplicationsPerStudent = 10 # aka totalNumberOfActivities
allePaameldteElever = set(fulltNavn) # Kanskje heller set(df['Fullt navn'].tolist())

# All applications are sorted into groups according to priority (kan programmet endres til numerisk prioritet?)
# kanskje flytte Hoy og Lav til def gruppert
prioritetHoy = [tuple(x) for x in df.itertuples(index=False, name=None) if x[3] == highPriorityString]
prioritetLav = [tuple(x) for x in df.itertuples(index=False, name=None) if x[3] == lowPriorityString]
allApplications = [tuple(x) for x in df.itertuples(index=False, name=None)]
random.shuffle(allApplications) # Trenger å randomisere for rettferdig fordeling (riktig sted?)
#Removing redundant applications (midlertidig deaktivert for testing purposes.)
#allApplications = list(set(allApplications)) # NOT TESTED (reduserer antall applications til 140?)
# priority groups; built in group_student_applications() 
# Skal den kalles her?

gruppertHoy = [] # Er disse redundante?
gruppertLav = []
gruppertTotal = []

# DEBUG
# print(prioritetHoy[0], type(prioritetHoy[0]), "\n\n")
# print(prioritetLav[0])

# Setter opp aktiviteter med maks antall deltagere:
# NB! Bør hentes fra excel/dataframe 
fordeling = {"emel": [], "anne marie": [], "sveinung": [], "natasha": [], "elisabeth": [], "andreas": [], "unresolved": []}
# NB! Bør være userInput
fordelingMax = {"emel": 12, "anne marie": 30, "sveinung": 25, "natasha": 50, "elisabeth": 8, "andreas": 100, "unresolved": 1000000}
# Dict som holder oversikt over hvor mange aktiviteter en elev er meldt på. 
eleverMedBekreftedeAktiviteter = {elev: 0 for elev in allePaameldteElever}

# emelMax = 12 # Redundant -> slett
# anneMarieMax = 30
# sveinungMax = 25
# natashaMax = 50
# elisabethMax = 8
# andreasMax = 100

# skal allApplications sendes som input til funksjonen?
def remove_full_activities_from_applications():
    # Some activities will be full, and unavailable for further applications
    listOfFullActivities = [activity for activity in fordeling.keys() if len(fordeling[activity]) >= fordelingMax[activity]]
    # DEBUG
    print("Fully signed activities: ", listOfFullActivities)
    for activity in fordeling: # activity, signed_students, max_students 
        print(activity)
        print(len(fordeling[activity]), fordelingMax[activity])
    print("Lenght of allApplications after removal of first group: ", len(allApplications)) 
    # print(allApplications[1][2])
    # # VIKTIG Å SLETTE
    # if allApplications[1][2].lower() in listOfFullActivities:
    #     print("True")
    # allApplications.remove(allApplications[1]) #virker
    # print(allApplications[1][2])
    # CODE
    # Creating set of remaining students in allApplications
    remainingStudents = set([tup[0] for tup in allApplications]) # LAmbda function?
    # DEBUG
    print("Number of remaining students, expected < 20: ", len(remainingStudents)) # actual: 54
    # print(remainingStudents)
    #print("Remaining applications\n", allApplications)
    # CODE 
    # Removing applications for fully signed activities
    for application in list(allApplications): # List preventing trouble with mutation while running
        if application[2].lower() in listOfFullActivities:
            allApplications.remove(application) #Funker 
    # DEBUG
    print("Length of allApplications after clean: ", len(allApplications))
    # CODE
    newRemainingStudents = set([tup[0] for tup in allApplications])
    # DEBUG
    print("List of remaning students, cleaned for unapplicable applications: ", newRemainingStudents)
    print("Length of 'unresolved' group before clean: ", len(fordeling["unresolved"]))
    # CODE
    # Students which now have no applications left, are moved to "unresolved" group
    for name in remainingStudents:
        if name not in newRemainingStudents:
            # Students that now have all 
            fordeling['unresolved'].append(name)
            # Removing unresolved students form list of students (corresponding applications, are they removed?)
            allePaameldteElever.remove(name) 
            # DEBUG (funker)
            # print("Removed ", name)
            #     print(allePaameldteElever[name])
            # except:
            #     print("Successful")
    print("Length of 'unresolved' group after clean: ", len(fordeling["unresolved"]))
    # WARNING! Elever kan fjernes helt uten å havne i 'unresolved'
    # Når den virker, gå tilbake til logikken for 2 ønsker


# Elever med bare ett "veldig lyst" ønske må prioriteres til "litt lyst"
# sorted() kan sortere etter flere variabler på en gang
# Sorterer elevene i grupper etter antall ønsker - DONE

def count_applications(applications):
    # tar inn tuples fra prioritetHoy/Lav
    groups = {key: [] for key in range(1, maxApplicationsPerStudent)} # 0 applications should not be possible
    counter = Counter(app[0] for app in applications)
    for student, wishes in counter.items():
        groups[wishes].append(student)
    return groups



def group_student_applications(priorityString):
    # bruke allApplications til å lage prioritetHoy/prioritetLav
    prioritetHoy = [tuple for tuple in allApplications if tuple[3] == highPriorityString] # fjernes
    prioritetLav = [tuple for tuple in allApplications if tuple[3] == lowPriorityString] # fjernes
    if priorityString:
        prioritet = [tuple for tuple in allApplications if tuple[3] == priorityString]
    else: 
        prioritet = [tuple for tuple in allApplications]
    # countHigh = Counter(application[0] for application in prioritetHoy)
    # countLow = Counter(application[0] for application in prioritetLav)
    # countTotal = Counter(application[0] for application in allApplications)
    gruppertHoy = count_applications(prioritetHoy) # fjernes
    gruppertLav = count_applications(prioritetLav) # fjernes
    gruppertTotal = count_applications(allApplications) # fjernes
    gruppert = count_applications(prioritet)
    return gruppert

def place_student(studentName):
# fordeling = {"emel": [], "anne marie": [], "sveinung": [], "natasha": [], "elisabeth": [], "andreas": [], "unresolved": []}
# fordelingMax = {"emel": 12, "anne marie": 30, "sveinung": 25, "natasha": 50, "elisabeth": 8, "andreas": 100, "unresolved": 1000000}
# eleverMedBekreftedeAktiviteter = {elev: 0 for elev in allePaameldteElever}
    # If student is assigned to max number of activities
    if eleverMedBekreftedeAktiviteter[studentName] >= maxActivitiesPerStudent:
        allePaameldteElever.remove(studentName)
        return
    #currentApplication = None
    for application in allApplications:
        if application[0] == studentName:
            # Removing application and keep searching if activity is full
            # Skal ikke forekomme for numberOfApplications <= maxActivitiesPerStudent
                # Men bør være relevant når numberOfApplications > maxActivitiesPerStudent
            if fordelingMax(application[2]) == len(fordeling(application[2])):
                allApplications.remove(application)
                continue # Sjekk at continue funker som forutsatt. 
            #currentApplication = application
            allApplications.remove(application)
            fordeling[application[2]].append(studentName)
            eleverMedBekreftedeAktiviteter[studentName] += 1
            return
    
            # for group_key in gruppertTotal: #(redundant?)
            #     # redundant?
            #     if student in gruppertTotal[group_key]:
            #         pass
            #         #gruppertTotal[group_key].remove(student)
            #         # VIKTIG! 
            #         # skal eleven fjernes fra gruppen, 
            #         # eller skal eleven bumpes ned, 
            #         # eller skal ingenting gjøres, og gruppene gjenopprettes etter hver iterasjon av gruppertTotal i hovedmetoden?

                # if student in group:
                #     group.remove(student) 
                # for student in group:
                #     if student == studentName:
                #         group.remove(studentName)

    # place in fordeling (pull info from allApplications)
    # add to eleverMedBekreftedeAktiviteter
    # # remove from groups ?redundant?



gruppertHoy = group_student_applications(highPriorityString) # Tenk på hva jeg skal gjøre med denne
gruppertLav = group_student_applications(lowPriorityString)
gruppertTotal = group_student_applications("")
# Creating list of students with no high-priority applications
    # Blir denne redundant med gruppertAll / allApplications ??
# List of all students. Useed to sort out students with no high-priority wishes, and if possible, bump up a low priority wish
# Identifying students without any wishes (REDO LOGIC)
noWishList = list(allePaameldteElever)
for elev in allePaameldteElever:
    for wishes in range(1,11): # max range bør hentes fra Excelark
        try:
            if elev in gruppertHoy[wishes]:
                noWishList.remove(elev) # funker, elever som ikke har noen høy-prioritet ønsker blir igjen i listen
        except:
            pass
#            print("Out of range error: ", wishes)
# Moving students without high-priority wishes, and only one low priority wish to high-priority list
    # Kan denne generaliseres? Kanskje som en function? Ta inn wishes som argument?
for elev in list(noWishList):
    if elev in gruppertLav[1]: 
        # Bumping students from low to high priority, if no high-priority wish exists
        gruppertHoy[1].append(elev)
        gruppertLav[1].remove(elev)
        # noWishList now contains students with no wishes at all, yet still in the database (i.e. no priority selection allowed in form)
        noWishList.remove(elev) # ser ut til å funke
        #print(f"elev {elev} flyttes")
# print(noWishList) # TEST - to elever på lista har erken høy- eller lav-prioritets ønsker (skal ikke forekomme(?) i ferdig produkt)
#print("\n\n", gruppertLav[1])
# NB: Dette skjer før fordelingen





#Making a random draw for each activity
# Gruppert viser bare hvor mange ønsker en elev har. Ønskene må hentes fra prioritetHøy

# Students without high-priority wishes are collected from low-priority -> redundant?
# lage function av denne? Integrere i def counter?
# NOT IMPLEMENTED
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


# CODE (redundant?)
random.shuffle(prioritetHoy) # Shuffling the applications for fair draw (necessary?)
random.shuffle(prioritetLav)

# DEBUG
counter = 0 
for application in allApplications: # Counting totalApplications -> OK (407)
    counter += 1
print("Total applications: ", counter)
counter = 0
for applications in gruppertTotal: # counting totalApplication from gruppertTotal -> OK
    #print(len(gruppertTotal[applications]))
    counter += applications * len(gruppertTotal[applications])
print("Total applications from gruppertTotal: ", counter)
counter = 0
for application in allApplications: # student is of type tuple
    for name in gruppertTotal[1]:
        if name == application[0]:
            counter +=1
print("Counting students with 1 application. Expected: 245: ", counter)

# CODE 
# Lages til en metode der elever med få plasseringer / få ønsker prioriteres

# CODE
# Grouping students by number of applications
gruppertHoy = group_student_applications(highPriorityString) # Tenk på hva jeg skal gjøre med denne
gruppertLav = group_student_applications(lowPriorityString)
gruppertTotal = group_student_applications("")

# WANT: assigning students with minimum flexibility, recalculating applications and rerun
# while allApplications:
    # Minimum flexibility group is distributed (1 application each)
        # Remember to account for already distributed activities
    # Clean applications for full activities
    # Recalculate groups of students according to applications
applicationCounter = 1
debugExitCounter = 0
while allApplications: # trenger continue(?)
    if debugExitCounter > 5:
        break
    debugExitCounter += 1
    # todelt kode; if applications < maxActivities; else: priorityActivities
    # First checking students with numberOfApplications <= maxActivitiesPerStudent 
    # DONE Kanskje gruppene skal justeres med assigned før gjennomgang?
    print("\n\nBumping up application group according to assigned activities\n\n")
    # Kan denne for eksempel heller være en "generator expression?"
    # Bumping up application group according to number of assigned activities
    studentsWithAssignedActivities = [student for student in eleverMedBekreftedeAktiviteter if eleverMedBekreftedeAktiviteter[student] > 0]
    for studentName in studentsWithAssignedActivities:
        for group in gruppertTotal:
            if studentName in gruppertTotal[group]:
                gruppertTotal[group].remove(studentName)
                gruppertTotal[group + studentsWithAssignedActivities[studentName]].append(studentName)
                print(studentName, "Bumped from", group, "to", group + studentsWithAssignedActivities[studentName])

    # While there are still students to assign that have applications <= maxActivities
    # Students must be removed from group when fully assigned
    print("\n\nAssigning students to activities\n\n")
    exitCounter2 = 0
    gruppertKeys = [number for number in range(1, maxActivitiesPerStudent + 1)]
    print("GruppertKeys: ", gruppertKeys)
    while not all(len(gruppertTotal[group]) == 0 for group in gruppertKeys): # "group in gruppertTotal and" kan legges til for mer robust kode (hindrer KeyError)
        # DEBUG
        # Tenk ut en rettferdig algoritme
            # Skal det kalles en plasseringsmetode? metode(elev, numberOfApplications)
            # Elever med én application plasseres først, deretter oppdateres listen og gjentas til alle er plassert
            # Nå gjentar jeg overordnet logikk
        listOfStudentsWithFewApplications = [gruppertTotal[gruppe] for gruppe in gruppertKeys] # printer elevnavn list-of-lists med index == numberOfApplications
        print("Debug liste: ", len(listOfStudentsWithFewApplications)) # maxActivitiesPerStudent antall lister med elever
        if exitCounter2 == 2:
            break
        exitCounter2 += 1
        # CODE
        # debugList har nå alle elevene med 1 og 2 applications. 
        # de kan plasseres i fordelt
        while listOfStudentsWithFewApplications:
            listIndex = 0
            for i in range(1, len(listOfStudentsWithFewApplications) + 1):
                if listOfStudentsWithFewApplications[i]:
                    listIndex = i
            for student in listOfStudentsWithFewApplications[i]:
                place_student(student)
            # Kontroller at listen regenereres korrekt, spesielt at gruppertTotal[] er oppdatert, og at gruppertKeys er korrekt
            listOfStudentsWithFewApplications = [gruppertTotal[gruppe] for gruppe in gruppertKeys]
            clean_applications()
            recreate_groups() # Skal bare inneholde elever som ikke er ferdig plassert.

        # Er følgende kode redundant?

        # Legg til assigned applications også
            # -> Når elever er fully assigned, fjernes de fra applications
            # -> Hva med elever som er partly assigned, men har flere applications?
            # Lage liste fra assigned for å prioritere elevene?
        # Må være avhengig av eleverMedBekreftedeAktiviteter[maxActivities]
        # skal jeg iterere gjennom gruppene her?
        # Eller lage liste med unassigned elever? begge? 
        for i in range(1, maxApplicationsPerStudent): # maxActivities??
            # prøv å kjøre uten list() også
            # prøver å lage en midlertidig liste av applications fra allApplications
            
            # Bør jeg gjøre gruppertX til dict-list-of-tuples? Kan det bli problemer med likhetssjekk?
            for j in range(1,i): # selecting one student at a time for activity placement, to make it fair
                pass # Need to find correct application/activity
            for student in list(gruppertTotal[i]): # NB LÅSER SEG / STOPPER ALDRI
                # Siden vi jobber med gruppertTotal[ < max], må jeg plassere alle elevene
                # dvs. vi starter med elevene med høy prioritet.
                #print("Prøver å skrive ut neste forekomst av elev med høyPri i gruppe [i]", next(tup[0] for tup in allApplications if tup[3] == highPriorityString))
                print("Prøver å skrive ut neste forekomst av elev med høyPri i gruppe [i]", i, student)
                # Hvordan finner jeg korrekt application? indexof?
                for j in range(1,i):
                    pass
                    # placing student in all desired activities
                        # NOT FAIR, one activity at a time is fair
                gruppertTotal[i].remove(student) # Hvis i > 1, skal ikke eleven fjernes før alle aktiviteter er oppfylt
                # remove application from allApplications (Kan også gjøres i CLEAN-prosedyren?)
                    # -> Risikerer jeg multiple oppføringer av samme application?
                if eleverMedBekreftedeAktiviteter[student] >= maxActivitiesPerStudent:
                    # append student to 'fordelt'
                    eleverMedBekreftedeAktiviteter[student] += 1
                #if student in prioritetHoy[i] # Unødig knotete å traversere denne? (Ikke ment å oppdateres?)
        # CLEAN ALLaPPLICATIONS FOR FULL GROUPS AND RERUN/CONTINUE
        for student in gruppertTotal[1]:
            pass
            # 1. pri er studenter som ikke har aktiviteter, 

    for applicationCounter in range(1, maxApplicationsPerStudent):
        if gruppertTotal == applicationCounter:
            # Skal jeg søke i prioritetHoy? Eller traversere gruppertHoy?
                # Kanskje prioritetHoy hvis applications > max? 
            # If allApplications > 2
            pass
print("DEBUG EXIT_COUNTER: ", debugExitCounter)

# # Randomizing name lists for fair draw
# for i in range(1, maxApplicationsPerStudent):
#     random.shuffle(gruppertTotal[i])
# # Students with 1 application assigned to activity
# for application in list(allApplications): # student is of type tuple | list() to avoid mutating while handling (?)
#     # Iterating through students with only one application
#     for name in gruppertTotal[1]:
#         if name == application[0]:
#             counter +=1
#             for activity in fordeling:
#                 if activity == application[2].lower():
#                     # Checking if activity is full, and if so, placing application in 'unresolved'
#                     if len(fordeling[activity]) < fordelingMax[activity]:
#                         # Assigning names to activity group
#                         fordeling[activity].append(name)
#                         # Increasing student activity count
#                         eleverMedBekreftedeAktiviteter[name] += 1
#                         # removing placed applications
#                         allApplications.remove(application)
#                     else:
#                         # Pass på at ingen som har flere alternativer blir plassert her
#                         # Gjelder kanskje bare elever med ett valg?
#                         fordeling["unresolved"].append(name)
#                         # Next line: disabled because no activity is assigned.
#                         # eleverMedBekreftedeAktiviteter[name] += 1
#                         # Application must be removed, even if the activity is full
#                         allApplications.remove(application) 
# #Iterating through students with two applications (nummber of total applications have been reduced)
# print("Going to remove_applications")
# remove_full_activities_from_applications()
# print("Returning from remove_applications")
# for application in allApplications: 
#     for name in gruppertTotal[2]:
#         # DENNE SKAL FJERNES TIL FORDEL FOR BEDRE LOGIKK MED RE-BEREGNING AV GRUPPENE
#         # fortsett her med å trekke aktiviteter for elever med 2 ønsker
#         # Sjekk for elever om har mistet ett av ønskene sine. 
#         # Legg inn funksjon for å rydde bort aktiviteter som er fulle, 
#             # Eventuelt nedjustere antall ønsker elevene har.
#         # Kanskje dumt å fortsette å iterere gjennom applications. Den er blitt redusert
#         pass
        


#DEBUG
counter = 0
for elev in eleverMedBekreftedeAktiviteter:
    counter += eleverMedBekreftedeAktiviteter[elev]
print("eleverMedBekreftedeAktiviteter, expected 245/407(139/???) minus unresolved: ", counter)
counter = 0
for application in allApplications:
    counter +=1
print("Expected applications after 1st pass 407-245=162 ", counter)



# for navn in gruppertTotal[1]:
#     print(navn)

# for application in allApplications:
#     #print(application[0]) Printer navn til alle applications
#     if application[0] in gruppertTotal[1]:
#         print(application) #NEI!  Printer alle elever med 1 application/ønske
#         # flere applications med samme navn -> flere oppføringer (skulle ikek skje)


# while maxApplicationsPerStudent > 0: #  macApplicationsPerStudent == 10
#     # gruppertLav og gruppertHoy erstattes mest sannsynlig av prioritetLav og prioritetHoy
#     # random.shuffle(gruppertLav[1]) # Randomizes lists
#     # random.shuffle(gruppertHoy[1]) # Randomizes lists
#     random.shuffle(gruppertTotal[1]) # Randomizes currents list
#     # Moves all students 1 down in number of applications -> Is this what I want?
#     # I want to select a random student and place in activityGroup, then reduce number of applications for this student
#     # Students with 1-2 applications go first
#     for student in list(gruppertTotal[1]): #type string - bør den være list(gruppertTotal[1]) ??
#         # gruppertTotal[1].pop(gruppertTotal[1].index(student)) #Removes student from group with 1 application/wish
#         gruppertTotal[1].remove(student) #Bedre enn pop
#         if eleverMedBekreftedeAktiviteter[student] <= maxActivitiesPerStudent: # Irrelevant for 1-2 applications
#             # all True print(eleverMedBekreftedeAktiviteter[student] <= maxActivitiesPerStudent)

#             for activity in fordeling:
#                 if len(fordeling[activity]) <= fordelingMax[activity] and activity == allApplications.index():
#                     fordeling[activity].append(student)
#                     counter += 1
#                     eleverMedBekreftedeAktiviteter[student] += 1
#                     #print(activity, student)
#                     # print(allApplications[0].index(student)) # Gir denne riktig treff?
#             print(eleverMedBekreftedeAktiviteter[student])
#         else: 
#             print("\n\nALL WISHES FULFILLED")
#     maxApplicationsPerStudent -= 1

# DEBUG
# for elev in eleverMedBekreftedeAktiviteter:
#     print(elev, eleverMedBekreftedeAktiviteter[elev])

# DEBUG
counter = 0
print("counting all activities assigned, including 'unassigned' ")
for activity in fordeling:
#     for elev in fordeling[activity]:
#         print(elev, activity)
    print(activity, len(fordeling[activity]))
    counter += len(fordeling[activity])
print(counter) 
print("Remaining applications (if any): \n", allApplications[0])
#print(fordeling)
    # for i in range(0, maxApplicationsPerStudent):
    #     #print("\n", i , "\n")
    #     for student in list(gruppertTotal[i]): #list() nødvendig eller unødvendig?
    #         # student in gruppertTotal må endre indeks.
    #         # En application må også plasseres i aktivitetsgruppe 
    #         #print(student, len(gruppertTotal[i]))
    #         if i > 1:
    #             gruppertTotal[i-1].append(student)
    #         counter += 1
    # maxApplicationsPerStudent -= 1

#print(counter) #DEBUG - teller studenter, ikke applications

# # Erstattes av while
# for wishes in range(1,maxApplicationsPerStudent): # Egen løkke for applications <= maxActivitiesPrStudent ? 
#     random.shuffle(gruppertLav[wishes]) # Randomizes lists
#     random.shuffle(gruppertHoy[wishes]) # Randomizes lists
#     random.shuffle(gruppertTotal[wishes]) # Randomizes lists
#     # Placing students with only one wish
#     if wishes == 1:
#         # gruppertTotal[1] contains all students with only one wish in total
#         for student in list(gruppertHoy[1]): # type(gruppertHoy) er dict, type(student) er str ; gruppertHoy[1] er studentens navn
#             #for application in list(prioritetHoy):
#             for application in list(allApplications):
#                 if student == application[0]:
#                     #print(gruppertHoy[wishes][student])
#                     #print(student, "\n", application)
#                 #gruppertHoy[wishes].remove(student)
#                     gruppertTotal[wishes].remove(student) # NB! vil fjerne alle ønskene til en elev på én gang!!! (ikke bra, må fjerne bare relevant ønske)
#                     # NB student må fjernes fra respektiv prioritet Høy/Lav gruppe også
#                     #print("\t TEST", type(prioritetHoy.index(application)))
#                     #print("\t", application[2].lower()) #ønsket aktivitet
#                     #print(len(fordeling[application[2].lower()])) # 
#                     #print("\t TEST: ", len(fordeling[application[2].lower()]), fordelingMax[application[2]])

#                     # Move application into activity group, if not full
#                     if len(fordeling[application[2].lower()]) < fordelingMax[application[2].lower()]:
#                         fordeling[application[2].lower()].append(application)
#                     else:
#                         # If desired group is full
#                         fordeling["unresolved"].append(application)
#                     prioritetHoy.remove(application) #redundant (bør løses for senere justeringer)
#                     #del gruppertHoy[wishes][student]
#                     # Legg application til fordeling
#                     # fjern student fra gruppertHoy
#                     # fjern application fra prioritetHøy

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

