
def act(a):
    """
    simple function to easily change the action number into a string
    returns string
    """
    if a == 0:
        return "BOUGHT AWAY"
    elif a == 1:
        return "BOUGHT HOME"
    elif a == 2:
        return "SKIP"
    else:
        return "action outside of defined actions"
