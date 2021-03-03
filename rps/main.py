from random import choice

class RPS:
    def __init__(self):
        pass

    # some more functions will go here

game = RPS()

self.rules = {
    'rock' 		: 'scissors',
    'paper'	    : 'rock',
    'scissors'  : 'paper'
}

  def err(self, msg):
		print(f"ERROR: {msg}")

	def disp_scores(self):
		print(f"SCORES:\n\tYOU: {self.usr_score}\n\tCPU: {self.cpu_score}\n")

	def tie(self):
		print("It's a tie")
		self.usr_score += 1
		self.cpu_score += 1

	def usr_win(self):
		print("You won!")
		self.usr_score += 1

	def cpu_win(self):
		print("CPU won!")
		self.cpu_score += 1

	def ask(self):
        for x in range( len(self.opt) ): print(f"{i + 1}. {self.opt[i]}")
        usr = input("\nSelect one option: ")

# exception handling (copy pasted mosta this)
        try: usr = int(usr) - 1
	   except ValueError:
		         self.err("INPUT INVALID! YOU MUST INPUT A NUMBER!\n")
		               return self.ask()
	    if -1 < usr < len(self.opt): return self.opt[usr]
	   else:
		self.err( "INPUT INVALID! YOU MUST INPUT A NUMBER BETWEEN 1 AND {len(self.opt)}!\n" )
		return self.ask()

    def match(self):
        cpu = choice(self.opt)
        usr = self.ask()
        print(f"You chose {usr.upper()} and the CPU chose {cpu.upper()}")
        if cpu == usr: self.tie()
        else:
            if self.rules[usr] == cpu: self.usr_win()
            else: self.cpu_win()
        pass
        self.disp_scores()
            endit = input("Press q to stop, or enter")
            print()
            If not endit: self.match()
            else: print("closing...")
