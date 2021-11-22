

def start_completion(current_intput: str,):
    # dict of all commands that have been typed, with all params & flags as value (or maybe tuple better)??

    # check if last command is complete -- is there a space in the end?
    if current_intput[-1] == ' ':
        # complete current word
        pass
    else:
        # check if last command needs/can take params or flags -- will be done in second step
        # check for other commands - only complete commands that have not yet been typed (wanted)
        pass
