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
        return {r:self.mutates(r) for r in list(set(self.resistances.keys() + activeDrugs))}

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
    viruses = [ResistantVirus(0.1, 0.05, {}, 0.005)] * 100
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

def problem5():
    pylab.title('Resistant virus patient treatment')
    pylab.ylabel('Number of viruses')
    pylab.xlabel('Timesteps')
    plot_simulation(300)
    plot_simulation(150)
    plot_simulation(75)
    plot_simulation(0)
    pylab.legend(loc=1)
    pylab.show()

    """
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """
    # TODO

#
# PROBLEM 6
#

def problem6():
    """
    Runs simulations and make histograms for problem 6.

    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """
    # TODO

#
# PROBLEM 7
#

def problem7():
    """
    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.

    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        
    """
    # TODO
