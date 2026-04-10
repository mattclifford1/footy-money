import sys
import math
import configparser


def _load_aliases(path='aliases.ini'):
    cfg = configparser.ConfigParser()
    cfg.read(path)  # silent no-op if file missing
    if 'aliases' not in cfg:
        return {}
    return {alias: canonical for alias, canonical in cfg['aliases'].items()}


def _load_rounding(path='config.ini'):
    cfg = configparser.ConfigParser()
    cfg.read(path)
    try:
        mode = cfg['rounding']['mode'].strip()
    except KeyError:
        mode = '2dp'
    return mode if mode in ('2dp', '0.1', '0.2', '0.5') else '2dp'


def _round_up(x, mode):
    if mode == '0.1':
        return math.ceil(x * 10) / 10
    elif mode == '0.2':
        return math.ceil(x * 5) / 5
    elif mode == '0.5':
        return math.ceil(x * 2) / 2
    return math.ceil(x * 100) / 100


def calc_money(lines):
    aliases = _load_aliases()
    rounding_mode = _load_rounding()

    
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
                # apply aliases and normalise case
                player = aliases.get(player.lower(), player).capitalize()
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
    per_game = _round_up(per_game, rounding_mode)
    return_txt += f'per game cost: £{per_game}\n'
    dict_values = 0
    for player, num in player_counts.items():
        add_white = ' '*(max_len_name-len(player))
        cost = num*per_game
        cost = _round_up(cost, rounding_mode)
        games_text = 'games' if num > 1 else 'game '
        return_txt += f'{player}{add_white}: {num} {games_text} = £{cost}\n'
        dict_values += cost
    return_txt += '===============\n\n\n'

    return_txt += 'Sanity checks:\n'
    return_txt += f'players: {total_players} (names) {total_players_txt} (numbers)\n'
    return_txt += f'rough money: {sessions*80} (for 7 a side pitch @ £80)\n'
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
