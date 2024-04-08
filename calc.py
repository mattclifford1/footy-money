import sys
import math

if len(sys.argv) == 1:
    file = 'fixtures-2-2024.txt'
else:
    file = sys.argv[1]

with open(file) as f:
    lines = [line.rstrip('\n') for line in f]
   
total_players = 0
total_players_txt = 0
player_counts = {}
total_money = 0
sessions = 0
max_len_name = 0

for line in lines:
    if line == '':
        continue
    if line[0].isnumeric():  # money line
        split_info = line.split(' ')
        total_money += int(split_info[2][1:]) # remove £
        total_players_txt += int(split_info[4])

    else:   # player line 
        
        players = line.split(' ')
        for player in players:
            if player in ['', ' ', '\n']:
                continue
            elif player in player_counts.keys():
                player_counts[player] += 1
            else:
                player_counts[player] = 1
                max_len_name = max(max_len_name, len(player))
            total_players += 1
        sessions += 1

per_game = total_money/total_players
player_counts = {k: v for k, v in sorted(player_counts.items(), key=lambda item: item[1], reverse=True)}

print('===============')
print(f'total sessions: {sessions}')
print(f'total cost   : £{total_money}')
per_game = math.ceil(per_game*100)/100
print(f'per game cost: £{per_game}')
dict_values = 0
for player, num in player_counts.items():
    add_white = ' '*(max_len_name-len(player))
    cost = num*per_game
    cost = math.ceil(cost*100)/100
    print(f'{player}{add_white}: {num} games = £{cost}')
    dict_values += cost
print('===============\n\n') 
    
    
print('Sanity checks:')
print('players: ', total_players, total_players_txt)
print(f'rough money: {sessions*71}')
print(f'added: {dict_values}')
              

