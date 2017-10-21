# 6.00 Problem Set 12
#
# Name:
# Collaborators:
# Time:

import numpy
import random
import pylab

class NoChildException(Exception):
    pass

def random_event(probability):
    return True if random.random() <= probability else False

class SimpleVirus(object):
    def __init__(self, maxBirthProb, clearProb):
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def doesClear(self):
        return random_event(self.clearProb)

    def reproduce(self, popDensity):
        if random_event(self.maxBirthProb * (1 - popDensity)):
            return SimpleVirus(self.maxBirthProb, self.clearProb)

        raise NoChildException()

class SimplePatient(object):
    def __init__(self, viruses, maxPop):
        self.viruses = viruses
        self.maxPop = maxPop
        self.totalPop = 0
        self.popDensity = 0

    def getTotalPop(self):
        return self.totalPop

    def update(self):
        self.viruses = [v for v in self.viruses if not v.doesClear()]
        self.popDensity = len(self.viruses) / self.maxPop
        for v in self.viruses:
            try:
                self.viruses.append(v.reproduce(self.popDensity))
            except:
                pass

        self.totalPop = len(self.viruses)
        return self.totalPop

def problem2():
    start = 100
    viruses = [SimpleVirus(0.1, 0.05)] * start
    patient = SimplePatient(viruses, 1000)
    stats = [start]
    for i in range(300):
        stats.append(patient.update())
    pylab.title('Simple virus for simple patient')
    pylab.ylabel('Number of viruses')
    pylab.xlabel('Timesteps')
    pylab.plot(stats)
    pylab.show()

class ResistantVirus(SimpleVirus):
    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb

    def getResistance(self, drug):
        return False if drug not in self.resistances else self.resistances[drug]

    def isResistantTo(self, drugs):
        return all([self.getResistance(d) for d in drugs])

    def mutates(self, resistance):
        if resistance in self.resistances and self.resistances[resistance]:
            return random_event(1 - self.mutProb)

        return random_event(self.mutProb)

    def mutateResistances(self, activeDrugs):
        return {r:self.mutates(r) for r in self.resistances.keys()}

    def reproduce(self, popDensity, activeDrugs):
        nonResistantTo = [d for d in activeDrugs if not self.getResistance(d)]
        if len(nonResistantTo) > 0:
            raise NoChildException()

        if random_event(self.maxBirthProb * (1 - popDensity)):
            return ResistantVirus(self.maxBirthProb, self.clearProb, self.mutateResistances(activeDrugs), self.mutProb)

        raise NoChildException()

class Patient(SimplePatient):
    def __init__(self, viruses, maxPop):
        SimplePatient.__init__(self, viruses, maxPop)
        self.prescriptions = []

    def addPrescription(self, newDrug):
        if newDrug not in self.prescriptions:
            self.prescriptions.append(newDrug)

    def getPrescriptions(self):
        return self.prescriptions

    def getResistPop(self, drugResist):
        return len([v for v in self.viruses if v.isResistantTo(drugResist)])

    def update(self):
        self.viruses = [v for v in self.viruses if not v.doesClear()]
        self.popDensity = len(self.viruses) / self.maxPop
        for v in self.viruses:
            try:
                self.viruses.append(v.reproduce(self.popDensity, self.prescriptions))
            except:
                pass

        self.totalPop = len(self.viruses)
        return self.totalPop

def simulation(delay_in_treatment):
    drug = 'guttagonol'
    viruses = [ResistantVirus(0.1, 0.05, {'guttagonol':False, 'grimpex':False}, 0.005)] * 100
    patient = Patient(viruses, 1000)
    totalViruses = []
    drugResistViruses = []
    for _ in range(delay_in_treatment):
        totalViruses.append(patient.update())
        drugResistViruses.append(patient.getResistPop([drug]))
    patient.addPrescription(drug)
    for _ in range(150):
        totalViruses.append(patient.update())
        drugResistViruses.append(patient.getResistPop([drug]))
    return [totalViruses, drugResistViruses]

def problem4():
    totalViruses, drugResistViruses = simulation(150)
    pylab.title('Resistant virus patient treatment with 150 delay')
    pylab.ylabel('Number of viruses')
    pylab.xlabel('Timesteps')
    pylab.plot(totalViruses)
    pylab.plot(drugResistViruses)
    pylab.show()

def plot_simulation(delay_in_treatment):
    totalViruses, _ = simulation(delay_in_treatment)
    pylab.plot(totalViruses, label='{0} delay'.format(delay_in_treatment))

def plot_histogram(delay_in_treatment):
    stats = []
    for _ in range(30):
        totalViruses, _ = simulation(delay_in_treatment)
        stats.append(totalViruses[-1])
    pylab.title('Resistant virus patient treatment')
    pylab.ylabel('Patients')
    pylab.xlabel('Viruses')
    pylab.hist(stats, label='{0} delay'.format(delay_in_treatment))
    pylab.legend(loc=1)

def problem5():
    pylab.title('Resistant virus patient treatment')
    pylab.ylabel('Viruses')
    pylab.xlabel('Timesteps')
    plot_simulation(300)
    plot_simulation(150)
    plot_simulation(75)
    plot_simulation(0)
    pylab.legend(loc=1)

    pylab.figure()
    plot_histogram(300)
    pylab.figure()
    plot_histogram(150)
    pylab.figure()
    plot_histogram(75)
    pylab.figure()
    plot_histogram(0)

    pylab.show()

def plot_histogram_two_drugs(delay_in_treatment):
    stats = []
    for _ in range(30):
        viruses = [ResistantVirus(0.1, 0.05, {'guttagonol':False, 'grimpex':False}, 0.005)] * 100
        patient = Patient(viruses, 1000)
        for _ in range(150):
            patient.update()
        patient.addPrescription('guttagonol')
        for _ in range(delay_in_treatment):
            patient.update()
        patient.addPrescription('grimpex')
        for _ in range(150):
            patient.update()
        stats.append(patient.getTotalPop())

    pylab.title('Resistant virus patient treatment two drugs')
    pylab.ylabel('Patients')
    pylab.xlabel('Viruses')
    pylab.hist(stats, label='{0} delay'.format(delay_in_treatment))
    pylab.legend(loc=1)

def problem6():
    plot_histogram_two_drugs(300)
    pylab.figure()
    plot_histogram_two_drugs(150)
    pylab.figure()
    plot_histogram_two_drugs(75)
    pylab.figure()
    plot_histogram_two_drugs(0)
    pylab.show()

def plot_two_drugs_with_delay():
    total = []
    guttagonol =  []
    grimpex = []
    both = []
    viruses = [ResistantVirus(0.1, 0.05, {'guttagonol':False, 'grimpex': False}, 0.005)] * 100
    patient = Patient(viruses, 1000)

    for _ in range(150):
        patient.update()
        total.append(patient.getTotalPop())
        guttagonol.append(patient.getResistPop(['guttagonol']))
        grimpex.append(patient.getResistPop(['grimpex']))
        both.append(patient.getResistPop(['guttagonol', 'grimpex']))
    patient.addPrescription('guttagonol')
    for _ in range(300):
        patient.update()
        total.append(patient.getTotalPop())
        guttagonol.append(patient.getResistPop(['guttagonol']))
        grimpex.append(patient.getResistPop(['grimpex']))
        both.append(patient.getResistPop(['guttagonol', 'grimpex']))
    patient.addPrescription('gripmex')
    for _ in range(150):
        patient.update()
        total.append(patient.getTotalPop())
        guttagonol.append(patient.getResistPop(['guttagonol']))
        grimpex.append(patient.getResistPop(['grimpex']))
        both.append(patient.getResistPop(['guttagonol', 'grimpex']))
    pylab.title('Two drugs with delay')
    pylab.ylabel('Viruses')
    pylab.xlabel('Timesteps')
    pylab.plot(total, label='total')
    pylab.plot(guttagonol, label='guttagonol')
    pylab.plot(grimpex, label='grimpex')
    pylab.plot(both, label='both')
    pylab.legend(loc=1)

def plot_two_drugs_no_delay():
    total = []
    guttagonol =  []
    grimpex = []
    both = []
    viruses = [ResistantVirus(0.1, 0.05, {'guttagonol':False, 'grimpex':False}, 0.005)] * 100
    patient = Patient(viruses, 1000)

    for _ in range(150):
        patient.update()
        total.append(patient.getTotalPop())
        guttagonol.append(patient.getResistPop(['guttagonol']))
        grimpex.append(patient.getResistPop(['grimpex']))
        both.append(patient.getResistPop(['guttagonol', 'grimpex']))
    patient.addPrescription('guttagonol')
    patient.addPrescription('grimpex')
    for _ in range(150):
        patient.update()
        total.append(patient.getTotalPop())
        guttagonol.append(patient.getResistPop(['guttagonol']))
        grimpex.append(patient.getResistPop(['grimpex']))
        both.append(patient.getResistPop(['guttagonol', 'grimpex']))
    pylab.title('Two drugs without delay')
    pylab.ylabel('Viruses')
    pylab.xlabel('Timesteps')
    pylab.plot(total, label='total')
    pylab.plot(guttagonol, label='guttagonol')
    pylab.plot(grimpex, label='grimpex')
    pylab.plot(both, label='both')
    pylab.legend(loc=1)

def problem7():
    plot_two_drugs_with_delay()
    pylab.figure()
    plot_two_drugs_no_delay()
    pylab.show()
