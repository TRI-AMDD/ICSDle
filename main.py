from pymatgen.core import Composition
import random
from data import get_data
from datetime import datetime


CARDINALITIES = ["unary", "binary", "ternary", "quaternary", "quinary", "hexanary", "heptanary"]
def check_formula(guess, answer, cardinality=True):
    gcomp = Composition(Composition(guess).reduced_formula)
    acomp = Composition(Composition(answer).reduced_formula)
    response = []
    if cardinality:
        gcardinality = CARDINALITIES[len(gcomp)-1]
        gcardinality += '\x1b[m:'
        label = "correct" if len(gcomp) == len(acomp) else "nothing"
        response.append([gcardinality, label])
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
            elif elt.row in acomp_rows:
                response += [[str(elt), "row"]]
            else:
                response += [[str(elt), "nothing"]]
            response += [[str(stoich), "nothing"]]
    return response


COLORS = {"correct": "30;42",
          "group": "30;43",
          "row": "30;45",
          "nothing": 0
          }

EMOJIS = {"correct": "\U0001f7e9",
          "group": "\U0001f7e8",
          "row": "\U0001f7ea",
          "nothing": "\U0001f533"
          }


def format_response(response, colors=COLORS):
    string = ""
    for r in response:
        string += "\x1b[{}m".format(colors[r[1]])
        string += r[0]
    string += "\x1b[m"
    return string


def format_response_emojis(response, emojis=EMOJIS):
    return "".join([emojis[r[1]] for r in response])


def run_game(answer="random"):
    formulas = get_data()
    if isinstance(answer, int):
        answer = formulas[answer]
    elif answer == "daily":
        random.seed(int(datetime.utcnow().strftime("%Y%m%d")))
        answer = random.choice(formulas)
    elif answer == "random":
        answer = random.choice(formulas)
    else:
        raise ValueError("{} is not a valid answer mode".format(answer))
    print("\x1b[{}mcorrect element\x1b[m, \x1b[{}mcorrect group\x1b[m, \x1b[{}mcorrect row\x1b[m".format(
        COLORS['correct'], COLORS['group'], COLORS['row']
    ))
    solved = False
    turns = 0
    all_responses = []
    while not solved:
        guess = input("Enter formula:")
        if guess == "exit":
            break
        try:
            comp = Composition(guess)
        except:
            print("Composition {} not valid".format(guess))
            continue
        if comp.reduced_formula not in formulas:
            print("{} not in ICSD formulas".format(guess))
        else:
            response = check_formula(guess, answer)
            all_responses.append(response)
            print(format_response(response))
            turns += 1
            if comp == Composition(answer):
                print("Solved on turn {}".format(turns))
                solved = True
    if not solved:
        print("Answer: {}".format(answer))
    else:
        print("\n".join(
            [format_response_emojis(response)
             for response in all_responses]))


if __name__ == "__main__":
    run_game(answer="daily")
