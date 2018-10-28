"""
File: calculator.py
Purpose: Handles calculations
"""

import os.path as path
import re

import yaml
import click

import periodictable

# from Moiety import Moiety

here = path.dirname(path.abspath(__file__))
table = periodictable.table

um_file = path.join(here, "user_moieties.yaml")
with open(um_file, "r") as um_yaml:
    user_moieties = yaml.load(um_yaml) or {}

uh_file = path.join(here, "user_history.yaml")
with open(uh_file, "r") as uh_yaml:
    user_history = yaml.load(uh_yaml) or {}


def analyze(formula, moles=1):
    """ Parses the chemical formula into a dict containing the chemical profile of the compound being analyzed
    (ie, each el in the compound and its stoichiometric equivalence) """

    profile = {}
    # Matches an uppercase letter followed by any number of lowercase letters and
    # a number after them, or some wordy stuff contained in parentheses and whatever
    # numbers may be right after those parentheses
    compound = re.findall(r"([A-Z][a-z]*)(\d*)|\((\w*)\)(\d*)", formula)

    # compound is a list of 4-tuples
    # each tuple is a "moiety" of the compound
    # moiety[0]: "" if the moiety is contained in parentheses, else the chemical symbol of an el in the compound
    # moiety[1]: "" if the moiety is contained in parentheses, else the stoichiometric equivalence of moiety[0]
    # moiety[2]: a functionality of the compound being analyzed (a subformula contained in parentheses), else ""
    # moiety[3]: stoichiometric equivalence of moiety[2], else ""

    for moiety in compound:
        el = moiety[0]
        el_moles = moiety[1]

        # If you encounter an element on the periodic table
        if el in table.keys():
            # If that element is already in the profile, just add the moles to the current sum
            if el in profile:
                profile[el] += int(moles) * int(el_moles if el_moles != "" else 1)
            # If not, add it to the profile and set the sum equal to the moles of element
            else:
                profile[el] = int(moles) * int(el_moles if el_moles != "" else 1)

        # If you encounter a sub-moiety in parentheses
        elif el == "":
            submoiety = moiety[2]
            submoiety_moles = moiety[3]

            # Analyze the sub-moiety. Hooray for recursion.
            subprofile = analyze(submoiety, submoiety_moles)

            # Add elements of the profile as above
            for key, val in subprofile.items():
                if key in profile:
                    profile[key] += int(val)
                else:
                    profile[key] = int(val)

        # If you encounter a symbol in user_moieties
        else:
            submoiety_moles = int(el_moles) if el_moles != "" else 1
            subprofile = analyze(user_moieties[el]["eq_form"], submoiety_moles)
            for key, val in subprofile.items():
                if key in profile:
                    profile[key] += int(val)
                else:
                    profile[key] = int(val)

    return profile


def get_mass(compound):
    """ Gets the mass of a compound """
    mass = 0
    profile = analyze(compound)

    for el, moles in profile.items():
        mass += moles * table[el]

    return mass


def get_mass_spec(compound, histogram):
    profile = analyze(compound)
    total_mass = get_mass(compound)
    mass_spec = {}
    for el, moles in profile.items():
        mass_spec[el] = 100 * (moles * table[el]) / total_mass

    mass_spec_string = ""
    if histogram:
        bar_scale = 60
        for el, percent in mass_spec.items():
            bar = "█" * int(bar_scale * percent // 100)
            mass_spec_string += ("%4s : %s %.1f%%\n" % (el, bar, percent))
    else:
        for el, percent in mass_spec.items():
            mass_spec_string += ("%4s : %.1f%%\n" % (el, percent))

    return mass_spec_string.rstrip()
