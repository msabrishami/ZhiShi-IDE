import IPython


class bC:
    GRN = '\033[92m'
    RED = '\033[91m'
    ORG = '\033[93m'
    ENDC = '\033[0m'
    BG1  = '\033[44m'
    BG0  = '\033[46m'
    BOLD = '\033[1m'

def msg_center(msg, maxL=60):
    padR = max(maxL - len(msg), 0)//2
    padL = max(maxL - (len(msg)+padR), 0)
    return " "*padR + msg + " "*padL


def print_title(fault=None, val=None, maxL=60):
    print("\033[H\033[J", end="")
    msg = msg_center("ZhiShi: ATPG Solution Report", maxL)
    print(f"{bC.BOLD}{msg}{bC.ENDC}")
    if fault is not None:
        msg = msg_center(f"DALG for '{fault}' SS@{val}", maxL)
        print(msg)
    print("_"*maxL)
    print()


def print_cmds(cmds, setup="curr", maxL=60, space=12):
    """ setup should be curr or next """
    if setup == "curr":
        msg = "Current instructions:"
        bCol = bC.BG1
    elif setup == "next":
        msg = "Possible next instructions:"
        bCol = bC.BG0
    else:
        return None

    msg = msg + " "*max(maxL - len(msg),0)
    print(f"{bCol}{msg}{bC.ENDC}")
    for cmd in cmds: 
        items = cmd.split()
        _cmd = ""
        for item in items[:-1]:
            pad = max(space - len(item), 0)
            _cmd += item+ " "*pad
        _cmd += items[-1]
        pad = max(maxL-len(_cmd),0)
        _cmd += " "*pad
        print(f"{bCol}{_cmd}{bC.ENDC}")


def possible_next(last_command):
    # Implement the logic to return a list of possible next commands
    # based on the last command
    items = last_command.split()
    if items[0]== "DALG" and "@" in items[1]:
        fault, stuck_val = items[1].split("@")
        nxt = "MAIN\tINJ\t<gate>\t<1/0>"
        return [nxt]
    
    base = items[0]
    op = items[1] 

    if base=="MAIN": 
        if op=="INJ":   nxt = "MAIN\tCAL\t#NUM"
        elif op=="CAL": nxt = f"{items[2]}\tInC\t<True/False>"
        elif op=="RET": nxt = f"{items[2]}"
        return [nxt]
    
    if items[1] == "CAL":
        nxt = f"{items[2]}\tInC\t<True/False>"
        return [nxt]
    
    if op == "RET" and items[2] == "MAIN":
        if items[3] == "True": nxt = "MAIN\tRET\tSUCCESS"
        elif items[3] == "False": nxt = "MAIN\tRET\tFAILURE"
        return [nxt]

    nxt = [f"{base}\t"]
    if op == "InC" and items[2] == "True":
        nxt[0] += f"REPORT\t<cktName>-<node>-<0/1>-sol-<idx>"
    elif op == "InC" and items[2] == "False":
        nxt[0] += f"RET\t#PARRENT\tFalse"
    elif op == "REPORT":
        nxt[0] += f"F@PO\t<True/False>"
    elif op == "F@PO" and items[2] == "False":
        nxt[0] += f"DF@0\t<True/False>"
    elif op == "F@PO" and items[2] == "True":
        nxt[0] += f"JF@0\t<True/False>"
    elif op == "DF@0" and items[2] == "False":
        nxt[0] += f"OPT\tDF.SELECT\t<gate>"
    elif op == "DF@0" and items[2] == "True":
        nxt[0] += f"RET\t#PARENT\tFalse"
    elif op == "OPT" and items[2] == "DF.SELECT":
        nxt[0] += f"OPT\tDF.GATE.VAL\t<line:val line:val ...>"
    elif op == "OPT" and items[2] == "DF.GATE.VAL":
        nxt[0] += "CAL\t#NEW-ID"
    elif op == "CAL":
        nxt[0] += f"{items[2]}InC\t<True/False>"
    elif op == "JF@0" and items[2] == "True":
        nxt[0] += "RET\t#PARRENT\tTrue"
    elif op == "JF@0" and items[2] == "False":
        nxt[0] += "OPT\tJF.SELECT\t<gate>"
    elif op == "OPT" and items[2] == "JF.SELECT":
        nxt[0] += "OPT\tJF.GATE.VAL\t<line:val line:val ...>"
    elif op == "OPT" and items[2] == "JF.GATE.VAL":
        nxt[0] += "CAL\t#NEW-ID"
        nxt.append(f"{base}\tJF.SELECT\t<gate>")
    elif op == "RET" and items[3] == "True":
        nxt[0] = f"{items[2]}\tRET\t#PARRENT\tTrue"
    elif op == "RET" and items[3] == "False":
        nxt[0] = f"#PARRENT\tOPT\tDF.SELECT\t<line:val line:val ...>"
        nxt.append(f"#PARRENT\tOPT\tJF.SELECT\t<line:val line:val ...>")
    else:
        nxt[0] = "... Umm! Not sure! ... "
    
    return nxt 


def get_fault():
    print_title()
    fault, sval = input("Enter the target fault <Node@Value> : ").split("@")
    return fault, sval

def main():

    fault, sval = get_fault()
    print_title(fault, sval)
    cmds = []
    cmds.append(f"DALG\t{fault}@{sval}")

    while True:
        print_cmds(cmds, "curr")
        print()
        if cmds[-1] in ["SUCCESS", "FAILURE"]:
            break
        next_commands = possible_next(cmds[-1])
        print_cmds(next_commands, "next")

        # Get user input
        while(True):
            command = input()
            if len(command) > 3: break
        if command.lower() in ['exit', 'quit', 'q']:
            break
        
        # Update instructions and last command
        cmds.append(command)

        # Clear screen (optional, for cleanliness)
        print("\033[H\033[J", end="")

    print("\033[H\033[J", end="")
    print_cmds(cmds)
    save = input("Save in file (yes/no)? ")
    if save.lower() in ["yes", "y", "ok"]:
        fname = input("Please enter the file name: ")
        with open(fname, "w") as outfile:
            outfile.write("\n".join(cmds))
            outfile.write("\n")

if __name__ == "__main__":
    main()

