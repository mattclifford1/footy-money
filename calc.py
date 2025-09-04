import sys
import math


def calc_money(lines):
    
    total_players = 0
    total_players_txt = 0
    player_counts = {}
    total_money = 0
    sessions = 0
    max_len_name = 0
    return_txt = ''
    print(lines)
    for line in lines:
        print(line)
        if line == '' or line == '\n' or line == ' ':
            continue
        if line[0] == '#':
            continue
        if line[0].isnumeric():  # money line
            players_num_given = 0
            split_info = line.split(' ')
            print('=============================')
            print(line)
            print(split_info)
            print('=============================')
            return_txt += f'{split_info[0]} {split_info[1]}\n'
            # remove £
            try:
                money = int(split_info[2][1:])
            except ValueError:  # windows read some characters differently
                money = int(split_info[2][2:])
            total_money += money
            total_players_txt += int(split_info[4])
            players_num_given += int(split_info[4])

        else:   # player line
            players_in_line = 0
            return_txt += f'{line} \n'
            players = line.split(' ')
            for player in players:
                player = player.capitalize()
                if player in ['', ' ', '\n']:
                    continue
                elif player in player_counts.keys():
                    player_counts[player] += 1
                else:
                    player_counts[player] = 1
                    max_len_name = max(max_len_name, len(player))
                total_players += 1
                players_in_line += 1
            sessions += 1

            # finshed the players line so show quick sanity check
            return_txt += f'players in line: {players_in_line} ({players_num_given} stated)\n\n'

    per_game = total_money/total_players
    player_counts = {k: v for k, v in sorted(
        player_counts.items(), key=lambda item: item[1], reverse=True)}

    return_txt += '===============\n'
    return_txt += f'total sessions: {sessions}\n'
    return_txt += f'total cost   : £{total_money}\n'
    per_game = math.ceil(per_game*100)/100
    return_txt += f'per game cost: £{per_game}\n'
    dict_values = 0
    for player, num in player_counts.items():
        add_white = ' '*(max_len_name-len(player))
        cost = num*per_game
        cost = math.ceil(cost*100)/100
        games_text = 'games' if num > 1 else 'game '
        return_txt += f'{player}{add_white}: {num} {games_text} = £{cost}\n'
        dict_values += cost
    return_txt += '===============\n\n\n'

    return_txt += 'Sanity checks:\n'
    return_txt += f'players: {total_players} (names) {total_players_txt} (numbers)\n'
    return_txt += f'rough money: {sessions*75} (for 7 a side pitch)\n'
    return_txt += f'added: {dict_values}\n'
    return_txt += f'num sessions: {sessions}'

    return return_txt


if __name__ == "__main__":
    if len(sys.argv) == 1:
        file = 'fixtures-all-2024.txt'
    else:
        file = sys.argv[1]

    with open(file) as f:
        lines = [line.rstrip('\n') for line in f]

    txt = calc_money(lines)

    print(txt)
