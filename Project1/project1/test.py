import subprocess
import re


RED    = '\33[101m'
GREEN  = '\33[102m'
DEFAULT = '\x1b[0m'


class TestRes:
    def __init__(self, victory: bool, score: int, node_nb: int, time: float):
        self.victory = victory
        self.score = score
        self.node_nb = node_nb
        self.time = time

class ResHminimax:
    def __init__(self, name: str):
        self.name = name
        self.small = []
        self.medium = []
        self.large = []
        self.large_easy = []
    
    def __str__(self):
        str_res = self.name + ":\n"
        str_res += "small: "
        str_res += "Win" if self.all_win('small') else "Lose"
        str_res += "\n"
        for res in self.small:
            str_res += f"\tScores: {res.score}\tNodes: {res.node_nb}\tTime: {res.time}\n"
        if self.medium:
            str_res += "\nMedium: "
            str_res += "Win" if self.all_win('medium') else "Lose"
            str_res += "\n"
            for res in self.medium:
                str_res += f"\tScores: {res.score}\tNodes: {res.node_nb}\tTime: {res.time}\n"
        if self.large:
            str_res += "\nLarge: "
            str_res += "Win" if self.all_win('large') else "Lose"
            str_res += "\n"
            for res in self.large:
                str_res += f"\tScores: {res.score}\tNodes: {res.node_nb}\tTime: {res.time}\n"
        if self.large_easy:
            str_res += "\nLarge easy: "
            str_res += "Win" if self.all_win('large_easy') else "Lose"
            str_res += "\n"
            for res in self.large_easy:
                str_res += f"\tScores: {res.score}\tNodes: {res.node_nb}\tTime: {res.time}\n"
        str_res += "\n"

        return str_res
    
    def add_res_small(self, new_res: TestRes):
        self.small.append(new_res)

    def add_res_medium(self, new_res: TestRes):
        self.medium.append(new_res)

    def add_res_large(self, new_res: TestRes):
        self.large.append(new_res)

    def add_res_large_easy(self, new_res: TestRes):
        self.large_easy.append(new_res)
    
    def win_small(self):
        for res in self.small:
            if not res.victory:
                return False
        return True
    
    def win_medium(self):
        for res in self.medium:
            if not res.victory:
                return False
        return True
    
    def win_large(self):
        for res in self.large:
            if not res.victory:
                return False
        return True
    
    def win_large_easy(self):
        for res in self.large_easy:
            if not res.victory:
                return False
        return True

    def all_win(self, name: str):
        if name == 'small':
            return self.win_small()
        elif name == 'medium':
            return self.win_medium()
        elif name == 'large':
            return self.win_large()
        elif name == 'large_easy':
            return self.win_large_easy()
    
    def check_all_win(self, name: str):
        res = False
        if name == 'small':
            res = self.win_small()
        elif name == 'medium':
            res = self.win_medium()
        elif name == 'large':
            res = self.win_large()
        elif name == 'large_easy':
            res = self.win_large_easy()

        if res:
            print(GREEN + "Success" + DEFAULT)
        else:
            print(RED + "Failure" + DEFAULT)
    


def report(ouput: str) -> TestRes:
    ouput = ouput.decode('utf-8')
    victory = False

    if re.match('Pacman emerges victorious!', ouput):
        victory = True
    
    score = re.search(r"Score: (-?\d+)", ouput)
    if score:
        score = int(score.group(1))
    
    node = re.search(r"nodes : (\d+)", ouput)
    if node:
        node = int(node.group(1))

    time = re.search(r"\(seconds\) : (\d+)\.(\d+)", ouput)
    if time:
        time = float(time.group(1) + "." + time.group(2))

    return TestRes(victory, score, node, time)


# minimax
res_minimax = ResHminimax("Minimax")
res = subprocess.check_output('python run.py --agentfile minimax.py --ghost dumby --layout small_adv --silentdisplay', shell=True)
res_minimax.add_res_small(report(res))
res = subprocess.check_output('python run.py --agentfile minimax.py --ghost greedy --layout small_adv --silentdisplay', shell=True)

res_minimax.add_res_small(report(res))
res = subprocess.check_output('python run.py --agentfile minimax.py --ghost smarty --layout small_adv --silentdisplay', shell=True)

res_minimax.add_res_small(report(res))


# hminimax0
# small
hminimax0_res = ResHminimax("Hminimax0")
res = subprocess.check_output('python run.py --agentfile hminimax0.py --ghost dumby --layout small_adv --silentdisplay', shell=True)

hminimax0_res.add_res_small(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax0.py --ghost greedy --layout small_adv --silentdisplay', shell=True)

hminimax0_res.add_res_small(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax0.py --ghost smarty --layout small_adv --silentdisplay', shell=True)

hminimax0_res.add_res_small(report(res))

# medium
res = subprocess.check_output('python run.py --agentfile hminimax0.py --ghost dumby --layout medium_adv --silentdisplay', shell=True)

hminimax0_res.add_res_medium(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax0.py --ghost greedy --layout medium_adv --silentdisplay', shell=True)

hminimax0_res.add_res_medium(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax0.py --ghost smarty --layout medium_adv --silentdisplay', shell=True)

hminimax0_res.add_res_medium(report(res))


# large
res = subprocess.check_output('python run.py --agentfile hminimax0.py --ghost dumby --layout large_adv --silentdisplay', shell=True)

hminimax0_res.add_res_large(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax0.py --ghost greedy --layout large_adv --silentdisplay', shell=True)

hminimax0_res.add_res_large(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax0.py --ghost smarty --layout large_adv --silentdisplay', shell=True)

hminimax0_res.add_res_large(report(res))

# large easy
res = subprocess.check_output('python run.py --agentfile hminimax0.py --ghost dumby --layout large_adv_easy --silentdisplay', shell=True)

hminimax0_res.add_res_large_easy(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax0.py --ghost greedy --layout large_adv_easy --silentdisplay', shell=True)

hminimax0_res.add_res_large_easy(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax0.py --ghost smarty --layout large_adv_easy --silentdisplay', shell=True)

hminimax0_res.add_res_large_easy(report(res))


# hminimax1
# small
hminimax1_res = ResHminimax("Hminimax1")
res = subprocess.check_output('python run.py --agentfile hminimax1.py --ghost dumby --layout small_adv --silentdisplay', shell=True)

hminimax1_res.add_res_small(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax1.py --ghost greedy --layout small_adv --silentdisplay', shell=True)

hminimax1_res.add_res_small(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax1.py --ghost smarty --layout small_adv --silentdisplay', shell=True)

hminimax1_res.add_res_small(report(res))


# medium
res = subprocess.check_output('python run.py --agentfile hminimax1.py --ghost dumby --layout medium_adv --silentdisplay', shell=True)

hminimax1_res.add_res_medium(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax1.py --ghost greedy --layout medium_adv --silentdisplay', shell=True)

hminimax1_res.add_res_medium(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax1.py --ghost smarty --layout medium_adv --silentdisplay', shell=True)

hminimax1_res.add_res_medium(report(res))


# large
res = subprocess.check_output('python run.py --agentfile hminimax1.py --ghost dumby --layout large_adv --silentdisplay', shell=True)

hminimax1_res.add_res_large(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax1.py --ghost greedy --layout large_adv --silentdisplay', shell=True)

hminimax1_res.add_res_large(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax1.py --ghost smarty --layout large_adv --silentdisplay', shell=True)

hminimax1_res.add_res_large(report(res))


# large easy
res = subprocess.check_output('python run.py --agentfile hminimax1.py --ghost dumby --layout large_adv_easy --silentdisplay', shell=True)

hminimax1_res.add_res_large_easy(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax1.py --ghost greedy --layout large_adv_easy --silentdisplay', shell=True)

hminimax1_res.add_res_large_easy(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax1.py --ghost smarty --layout large_adv_easy --silentdisplay', shell=True)

hminimax1_res.add_res_large_easy(report(res))


# hminimax2
# small
hminimax2_res = ResHminimax("Hminimax2")
res = subprocess.check_output('python run.py --agentfile hminimax2.py --ghost dumby --layout small_adv --silentdisplay', shell=True)

hminimax2_res.add_res_small(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax2.py --ghost greedy --layout small_adv --silentdisplay', shell=True)

hminimax2_res.add_res_small(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax2.py --ghost smarty --layout small_adv --silentdisplay', shell=True)

hminimax2_res.add_res_small(report(res))


# medium
res = subprocess.check_output('python run.py --agentfile hminimax2.py --ghost dumby --layout medium_adv --silentdisplay', shell=True)

hminimax2_res.add_res_medium(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax2.py --ghost greedy --layout medium_adv --silentdisplay', shell=True)

hminimax2_res.add_res_medium(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax2.py --ghost smarty --layout medium_adv --silentdisplay', shell=True)

hminimax2_res.add_res_medium(report(res))


# large
res = subprocess.check_output('python run.py --agentfile hminimax2.py --ghost dumby --layout large_adv --silentdisplay', shell=True)

hminimax2_res.add_res_large(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax2.py --ghost greedy --layout large_adv --silentdisplay', shell=True)

hminimax2_res.add_res_large(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax2.py --ghost smarty --layout large_adv --silentdisplay', shell=True)

hminimax2_res.add_res_large(report(res))


# large easy
res = subprocess.check_output('python run.py --agentfile hminimax2.py --ghost dumby --layout large_adv_easy --silentdisplay', shell=True)

hminimax2_res.add_res_large_easy(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax2.py --ghost greedy --layout large_adv_easy --silentdisplay', shell=True)

hminimax2_res.add_res_large_easy(report(res))
res = subprocess.check_output('python run.py --agentfile hminimax2.py --ghost smarty --layout large_adv_easy --silentdisplay', shell=True)

hminimax2_res.add_res_large_easy(report(res))

print(res_minimax)
print(hminimax0_res)
print(hminimax1_res)
print(hminimax2_res)