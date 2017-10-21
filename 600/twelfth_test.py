from twelfth import *
import pytest

def test_random_event():
    assert random_event(0) == False
    assert random_event(1) == True

def test_infected_simple_patient():
    maxBirthProb = 0.7
    clearProb = 0.3
    viruses = [SimpleVirus(maxBirthProb, clearProb)] * 1000
    patient = SimplePatient(viruses, 100000)
    assert patient.getTotalPop() == 0
    patient.update()
    assert patient.getTotalPop() > 2000
    assert patient.getTotalPop() < 3000

def test_resistant_virus():
    virus = ResistantVirus(1, 0.05, {'grimpex': True, 'guttagonol': False}, 0.9)
    assert virus.isResistantTo(['grimpex']) == True
    assert virus.isResistantTo(['grimpex', 'guttagonol']) == False

def test_resistant_virus_does_not_reproduce_when_not_resistant_to_one_of_the_drugs():
    virus = ResistantVirus(1, 0.05, {'grimpex': True, 'guttagonol': False}, 0.01)
    with pytest.raises(NoChildException):
        virus.reproduce(0, ['grimpex', 'guttagonol'])

def test_resistant_virus_reproduces_when_resistant_to_one_of_the_drugs():
    virus = ResistantVirus(1, 0.05, {'grimpex': True, 'guttagonol': False}, 0.01)
    offspring = virus.reproduce(0, ['grimpex'])
    assert offspring.getResistance('grimpex') == True
    assert offspring.getResistance('guttagonol') == False

def test_resistant_virus_offspring_with_high_mutability_gains_new_traits():
    virus = ResistantVirus(1, 0.05, {'grimpex': True, 'guttagonol': False}, 0.9)
    offspring = virus.reproduce(0, [])
    assert offspring.getResistance('grimpex') == False
    assert offspring.getResistance('guttagonol') == True

def test_patient_progress_with_drugs():
    viruses = [ResistantVirus(1, 0.05, {'grimpex': True, 'guttagonol': False}, 0.01)] * 100
    patient = Patient(viruses, 1000)
    nonResistantTo = 'guttagonol'
    patient.addPrescription(nonResistantTo)
    assert patient.getResistPop(nonResistantTo) == 0
    for _ in range(150):
        patient.update()
    assert patient.getTotalPop() == 0
