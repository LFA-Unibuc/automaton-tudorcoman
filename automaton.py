class RejectionException(Exception):
    pass

class Automaton():
    def __init__(self, config_file):
        self.config_file = config_file
        self.sigma = []
        self.states = []
        self.transitions = []
        self.initialState = ""
        self.finalStates = []

    @staticmethod
    def get_sigma(lines, st, dr):
        lista = []
        for i in range(st, dr):
            word = lines[i].split()
            if len(word) != 1:
                return ["invalid"]
            lista.append(word[0])
        return lista

    @staticmethod
    def get_states(lines, st, dr):
        lista = []
        s = 0
        finalStates = []
        for i in range(st, dr):
            state = [tok.strip() for tok in lines[i].split(',')]
            lista.append(state[0])
            if 'S' in state:
                initialState = state[0]
                s += 1
                if s > 1:
                    return ["invalid"]
            if 'F' in state:
                finalStates.append(state[0])

        return (lista, initialState, finalStates)

    @staticmethod
    def get_transitions(lines, st, dr):
        tr = []
        for i in range(st, dr):
            transition = [x.strip() for x in lines[i].split(',')]
            if len(transition) != 3:
                return ["invalid"]
            tr.append(transition)
        return tr

    def validate(self):
        """Return a Boolean

        Returns true if the config file is valid,
        and raises a ValidationException if the config is invalid.
        """        

        with open(self.config_file, "r") as inpf:
            input_str = inpf.read()
            try:
                self.read_input(input_str)
                for transition in self.transitions:
                    if transition[0] not in self.states or transition[2] not in self.states or transition[1] not in self.sigma:
                        return False
                return True
            except RejectionException:
                return False
       
        return True

    def accepts_input(self, input_str):
        """Return a Boolean

        Returns True if the input is accepted,
        and it returns False if the input is rejected.
        """

        try:
            self.read_input(input_str)
            return True
        except RejectionException:
            return False

    def read_input(self, input_str):
        """Return the automaton's final configuration
        
        If the input is rejected, the method raises a
        RejectionException.
        """

        lines = input_str.split('\n')
        lines = [line for line in lines if len(line) and not line.startswith('#')]

        n = len(lines) - 1
        i = 0
        while i < n:
            
            # inceput de sectiune
            section = lines[i].split()[0]
            j = i + 1
            while j < n and lines[j] != 'End':
                j += 1
            
            if section == 'Sigma':
                self.sigma = Automaton.get_sigma(lines, i + 1, j)
                
                if self.sigma == ["invalid"]:
                    raise RejectionException()
            elif section == 'States':
                (self.states, self.initialState, self.finalStates) = Automaton.get_states(lines, i + 1, j)
                
                if self.states == ["invalid"]:
                    raise RejectionException()
            elif section == 'Transitions':
                self.transitions = Automaton.get_transitions(lines, i + 1, j)
                if self.transitions == ["invalid"]:
                    raise RejectionException()
            else:
                raise RejectionException()
            
            i = j + 1        

if __name__ == "__main__":
    a = Automaton('config.cfg')
    print(a.validate())
    print(a.sigma)
