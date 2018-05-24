import math
import heapq

i=0
para = "crow"

cells  = {}

start  =None
goal  = None
#num_cells = None
# A* variables
# Python's built-in heapq module uses a plain ol' list as it's underlying data structure. Actually,
# heapq is just a set of functions that can be called on a list. Such as:
# 
#     heapify(list)
#     heappop(list)
#     heappush(list,item)
# 
# So open_list is the list that we'll use to store the f_scores of all the opened cells. The cell with the lowest
# f_score is of our highest priority, so when we call heapify(open_list) this will order the list so that the lowest
# score is the first element.

open_list = []
# There's an issue with this, as you may have noticed. We're only keeping track of the f_scores of all the opened cells
# in open_list. When we retreive the lowest f_score, how do we know which cell is this? pq_dict is a ditionary for our
# priority queue. 

# When we pop the highest priority f_score out of open_list, we use this as a key to retreive the actual cell
# identifier from pq_dict

pq_dict = {}   # our priority queue of opened cells' f_scores
			 
closed_list = {}    # A dictionary of closed cells

def init_cell(recMapInfo):
	global num_cells
	#global cells
	cells = {}
	map_info = recMapInfo["map"]

	map_x = map_info["x"]
	map_y = map_info["y"]
	map_z = map_info["z"]
	#cell_size = 1
	num_cells = map_x
	for x in range(num_cells):
		for y in range(num_cells):
			cells[(x,y)]= { 'state':None,   # None, Wall, Goal, Start Are the possible states. None is walkable 
							'f_score':None, # f() = g() + h() This is used to determine next cell to process
							'h_score':None, # The heuristic score, We use straight-line distance: sqrt((x1-x0)^2 + (y1-y0)^2)
							'g_score':None, # The cost to arrive to this cell, from the start cell
							'parent':None}  # In order to walk the found path, keep track of how we arrived to each cell
	return cells

def init_map(recMapInfo,hight):
	global cells
	#cells = {}

	cells = init_cell(recMapInfo)

	buildings = recMapInfo["building"]
	for building in buildings:
		x = building["x"]
		y = building["y"]
		l = building["l"]
		w = building["w"]
		h = building["h"]
		if h>=hight:
			for i in range(x,x+l):
				for j in range(y,y+w):
					cells[(i,j)]["state"] = "Wall"
	return cells

def init_start_goal(cell_start,cell_goal):
	#cells = map_cells
	global start,goal
	start  =cell_start
	goal = cell_goal
	cells[start]["state"] = "Start"
	cells[goal]['state'] = "Goal"
	#return cells

def calc_f(node):
	cells[node]['f_score'] = cells[node]['h_score'] + cells[node]['g_score']

def onBoard(node):
	x, y = node
	return x >= 0 and x < num_cells and y >= 0 and y < num_cells

# Calculate the heuristic score, straight line distance between two points:
# You'll notice I multiply by 10. This is because of how I keep track of the g_score, which you'll see later
# but I'll explain now:
#
# To simplify the calculations of the g_score, if we move in an orthoganal direction, we consider the cost
# of this move to be 10, and not 1. We do this because of the cost of a diagonal move. Typically this would
# be the squareroot of 2 = 1.4142..
#
# To decrease the number of essentially useless computations, we round this to 1.4...and why deal with decimals?
# So we multiply that by 10 to get a cost of 14 to move diagonal and 10 to move orthoganal.

def calc_h(node,para = "crow"):
	#global heuristic
	x1, y1 = goal
	x0, y0 = node
	if para == 'manhattan':
		cells[node]['h_score'] = (abs(x1-x0)+abs(y1-y0))*10#
	elif para == 'crow':
		cells[node]['h_score'] = math.sqrt( (x1-x0)**2 + (y1-y0)**2 )*10
	else:
		cells[node]['h_score'] = 0


# Return a list of adjacent orthoganal walkable cells 

def orthoganals(current):
	x, y = current
	
	N = x-1, y
	E = x, y+1
	S = x+1, y
	W = x, y-1
	
	directions = [N, E, S, W]
	return [x for x in directions if onBoard(x) and cells[x]['state'] != 'Wall' and not x in closed_list]



# Check if diag is blocked by a wall, making it unwalkable from current

def blocked_diagnol(current,diag):
	x, y = current
	
	N = x-1, y
	E = x, y+1
	S = x+1, y
	W = x, y-1
	NE = x-1, y+1
	SE = x+1, y+1
	SW = x+1, y-1
	NW = x-1, y-1
	
	if diag == NE:
		return cells[N]['state'] == 'Wall' or cells[E]['state'] == 'Wall'
	elif diag == SE:
		return cells[S]['state'] == 'Wall' or cells[E]['state'] == 'Wall'
	elif diag == SW:
		return cells[S]['state'] == 'Wall' or cells[W]['state'] == 'Wall'
	elif diag == NW:
		return cells[N]['state'] == 'Wall' or cells[W]['state'] == 'Wall'
	else:
		return False # Technically, you've done goofed if you arrive here.

# Return a list of adjacent diagonal walkable cells

def diagonals(current):

	res = []
	x, y = current
	
	NE = x-1, y+1
	SE = x+1, y+1
	SW = x+1, y-1
	NW = x-1, y-1
	
	directions = [NE, SE, SW, NW]

	#for x in directions:
		#print("cells:",len(cells))
		#print("celss-type:",type(cells))
		#if onBoard(x) :#and cells[x]['state']!='Wall' :#and x not in closed_list :#and not blocked_diagnol(current,x):
		#	res.append(x)
	#return res
	return [x for x in directions if onBoard(x) and cells[x]['state'] != 'Wall' and not x in closed_list and not blocked_diagnol(current,x)]



# Update a child node with information from parent, such as g_score and the parent's coords

def update_child(parent, child, cost_to_travel):
	cells[child]['g_score'] = cells[parent]['g_score'] + cost_to_travel
	cells[child]['parent'] = parent

def find_next_node(coord):
	node  = cells[coord]['parent']
	print(node)
	if node!=None:
		if cells[node]['parent'] != None:
		
			find_next_node(cells[coord]['parent'])
		else:
			return node
	else:
		return coord
def process_node(coord):
	global i
	#i = 0
	i+=1
	print(i)
	global goal, open_list, closed_list, pq_dict
	if coord == goal:
		print("Cost %d\n" % cells[goal]['g_score'])
		#unwind_path(cells[goal]['parent'], slow)
		return find_next_node(goal)
		
	# l will be a list of walkable adjacents that we've found a new shortest path to
	l = [] 
	
	# Check all of the diagnols for walkable cells, that we've found a new shortest path to
	for x in diagonals(coord):
		# If x hasn't been visited before
		if cells[x]['g_score'] == None:
			update_child(coord, x, cost_to_travel=14)
			l.append(x)
		# Else if we've found a faster route to x
		elif cells[x]['g_score'] > cells[coord]['g_score'] + 14:
			update_child(coord, x, cost_to_travel=14)
			l.append(x)
	
	for x in orthoganals(coord):
		# If x hasn't been visited before
		if cells[x]['g_score'] == None:
			update_child(coord, x, cost_to_travel=10)
			l.append(x)
		# Else if we've found a faster route to x
		elif cells[x]['g_score'] > cells[coord]['g_score'] + 10:
			update_child(coord, x, cost_to_travel=10)
			l.append(x)
	
	
		# If we found a shorter path to x
		# Then we remove the old f_score from the heap and dictionary
		if cells[x]['f_score'] in pq_dict:
			if len(pq_dict[cells[x]['f_score']]) > 1:
				pq_dict[cells[x]['f_score']].remove(x)
			else:
				pq_dict.pop(cells[x]['f_score'])
			open_list.remove(cells[x]['f_score'])
		# Update x with the new f and h score (technically don't need to do h if already calculated)
		calc_h(x)
		calc_f(x)
		# Add f to heap and dictionary
		open_list.append(cells[x]['f_score'])
		if cells[x]['f_score'] in pq_dict:
			pq_dict[cells[x]['f_score']].append(x)
		else:
			pq_dict[cells[x]['f_score']] = [x]
	
	#print(l)
	heapq.heapify(open_list)
	
	
	if len(open_list) == 0:
		print('NO POSSIBLE PATH!')
		return
	f = heapq.heappop(open_list)
	if len(pq_dict[f]) > 1:
		node = pq_dict[f].pop()
	else:
		node = pq_dict.pop(f)[0]
	
	heapq.heapify(open_list)
	closed_list[node]=True

	process_node(node)


# Start the search for the shortest path from start to goal

def find_path(start,goal):
	if start != None and goal != None:
		#print(type(start))
		#print(type(cells[start]))
		cells[start]['g_score'] = 0
		calc_h(start)
		calc_f(start)
		
		closed_list[start]=True
		node = process_node(start)
		return node




if __name__=="__main__":
	recMapInfo = {
	"map": {         
		"x": 100,  
		"y": 100,
		"z": 100
	},
	"parking": {    
		"x": 0,
		"y": 0
	},
	"h_low": 60,    
	"h_high": 100,  
	"building": [    
					
					
		{ "x": 10, "y": 10, "l": 10, "w": 10, "h": 80 },
		{ "x": 40, "y": 40, "l": 10, "w": 10, "h": 60 }

	],
	 
	"fog": [
		{ "x": 60, "y": 60, "l": 10, "w": 10, "b": 55, "t": 90 },
		{ "x": 35, "y": 47, "l": 15, "w": 20, "b": 60, "t": 100 }
	],
	"init_UAV": [
		{ "no": 0, "x":0,"y":0,"z":0,"load_weight": 100,"type": "F1","status": 0, "goods_no":-1},
		{ "no": 1, "x":0,"y":0,"z":0,"load_weight": 20 ,"type": "F3","status": 0, "goods_no":-1},
		{ "no": 2, "x":0,"y":0,"z":0,"load_weight": 20 ,"type": "F3","status": 0, "goods_no":-1}
	],
	"UAV_price": [
		{ "type": "F1","load_weight": 100,"value": 300 },
		{ "type": "F2","load_weight": 50, "value": 200 },
		{ "type": "F3","load_weight": 20, "value": 100 },
		{ "type": "F4","load_weight": 30, "value": 150 },
		{ "type": "F5","load_weight": 360, "value": 400 }
	],

	} 
	
	cells = init_map(recMapInfo,25)
	#print(cells[(12,12)])
	init_start_goal((2,2),(9,9))
	print(len(cells))
	#print("num_cells:",num_cells)
	#print(start)
	#start  = (2,2)
	#goal = (99,99)
	#print(cells[(2,2)])
	print("next_node:",find_path(start,goal))



