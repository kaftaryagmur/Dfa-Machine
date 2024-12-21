class DFA:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states

    def process(self, input_string):
        current_state = self.start_state
        print(f"\nStarting at state: {current_state}")

        for symbol in input_string:
            if symbol not in self.alphabet:
                print(f"Error: Invalid symbol '{symbol}' not in alphabet!")
                return False
            current_state = self.transition_function.get((current_state, symbol))
            if current_state is None:
                print(f"Error: No transition defined for ({current_state}, {symbol})")
                return False
            print(f"Read '{symbol}', transitioned to state: {current_state}")

        return current_state in self.accept_states

    def display_ascii_dfa(self):
        print("\nDFA Representation (ASCII):")
        print(f"States: {', '.join(self.states)}")
        print(f"Start State: {self.start_state}")
        print(f"Accept States: {', '.join(self.accept_states)}\n")
        print("Transitions:")
        for (state, symbol), next_state in self.transition_function.items():
            print(f"({state}) --{symbol}--> ({next_state})")
