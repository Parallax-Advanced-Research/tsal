import re

def key_words(txt, start, end):
    tsal = [":fluents", "(+", "(-", "(=", "(=", "(!=", "(%"]
    pddl = [":functions", "(increase", "(decrease", "(eq", "(set", "(neq", "(mod"]  #SET AND EQ do same thing, fluent vs pred. need general solution
    start = locals()[start]
    end = locals()[end]
    mapping = {start[i]: end[i] for i in range(len(tsal))}
    for k, v in mapping.items():
        txt = txt.replace(k, v)
    return txt

def group_text(txt, keyword):
    action_matches = re.finditer(keyword, txt)
    group = []
    action_se = []
    for action in action_matches:
        stack = 0
        startIndex = 0
        for i, c in enumerate(txt[action.start():]):
            if c == '(':
                if stack == 0:
                    startIndex = i + 1  # string to extract starts one index later
                # push to stack
                stack += 1
            elif c == ')':
                # pop stack
                stack -= 1
                if stack == 0:
                    action_txt = txt[action.start():action.start() + i + 1]
                    action_se.append((action.start(), action.start() + i + 1))
                    action_txt = '\t' + '\n\t'.join(action_txt.splitlines())
                    group.append(action_txt)
                    break
    #grouped_text = "(:actions\n" + '\n'.join(group) + '\n)'
    grouped_text = '\n'.join(group)
    actions_start = None
    if action_se:
        actions_start = action_se[0][0]
        remove_count = 0
        for start, end in action_se:
            start -= remove_count
            end -= remove_count
            diff = end - start
            remove_count += diff + 1
            txt = txt[0:start:] + txt[end+1::]
    return txt, actions_start, grouped_text, group

def forall_to_event(txt):
    action_txt, action_start, all_action_txt, action_group = group_text(txt, "\(:action")
    forall_matches = re.finditer("\(forall", txt)
    group = []
    forall_se = []
    counter = 0
    for forall in forall_matches:
        stack = 0
        startIndex = 0
        for i, c in enumerate(txt[forall.start():]):
            if c == '(':
                if stack == 0:
                    startIndex = i + 1  # string to extract starts one index later
                # push to stack
                stack += 1
            elif c == ')':
                # pop stack
                stack -= 1
                if stack == 0:
                    forall_txt = txt[forall.start():forall.start() + i + 1]
                    action = [x for x in action_group if forall_txt in x][0]
                    forall_txt = '\t' + '\n\t'.join(forall_txt.splitlines())
                    group.append(forall_txt)
                    print("and" in forall_txt)
                    type_txt, type_start, all_type_txt, type_group = group_text(forall_txt, "\(?")
                    when_txt, when_start, all_when_txt, when_group = group_text(forall_txt, "\(when")
                    and_txt, and_start, all_and_txt, and_group = group_text(forall_txt, "\(and")
                    if len(and_group) == 2:
                        precond_raw = and_group[0]
                        effect_raw = and_group[1]
                    elif len(and_group) == 1:
                        loc = when_group[0].find(and_group[0][1:])  #TODO if precond not and, update
                        precond_raw = and_group[0]
                        effect_raw = when_group[0][loc + len(and_group[0]):]
                    else:
                        pass
                    precond = []
                    effect = []
                    not_flag = False
                    for pre in precond_raw.split("(")[2:]:
                        if "not" in pre:
                            not_flag = True
                            continue
                        if not_flag:
                            precond.append("(not (" + pre.split(")")[0] + ")")
                        else:
                            precond.append("(" + pre.split(")")[0] + ")")
                        not_flag = False
                    for eff in effect_raw.split("(")[2:]:
                        if "not" in eff:
                            not_flag = True
                            continue
                        if not_flag:
                            effect.append("(not (" + eff.split(")")[0] + ")")
                        else:
                            effect.append("(" + eff.split(")")[0] + ")")
                        not_flag = False
                    arguments = [" ".join(x.split(" ")[1:]).replace(")", "").split(" ") for x in precond]
                    use_arguments = []
                    for x in arguments:
                        for y in x:
                            if y not in use_arguments:
                                use_arguments.append(y)
                    replace = "(forall" + str(counter) + " " + " ".join(use_arguments) + ")"
                    forall_se.append((forall.start(), forall.start() + i + 1, replace))
                    event_txt = "(:event for_all" + str(counter) + "\n\t:parameter("
                    counter += 1
                    break
    grouped_text = '\n'.join(group)
    actions_start = None
    if forall_se:
        actions_start = forall_se[0][0]
        remove_count = 0
        for start, end, replace in forall_se:
            rep_len = len(replace)
            start -= remove_count
            end -= remove_count
            diff = end - start
            remove_count += diff + 1 - rep_len
            txt = txt[0:start:] + replace + txt[end + 1::]
    pass

def write_to_file(file_name, txt):
    with open(file_name, "w") as f:
        f.write(txt)
    return file_name

def pddl_To_Tsal(pddl_file, typ):
    tsal_file = pddl_file.replace(pddl_file[-4:], "tsal")
    pddl = None
    with open(pddl_file, "r") as f:
        pddl = f.read()
    txt = key_words(pddl, "pddl", "tsal")
    if typ == "dom":
        txt, start, action_txt, actions = group_text(txt, "\(:action ")
        action_txt = "(:actions\n" + action_txt + '\n)'
        txt = txt[0:start:] + action_txt + txt[start::]
        txt, start, event_txt, events = group_text(txt, "\(:event ")
        event_txt = "(:events\n" + event_txt + '\n)'
        txt = txt[0:start:] + event_txt + txt[start::]
    elif typ == "prob":
        txt, start, metric_txt, metrics = group_text(txt, "\(:metric")
    write_to_file(tsal_file, txt)
    return tsal_file


def tsal_To_Pddl(tsal_file, typ):
    txt = key_words(tsal_file, "tsal", "pddl")
    if typ == "domain":
        txt, start, action_txt, actions = group_text(txt, "\(:action ")
        txt, start, actions_txt, actions_header = group_text(txt, "\(:actions\n")
        txt = txt[0:start:] + action_txt + txt[start::]
        txt, start, event_txt, events = group_text(txt, "\(:event ")
        txt, start, events_txt, events_header = group_text(txt, "\(:events\n")
        txt = txt[0:start:] + event_txt + txt[start::]
        txt, start, derived_txt, derived = group_text(txt, "\(:derived")
        txt, start, derived_txt, derived = group_text(txt, "\(:processes")
        pass
    elif typ == "problem":
        txt, start, timed_txt, timed_init = group_text(txt, "\(:timed-init")
    return txt


