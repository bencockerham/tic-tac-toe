def clear(): #use to clear the screen before each re-draw
	print(' \n' *25)

class Player(object): 
	def __init__(self, name, designation_x, score):
		self.name = name
		self.designation_x = designation_x
		self.score = score
		
	'''def set_name(self):
		self.name = raw_input('What is your name? ')
		return'''
		
	def set_designation(self): #the idea is that this function is only used with p1, therefore we find p2's designation as the opposite of p1
		choosing = True
		while choosing:
			choose = raw_input('Would you like to be X or O? ')
			if choose.upper() == 'X':
				self.designation_x = True
				choosing = False
			elif choose.upper() == 'O':
				self.designation_x = False
				choosing = False
			else:
				print 'Please only choose X or O'
	#need to find a method to insure that both players aren't the same designation

class Board(object):
	def __init__(self, name, height_width): # height and width should be equal
		self.name = name
		self.height_width = height_width #height in 'lines' and width in 'space' characters
		
	def set_size(self):
		print 'Please input new height/width dimmension for the board squares. Note: height and width are equal'
		setting = True
		while setting:
			try:
				dimm = int(raw_input('Enter one integer between 4 and 20 for the height and width. A range between 5 and 15 is recommended.'))
				if dimm in range(4,20):
					self.height_width = dimm
					setting = False
				else:
					print 'Please choose a number between 4 and 20'
			except ValueError:
				print 'Please only enter an integer'
		print 'The new board square size is: ' + str(self.height_width) + ' X ' + str(self.height_width)
	
	def draw_board(self):
		clear()
		rowA.draw()
		print('- '*self.height_width*2)
		rowB.draw()
		print('- '*self.height_width*2)
		rowC.draw()

class BoardSpace(object):
	def __init__(self, name, x_c, y_c, state, ownership):
		self.name = name
		self.x_c = x_c #the X coordinates of the object (ie 1,2,3)
		self.y_c = y_c #the Y coordinates of the object (ie A,B,C)
		self.state = state  #does this display X, O, or nothing? Could also add in more states to
		self.ownership = ownership #who owns this object? p1, p2, or none?
		
	def set_state(self):
		self.ownership = gameplay.activeplayer
		if gameplay.activeplayer == 'p1':
			if p1.designation_x == True:
				self.state = 'x'
			else:
				self.state = 'o'
		elif gameplay.activeplayer == 'p2':
			if p2.designation_x == True:
				self.state = 'x'
			else:
				self.state = 'o'
		else:
			print 'STATE SET ERROR'
		
class BoardRow(object):
	def __init__(self, name, position, height, width, w, s): 
		self.name = name
		self.position = position # 'A' 'B' or 'C' only
		self.height = height
		self.width = width
		self.w = w #interior iterator for draw_x (etc) functions within cells
		self.s = w #exterior iterator for draw_x (etc) functions within cells

	def draw_x(self):
		print((' '*self.s + 'x' + ' ' *(self.w-1)) + (' ' *(self.w-1) + 'x' + ' '*self.s)),

	def draw_o(self):
		print((' '*(self.w-1) + 'o' + ' '*self.s) + (' '*self.s + 'o' + ' '*(self.w-1))),
	
	def draw_empty(self):
		print(' '*self.width),
		
	def draw_n(self):
		print '\n',
		
	def draw_side(self):
		print '|',

	def draw(self): 
		space_dict = {}
		draw_dict = {}
		self.height = board.height_width
		self.width = board.height_width
		import gc
		for obj in gc.get_objects():
			if isinstance(obj, BoardSpace):
				space_dict[obj.name] = [obj.y_c, obj.x_c, obj.state]
		for space in space_dict:
			if space_dict[space][0] == self.position:
				spacex = space_dict[space][1]
				spacestate = space_dict[space][2]
				if spacestate == 'x':
					spacedraw = self.draw_x
				elif spacestate == 'o':
					spacedraw = self.draw_o
				else:
					spacedraw = self.draw_empty
				draw_dict[spacex] = [spacedraw]
		draw_dict[4] = [self.draw_n]
		self.w = self.width/2
		self.s = 0
		for h in range(self.height/2):
			draw_dict[1][0](), self.draw_side(), draw_dict[2][0](), self.draw_side(), draw_dict[3][0](), draw_dict[4][0]()
			self.w -= 1
			self.s += 1
			#print '\n'
		self.w += 1
		self.s -= 1
		for j in range(self.height/2):
			draw_dict[1][0](), self.draw_side(), draw_dict[2][0](), self.draw_side(), draw_dict[3][0](), draw_dict[4][0]()
			self.w += 1
			self.s -= 1
			#print '\n'
		#print('- '*self.width*2) #spacing didn't work out with width*3, unsure why (maybe just character size). *2 seems to look pretty good
		
class Scoreboard(object):
	def __init__(self, name, games, game_no, p1, p2, tie):
		self.name = name
		self.game_no = game_no #iterative game number
		self.games = {} #format [iterative game number] = [winner, turns]
		self.p1 = p1 #cumulative total of wins for p1
		self.p2 = p2 #cumulative total of wins for p2
		self.tie = tie #cumulative total of ties
		
	def update(self):
		game = self.game_no + 1
		self.game_no = game
		self.games[game] = [gameplay.activeplayer, gameplay.turn]
		if gameplay.activeplayer == 'p1':
			self.p1 += 1
		else:
			pass
		if gameplay.activeplayer == 'p2':
			self.p2 += 1
		else:
			pass
		if gameplay.activeplayer == 'tie':
			self.tie += 1
		else:
			pass
		
	def display_scoreboard(self):
		clear()
		for n in range(3):
			print ('*'*60)
		print 'SCOREBOARD'
		for n in range(3):
			print ('*'*60)
		print 'NAME' + (' '*15) + 'SCORE'
		print p1.name + (' '*15) + str(self.p1)
		print p2.name + (' '*15) + str(self.p2)
		print 'TIE' + (' '*15) + str(self.tie)
		raw_input('Press Enter to list all game results')
		for n in range(3):
			print ('*'*60)
		print('Game Number: Winner, Turns')
		for g in self.games:
			print str(g) + ': ' + str(self.games[g])

class Gameplay(object):
	def __init__(self, name, turn, activeplayer, current_move):
		self.name = name
		self.turn = turn #the current turn number (odd is p1, even is p2). Iterative
		self.activeplayer = activeplayer
		self.current_move = current_move #name of boardspace that activeplayer is selecting during the current turn
	
	def reset_boardspaces(self): #sets all boardspace objects to empty and no ownership; resets turn count
		A1.state = 'empty'
		A1.ownership = 'none'
		A2.state = 'empty'
		A2.ownership = 'none'
		A3.state = 'empty'
		A3.ownership = 'none'
		B1.state = 'empty'
		B1.ownership = 'none'
		B2.state = 'empty'
		B2.ownership = 'none'
		B3.state = 'empty'
		B3.ownership = 'none'
		C1.state = 'empty'
		C1.ownership = 'none'
		C2.state = 'empty'
		C2.ownership = 'none'
		C3.state = 'empty'
		C3.ownership = 'none'
		self.turn = 1
	
	def startup(self): #selecting board size, player names, and x/o designations
		clear()
		print 'Welcome to the game!'
		print 'For Player 1:'
		p1.name = raw_input('What is your name? ')
		print 'For Player 2:'
		p2.name = raw_input('What is your name? ')
		print 'For Player 1:'
		p1.set_designation()
		if p1.designation_x == True:
			p2.designation_x = False
		else:
			p2.designation_x = True
		print 'Default Board size is square = 10x10.  Would you like to change that?'
		change = raw_input('Y/N ')
		if change.upper() == 'Y':
			board.set_size()
		elif change.upper() == 'N':
			pass
		else:
			print 'Please enter Y or N only'
		self.reset_boardspaces()
		self.activeplayer = 'p1'
		self.turn = 1
	
	def play(self): #the interactions with the player and storing results
		if self.turn % 2 == 0:
			self.activeplayer = 'p2'
		else:
			self.activeplayer = 'p1'
		space_dict = {} #houses all spaces and their states
		open_spaces = {} #houses all open spaces
		import gc
		for obj in gc.get_objects():
			if isinstance(obj, BoardSpace):
				space_dict[obj.name] = [obj.state]
		for space in space_dict:
			if space_dict[space][0] == 'empty':
				set_space_routine = set_state_dict[space][0]
				open_spaces[space] = ['empty', set_space_routine ]  #populates with list of open spaces, designation empty, and the corresponding set_state routine
		board.draw_board() #draw board function
		print 'Player' + self.activeplayer + 'please enter the square designation. The current open squares are: '
		print sorted(open_spaces)
		selecting = True
		while selecting:
			move = raw_input('Please enter square letter/number designation \n')
			if move in sorted(open_spaces):
				selecting = False
			else:
				print 'Make sure to only enter an open space!'
		print self.activeplayer + ' selected ' + move
		open_spaces[move][1]() #calls set_space routine for the selected space ('move')
		win = self.win_check()
		if win == True:
			board.draw_board()
			print self.activeplayer + ' wins!' 
			#need scoreboard routine
		elif win == False:
			self.turn += 1
		return win
				
	def tie_check(self):
		open_list = []
		x = 0
		import gc
		for obj in gc.get_objects():
			if isinstance(obj, BoardSpace):
				if obj.state == 'empty':
					open_list.append(obj)
		for open in open_list:
			x += 1
		tie = True
		if x == 0:
			tie = True
			print 'Tie!'
		else:
			tie = False
		return tie
				
	def win_check(self): #after the play interaction, tally up the votes
		win = False
		all_space_dict = {} #dict for all spaces
		x_list = [] #list of x coordinates
		y_list = [] #list of y coordinates
		import gc
		for obj in gc.get_objects():
			if isinstance(obj, BoardSpace):
				all_space_dict[obj.name] = [obj.ownership, obj.y_c, obj.x_c]
			else:
				pass
		for space in all_space_dict:
			if all_space_dict[space][0] == self.activeplayer:
				x_list.append(all_space_dict[space][2])
				y_list.append(all_space_dict[space][1])
		Acount = y_list.count('A')
		Bcount = y_list.count('B')
		Ccount = y_list.count('C')
		Y1count = x_list.count(1)
		Y2count = x_list.count(2)
		Y3count = x_list.count(3)
		if Acount >= 3:
			win = True
		elif Bcount >= 3:
			win = True
		elif Ccount >= 3:
			win = True
		elif Y1count >= 3:
			win = True
		elif Y2count >= 3:
			win = True			
		elif Y3count >= 3:
			win = True
		else:
			pass
		diag = False
		diag = self.diag_check()
		if diag == True:
			win = True
		else:
			pass
		return win
		
	def diag_check(self):
		player_list = []
		import gc
		for obj in gc.get_objects():
			if isinstance(obj, BoardSpace):
				if obj.ownership == self.activeplayer:
					player_list.append(obj.name)
		diag = False
		d = 0
		c = 0		
		if 'A1' in player_list:
			d += 1
		else:
			pass
		if 'B2' in player_list:
			d += 1
		else:
			pass
		if 'C3' in player_list:
			d += 1
		if d == 3:	
			diag = True
		else: 
			pass		
		if 'A3' in player_list:
			c += 1
		else:
			pass
		if 'B2' in player_list:
			c += 1
		else:
			pass
		if 'C1' in player_list:
			c += 1
		if c == 3:
			diag = True
		else:
			pass
		return diag
		
		
class Admin(object): #choosing between viewing scores and playing a game
	def __init__(self, name, opt_dict, playing):
		self.name = name
		self.opt_dict = {}
		self.playing = True
	
	def set_options(self):
		self.opt_dict = {
			1: ['Play a game!', gameflow.flow],
			2: ['View the scoreboard', scoreboard.display_scoreboard],
			3: ['Exit', self.done]
			}
			
	def start(self):
		clear()
		for n in range(3):
			print ('*'*60)
		print 'WELCOME TO THE GAME!'
		for s in self.opt_dict:
			print str(s) + ' ' + self.opt_dict[s][0] 
		choosing = True
		while choosing:
			choice = int(raw_input('Please enter your choice \n'))
			try:
				if choice in self.opt_dict:
					self.opt_dict[choice][1]()
					choosing = False
				else:
					print 'Please only enter a menu option number'
			except ValueError:
				print 'Please only enter a menu option number'
				
	def done(self):
		self.playing = False
		
class Flow(object):
	def __init__(self, name):
		self.name = name

	def flow(self): #the flow of all modules and gameplay inside main
		playing = True
		while playing:
			win = gameplay.play()
			tie = gameplay.tie_check()
			if win == True:
				playing = False
			elif tie == True:
				board.draw_board() #shows final move in event of a tie
				gameplay.activeplayer = 'Tie'
				print 'Tie!'
				playing = False
			else:
				playing = True
		scoreboard.update()
		gameplay.reset_boardspaces()
		
class SaveResults(object):
	def __init__(self, name):
		self.name = name
		
	def save_results(self):
		from datetime import date
		today = date.today()
		keep = open("ttt_results.txt", "a")
		keep.write(str(today) + ',' 'p1,' + str(p1.name) + ',' + str(scoreboard.p1) + ',p2,' +  str(p2.name) + ',' + str(scoreboard.p2) + 'Ties,' + str(scoreboard.tie))
		keep.write('\n')
		keep.close

save_to_file = SaveResults('Save Results')
admin = Admin('Admin', {}, True)
gameflow = Flow('Gameflow')
scoreboard = Scoreboard('Scoreboard', {}, 0, 0, 0, 0)
p1 = Player('Name1', True, 0)
p2 = Player('Name2', False, 0)
board = Board('board', 10)
A1 = BoardSpace('A1', 1, 'A', 'x', 'none')
A2 = BoardSpace('A2', 2, 'A', 'o', 'none')
A3 = BoardSpace('A3', 3, 'A', 'x', 'none')
B1 = BoardSpace('B1', 1, 'B', 'x', 'none')
B2 = BoardSpace('B2', 2, 'B', 'o', 'none')
B3 = BoardSpace('B3', 3, 'B', 'x', 'none')
C1 = BoardSpace('C1', 1, 'C', 'x', 'none')
C2 = BoardSpace('C2', 2, 'C', 'o', 'none')
C3 = BoardSpace('C3', 3, 'C', 'x', 'none')
rowA = BoardRow('rowA', 'A', 10, 10, 5, 0)
rowB = BoardRow('rowB', 'B', 10, 10, 5, 0)
rowC = BoardRow('rowC', 'C', 10, 10, 5, 0)
gameplay = Gameplay('Gameplay', 0, 'p1', '')
set_state_dict = {
	'A1': [A1.set_state],
	'A2': [A2.set_state],
	'A3': [A3.set_state],
	'B1': [B1.set_state],
	'B2': [B2.set_state],
	'B3': [B3.set_state],
	'C1': [C1.set_state],
	'C2': [C2.set_state],
	'C3': [C3.set_state]
	}

def Main():
	admin.set_options()
	gameplay.startup()
	stop = False
	while not stop:
		admin.start()
		#clear()
		if admin.playing == False:
			stop = True
		else:
			print 'Would you like to continue playing? (Y/N)'
			again = raw_input()
			if again.upper() == 'Y':
				stop = False
			if again.upper() == 'N':
				stop = True
			else:
				print 'Please only enter Y or N'
	save_to_file.save_results()
	print 'Goodbye!'

Main()
	
	

	

	
