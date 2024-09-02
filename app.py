import math
import gradio as gr


def calc_money(footy_notes):
    lines = footy_notes.split('\n')
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

        else:   # player line
            return_txt += f'{line} \n\n'
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
        return_txt += f'{player}{add_white}: {num} games = £{cost}\n'
        dict_values += cost
    return_txt += '===============\n\n\n'

    return_txt += 'Sanity checks:\n'
    return_txt += f'players: {total_players} {total_players_txt}\n'
    return_txt += f'rough money: {sessions*71} (for 7 a side pitch)\n'
    return_txt += f'added: {dict_values}\n'

    return return_txt



if __name__ == "__main__":
    with open('info.txt') as f:
        default = f.read()
    input = gr.Textbox(value=default, label="Enter footy notes")
    demo = gr.Interface(fn=calc_money, inputs=input, outputs="textbox")
    demo.launch()
