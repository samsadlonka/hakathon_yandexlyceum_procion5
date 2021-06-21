import json
from math import sqrt


def make_draft(data: dict) -> dict:
    draft = {}
    # TODO: Make draft here
    return draft


def give_num_from_str(coor: str) -> list:
    return list(map(lambda x: int(x), coor.split('/')))


def give_str_from_num(coor: list) -> str:
    return '/'.join(list(map(lambda x: str(x), coor)))


def append_coor_our(side_list: list, step: int, ship_opp: str, vektor: int) -> None:
    pos_op = give_num_from_str(ship_opp)
    pos_op[vektor] += step
    side_list.append(pos_op)


"""def distribute_near_enemy_side(position_our_ship_list, index_1, index_2, my_ships):
    x_coor = [(position_our_ship_list[index_1][0], index_1), (position_our_ship_list[index_2][0], index_2),
              (int(my_ships[index_1]['Position'][0]), index_1), (int(my_ships[index_2]['Position'][0]), index_2)]
    index_min, index_max = x_coor.index(min(x_coor, key=lambda x: x[0])), x_coor.index(max(x_coor, key=lambda x: x[0]))
    if not(index_min == 0 and index_max == 1) and not(index_min == 2 and index_max == 3):
        if [x_coor[index_min][1]] == x_coor[index_max][1]:
            position_our_ship_list[index_1], position_our_ship_list[index_2] = position_our_ship_list[index_2], \
                                                                                   position_our_ship_list[index_1]
            return 'Ship turns'
        return ''
    return ''
"""


def make_turn(data: dict) -> dict:
    battle_output = {
        'Message': f"I have {len(data['My'])} ships and move to center of galaxy and shoot \n",
        'UserCommands': []
    }
    x_min, x_max, y_min, y_max, z_min, z_max = 30, 0, 30, 0, 30, 0
    y_min_side_ship, y_max_side_ship, z_max_side_ship = [], [], []
    for ship_opponent in data['Opponent']:
        x, y, z = list(map(lambda coor: int(coor), ship_opponent["Position"].split('/')))
        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x
        if y < y_min:
            y_min = y
            append_coor_our(y_min_side_ship, -3, ship_opponent['Position'], 1)
        elif y == y_min:
            append_coor_our(y_min_side_ship, -3, ship_opponent['Position'], 1)
        if y > y_max:
            y_max = y
            append_coor_our(y_max_side_ship, +3, ship_opponent['Position'], 1)
        elif y == y_max:
            append_coor_our(y_max_side_ship, +3, ship_opponent['Position'], 1)
        if z < z_min:
            z_min = z
        if z > z_max:
            z_max = z
            append_coor_our(z_max_side_ship, +4, ship_opponent['Position'], 2)
        elif z == z_max:
            append_coor_our(z_max_side_ship, +4, ship_opponent['Position'], 2)

    position_our_ship = [y_max_side_ship[0]]
    if len(y_max_side_ship) > 1:
        position_our_ship.append(y_max_side_ship[-1])
    else:
        ship_with_margin = y_max_side_ship[0]
        ship_with_margin[0] += 3
        position_our_ship.append(ship_with_margin)

    position_our_ship[0], position_our_ship[1] = position_our_ship[1], position_our_ship[0]

    position_our_ship.append(y_min_side_ship[0])
    if len(y_min_side_ship) > 1:
        position_our_ship.append(y_min_side_ship[-1])
    else:
        ship_with_margin = y_max_side_ship[0]
        ship_with_margin[0] += 3
        position_our_ship.append(ship_with_margin)

    position_our_ship[2], position_our_ship[3] = position_our_ship[3], position_our_ship[2]

    position_our_ship.append(z_max_side_ship[0])

    for index, ship in enumerate(data['My']):
        x_our, y_our, z_our = give_num_from_str(ship['Position'])
        battle_output['UserCommands'].append({
            "Command": "MOVE",
            "Parameters": {
                'Id': ship['Id'],
                'Target': give_str_from_num(position_our_ship[index])
            }
        })
        # Ближайшая цель для выстрела, потом исправить
        distance_to_enemy_ship = []
        for ship_opponent in data['Opponent']:
            x, y, z = list(map(lambda coor: int(coor), ship_opponent["Position"].split('/')))
            distance_to_enemy_ship.append({
                'coor_opponent': f'{x}/{y}/{z}',
                'distance': sqrt((x - x_our) ** 2 + (y - y_our) ** 2 + (z - z_our) ** 2)
            })
        distance_to_enemy_ship.sort(key=lambda obj: obj['distance'])
        guns = [x for x in ship['Equipment'] if x['Type'] == 1]
        if guns:
            gun = guns[0]
            battle_output['UserCommands'].append({
                "Command": "ATTACK",
                "Parameters": {
                    'Id': ship['Id'],
                    'Name': gun['Name'],
                    'Target': distance_to_enemy_ship[0]['coor_opponent']
                }
            })
    return battle_output


def make_first_turn(data: dict) -> dict:
    battle_output = {
        'Message': f"I have {len(data['My'])} ships and move to center of galaxy and shoot \n",
        'UserCommands': []
    }
    i = 2
    for ship in data['My'][1:]:
        if data['My'][0]['Position'] == '0/0/0':
            battle_output['UserCommands'].append({
                "Command": "MOVE",
                "Parameters": {
                    'Id': ship['Id'],
                    'Target': str(int(ship['Position'].split('/')[0]) + i) + '/' +
                              '/'.join(ship['Position'].split('/')[1:])
                }
            })
        else:
            battle_output['UserCommands'].append({
                "Command": "MOVE",
                "Parameters": {
                    'Id': ship['Id'],
                    'Target': str(int(ship['Position'].split('/')[0]) - i) + '/' +
                              '/'.join(ship['Position'].split('/')[1:])
                }
            })
        i += 1
    return battle_output


def play_game():
    first = True
    while True:
        line = json.loads(input())
        if 'PlayerId' in line:
            print(json.dumps(make_draft(line), ensure_ascii=False))
        elif 'My' in line and first:
            print(json.dumps(make_first_turn(line), ensure_ascii=False))
            first = False
        elif 'My' in line:
            print(json.dumps(make_turn(line), ensure_ascii=False))


if __name__ == '__main__':
    play_game()
