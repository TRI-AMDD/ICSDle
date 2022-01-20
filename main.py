from pymatgen.core import Composition
import random
from data import get_data


def check_formula(guess, answer):
    gcomp = Composition(Composition(guess).reduced_formula)
    acomp = Composition(Composition(answer).reduced_formula)
    response = []
    acomp_groups = [e.group for e in acomp]
    acomp_rows = [e.row for e in acomp]
    for elt in gcomp:
        stoich = int(gcomp.get(elt))
        if elt in acomp:
            response += [[str(elt), "correct"]]

            if stoich == acomp.get(elt):
                response += [[str(stoich), "correct"]]
            else:
                response += [[str(stoich), "nothing"]]
        else:
            if elt.group in acomp_groups:
                response += [[str(elt), "group"]]
            elif elt.group in acomp_rows:
                response += [[str(elt), "row"]]
            else:
                response += [[str(elt), "nothing"]]
            response += [[str(stoich), "nothing"]]
    return response


COLORS = {"correct": 42,
          "group": 43,
          "row": 45,
          "nothing": 0
          }


def format_response(response, colors=COLORS):
    string = ""
    for r in response:
        string += "\x1b[{}m".format(colors[r[1]])
        string += r[0]
    return string


def run_game(turns=10):
    formulas = get_data()
    answer = random.choice(formulas)
    for n in range(turns):
        guess = input("Enter formula:")
        if Composition(guess).reduced_formula not in formulas:
            print("{} not in ICSD formulas".format(guess))
        else:
            response = check_formula(guess, answer)
            print(format_response(response))
            if all([r[1] == "correct" for r in response]):
                print("Solved on turn {}".format(n+1))
                break


if __name__ == "__main__":
    run_game()
