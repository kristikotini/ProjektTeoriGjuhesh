import read_states


class NFA:
    def __init__(self, start_state, final_states, alphabet):
        self.start_state = start_state
        self.final_states = final_states
        self.alphabet = alphabet

