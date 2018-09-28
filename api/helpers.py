from operator import itemgetter


def sort_by_goals_scored(table):
		final_table = []
		for x in range(0, len(table)):
			if x >= len(final_table):
				level_on_goal_difference = []
				addAmount = 1
				check = True
				while check:
					try:
						if table[x]['goal_difference'] == table[x+addAmount]['goal_difference']:
							if addAmount == 1:
								level_on_goal_difference.append(table[x])
							level_on_goal_difference.append(table[x+addAmount])
							addAmount += 1
						else:
							check = False
					except IndexError:
						check = False
					finally:
						if not check:
							if len(level_on_goal_difference) > 0:
								fixed = sorted(level_on_goal_difference, key=itemgetter('goals_for'), reverse=True)
								final_table.extend(fixed)
							else:
								final_table.append(table[x])
		return final_table

			
def sort_by_goal_difference(table):
	final_table = []
	for x in range(0, len(table)):
		if x >= len(final_table):
			level_on_points = []
			addAmount = 1
			check = True
			while check:
				try:
					if table[x]['points'] == table[x+addAmount]['points']:
						if addAmount == 1:
							level_on_points.append(table[x])
						level_on_points.append(table[x+addAmount])
						addAmount += 1
					else:
						check = False
				except IndexError:
					check = False
				finally:
					if not check:
						if len(level_on_points) > 0:
							fixed = sorted(level_on_points, key=itemgetter('goal_difference'), reverse=True)
							fixed = sort_by_goals_scored(fixed)
							final_table.extend(fixed)
						else:
							final_table.append(table[x])
	return final_table
