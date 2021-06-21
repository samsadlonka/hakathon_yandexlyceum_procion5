import json
from math import sqrt


def make_draft(data: dict) -> dict:
    draft = {}
    # TODO: Make draft here
    return draft


def make_turn(data: dict) -> dict:
    battle_output = {
        'Message': f"I have {len(data['My'])} ships and move to center of galaxy and shoot",
        'UserCommands': []
    }
    for ship in data['My']:
        x_our, y_our, z_our = list(map(lambda coor_our: int(coor_our), ship['Position'].split('/')))
        distance_to_enemy_ship = []
        for ship_opponent in data['Opponent']:
            x, y, z = list(map(lambda coor: int(coor), ship_opponent["Position"].split('/')))
            distance_to_enemy_ship.append({
                'coor_opponent': f'{x}/{y}/{z}',
                'distance': sqrt((x - x_our) ** 2 + (y - y_our) ** 2 + (z - z_our) ** 2)
            })
        distance_to_enemy_ship.sort(key=lambda obj: obj['distance'])


        attack_was, move_was = False, False


        for distance in distance_to_enemy_ship:
            guns = [x for x in ship['Equipment'] if x['Type'] == 1]
            if guns and distance['distance'] <= guns[0]['Radius'] and not (attack_was):
                gun = guns[0]
                battle_output['UserCommands'].append({
                    "Command": "ATTACK",
                    "Parameters": {
                        'Id': ship['Id'],
                        'Name': gun['Name'],
                        'Target': distance['coor_opponent']
                    }
                })
                attack_was = True
            if not guns:
                battle_output['UserCommands'].append({
                    "Command": "MOVE",
                    "Parameters": {
                        'Id': ship['Id'],
                        'Target': distance['coor_opponent']
                    }
                })
                break
            elif distance['distance'] > guns[0]['Radius']:
                battle_output['UserCommands'].append({
                    "Command": "MOVE",
                    "Parameters": {
                        'Id': ship['Id'],
                        'Target': distance['coor_opponent']
                    }
                })
                break
    return battle_output


def play_game():
    while True:
        raw_line = input()
        line = json.loads(raw_line)
        if 'PlayerId' in line:
            print(json.dumps(make_draft(line), ensure_ascii=False))
        elif 'My' in line:
            print(json.dumps(make_turn(line), ensure_ascii=False))


if __name__ == '__main__':
    play_game()