import sys

class console_output:
    @classmethod
    def title (self):
        print('                     Urna eletrônica                    ')

    @classmethod
    def menu (self, name, index):
        print(f':: Para o Candidato {name} - Digite [{index}]')

    @classmethod
    def sep (self):
        print('--------------------------------------------------------')

    @classmethod
    def new_line (self):
        print('\r\n')

    @classmethod
    def exit_option (self):
        print(':: Para sair - Digite [0]')

class Candidate:
    def __init__(self, name, votes):
        self.name = name
        self.votes = votes
    def __repr__(self):
        return '{' + self.name + ', ' + str(self.votes) + '}'

    @classmethod
    def getNull (self):
        return Candidate('Nulo', 0)

class ElectronicVotingMachine:
    def __init__(self) -> None:
        self.option = 0
        self.candidates = []
    
    @classmethod
    def register (self, candidates):
        self.candidates = candidates
        self.candidates.insert(0, None)

    @classmethod
    def input (self) -> int:
        self.option = int(input('Informe o n° de seu candidato(a): '))
        return self.option
            
    @classmethod
    def confirm (self):
        self.candidates[self.option].votes += 1
        print('Votação realizada com sucesso! \n\r')
    
    @classmethod
    def getCadidates (self):
        return [candidate for candidate in self.candidates if candidate]
    
    @classmethod
    def banner (self):
        candidates = self.candidates
        console_output.new_line()
        console_output.title()
        console_output.sep()
        for candidate in candidates:
            if candidate:
                console_output.menu(candidate.name, candidates.index(candidate))
        console_output.exit_option()
        console_output.sep()
        console_output.new_line()

class CheckUrn:
    def __init__(self, candidates) -> None:
        self.candidates = candidates
    
    def allEquals (self, candidates) -> bool:
        iterator = iter(candidates)
        try:
            first = next(iterator)
        except StopIteration:
            return True
        return all(first.votes == x.votes for x in iterator)

    def verifyWinnerCandidate (self) -> str:
        sortedByVotes = sorted(self.candidates, key=lambda x: x.votes, reverse=True)
        candidateWinner = sortedByVotes[0]
        if self.allEquals(sortedByVotes) or sortedByVotes[0].votes == sortedByVotes[1].votes:
            return '\n\rNão houve ganhador, haverá segundo turno!'
        elif candidateWinner.name == 'Nulo':
            return '\n\rHaverá segundo turno, pois não houve ganhadores!'
        return f'\n\rO candidato(a) {candidateWinner.name} ganhou a Eleição!'

    def results (self):
        print('\r')
        for candidate in self.candidates:
            if candidate.name == 'Nulo':
                print(f'Votos nulos {candidate.votes}.')
            else:
                print(f'O candidato(a) {candidate.name} teve, {candidate.votes}, votos.')
        print(self.verifyWinnerCandidate())

def registerDataWithCallback (callback, **keysargs):
    register = keysargs.get('register')
    candidates = []
    if register:
        for i in range(0, int(register)):
            text = f':: [{i + 1}/{register}] Digite o nome do candidato: '
            name = input(text)
            candidates.append(Candidate(name, 0))
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
        candidates.append(Candidate.getNull())
        callback(candidates)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        amount = sys.argv[1].split('=')[1]
        registerDataWithCallback(ElectronicVotingMachine.register, register=amount)
    else:
        ElectronicVotingMachine.register([
        Candidate('John Doe', 0),
        Candidate('Linus Torvalds', 0),
        Candidate('Judd Vinet', 0),
        Candidate.getNull()
    ])
    print('\x1b[2J\x1b[1;1H', end='')
    ElectronicVotingMachine.banner()
    while True:
        try:
            option = ElectronicVotingMachine.input()
            if option == 0:
                break
            ElectronicVotingMachine.confirm()
        except KeyboardInterrupt:
            print('\n\rPrograma interrompido pelo usuário!')
            sys.exit(0)
        except:
            print('Atenção, opção inválida!\n\r')
    data = CheckUrn(ElectronicVotingMachine.getCadidates())
    data.results()
