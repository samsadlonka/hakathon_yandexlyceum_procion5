import json
from math import sqrt
from copy import deepcopy


def make_draft(data: dict) -> dict:
    draft = {}
    # TODO: Make draft here
    return draft


# --------------- Вспомогательные функции ------------------------ #

def give_num_from_str(coor: str) -> list:
    return list(map(lambda x: int(x), coor.split('/')))


def give_str_from_num(coor: list) -> str:
    return '/'.join(list(map(lambda x: str(x), coor)))


def give_distances_to_other_points(one_point, points):
    """Возвращает расстояния от одной точки до нескольких других"""
    x_our, y_our, z_our = give_num_from_str(one_point)
    distances_to_points = []
    for point in points:
        x, y, z = point
        distances_to_points.append({
            'coor_opponent': [x, y, z],
            'distance': sqrt((x - x_our) ** 2 + (y - y_our) ** 2 + (z - z_our) ** 2)
        })
    return distances_to_points


def found_nearest_goal(our_ship_point, ships_enemy):
    """Возвращает ближайшую цель для одного из наших кораблей"""
    ships_enemy = [give_num_from_str(ship['Position']) for ship in ships_enemy]
    distances_to_enemy_ship = give_distances_to_other_points(our_ship_point, ships_enemy)
    return min(distances_to_enemy_ship, key=lambda x: x['distance'])


def give_overall_goal_for_all_our_ships(our_ships, enemy_ships):
    """Возвращает цель, которая была у большинства ближней"""
    nearest_goals = [give_str_from_num(found_nearest_goal(ship['Position'], enemy_ships)['coor_opponent'])
                     for ship in our_ships]
    return give_num_from_str(max(set(nearest_goals), key=nearest_goals.count))


def give_area_without_enemy(goal, enemy_ships):
    """Определяет область, в которой меньше всего противников"""
    area = []
    for index, coordinate in enumerate(goal):
        less_coordinate, more_coordinate = 0, 0
        for ship in enemy_ships:
            ship_format_num = give_num_from_str(ship['Position'])
            if ship_format_num[index] < coordinate:
                less_coordinate += 1
            else:
                more_coordinate += 1
        if less_coordinate < more_coordinate and coordinate > 3:
            area.append((-1, coordinate))
        else:
            area.append((coordinate, 30))
    return area


def give_points_next_to_target(area, coor_target):
    LOCATION_POINTS = [(1, 1, 1), (-4, 0, 0), (1, 1, 3), (-4, 1, 3), (1, 0, -2)]
    """Получаем все точки, до которых нужно будет дойти нашим кораблям"""
    coor_target_list_of_num = give_num_from_str(coor_target)
    sign_x_y_z = [1, 1, 1]  # 1 значит +
    for index, area_vector in enumerate(area):
        if area_vector[0] != -1:
            coor_target_list_of_num[index] += 1  # Изменяем точку, от которой будем отталкиваться и
            sign_x_y_z[index] -= 1               # находить другие точки

    points_next_to_target = []
    # С помощью измененной точки(то есть мы изменили ship['Position']) находим все точки вокруг нее
    for point in LOCATION_POINTS:
        copy_target_point = coor_target_list_of_num.copy()
        for index, vector in enumerate(point):
            if sign_x_y_z[index] == 1:
                copy_target_point[index] += vector
            else:
                copy_target_point[index] -= vector
        points_next_to_target.append(copy_target_point)

    return points_next_to_target


def distribution_points_our_ships(ships_our, points_next_to_target):
    """Распределение полученных точек между нашими кораблями, чтобы они не сталкивались"""
    sum_distances = []
    for index, ship in enumerate(ships_our):
        distances = give_distances_to_other_points(ship['Position'], points_next_to_target)
        distances_format = [distance['distance'] for distance in distances]
        sum_distances.append((sum(distances_format), ship, distances))

    sum_distances.sort(key=lambda x: x[0])

    distributed_points = []

    for _, ship, distances in sum_distances:
        occupied_points = [elem[1] for elem in distributed_points]
        distances = list(filter(lambda x: x['coor_opponent'] not in occupied_points, distances))
        distributed_points.append([ship['Id'],
                                   max(distances, key=lambda x: x['distance'])['coor_opponent']])

    distributed_points = [[points[0], give_str_from_num(points[1])] for points in distributed_points]
    return distributed_points


# -------------- Вспомогательные функции END --------------------- #


def make_turn(data: dict, target) -> dict:
    battle_output = {
        'Message': f"{target}",
        'UserCommands': []
    }

    if target == '' or target not in [ship_enemy['Position'] for ship_enemy in data['Opponent']]:
        target = give_str_from_num(
            give_overall_goal_for_all_our_ships(data['My'], data['Opponent']))

    free_area = give_area_without_enemy(give_num_from_str(target), data['Opponent'])
    points_next_target = give_points_next_to_target(free_area, target)
    # Важная переменная, в ней хранятся распределенные точки, куда нужно идти кораблям своим
    distributed_points = distribution_points_our_ships(data['My'], points_next_target)

    distances_to_target = give_distances_to_other_points(target,
                                                         [give_num_from_str(ship['Position']) for ship in data['My']])

    count_ships_reaching_target = 0
    for distance in distances_to_target:
        distance_coor = give_str_from_num(distance['coor_opponent'])
        ship = list(filter(lambda x: x['Position'] == distance_coor, data['My']))[0]
        guns = [x for x in ship['Equipment'] if x['Type'] == 1]
        if distance['distance'] < 7:
            count_ships_reaching_target += 1
        if distance['distance'] < 7 and guns:
            gun = guns[0]
            battle_output['UserCommands'].append({
                "Command": "ATTACK",
                "Parameters": {
                    'Id': ship['Id'],
                    'Name': gun['Name'],
                    'Target': target  # Стреляет просто по одной точки, изменить потом
                }
            })

    if count_ships_reaching_target == len(data['My']):
        copy_distributed_points = deepcopy(distributed_points)
        for index, points in enumerate(copy_distributed_points):
            elem_copy = distributed_points[index][1]
            distributed_points[index - 1][1] = elem_copy

    for points in distributed_points:
        battle_output['UserCommands'].append({
            "Command": "MOVE",
            "Parameters": {
                'Id': points[0],
                'Target': points[1]
            }
        })

    battle_output['Message'] = target

    """Сделать так чтобы когда у всех было расстояние меньше 5, все стреляли, а потом менялись позициями
       Не стрелть ни в кого кроме цели. (Только сделать провекру того, что вдруг мы досатаем до кого-то и
       не достаем до цели, тогда можно стрелять, но опасаясь попасть в своих.)"""
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
    target = ''
    first = True
    while True:
        raw_line = input()
        line = json.loads(raw_line)
        if 'PlayerId' in line:
            print(json.dumps(make_draft(line), ensure_ascii=False))
        elif 'My' in line and first:
            print(json.dumps(make_first_turn(line), ensure_ascii=False))
            first = False
        elif 'My' in line:
            responce = make_turn(line, target)
            target = responce['Message']
            print(json.dumps(responce, ensure_ascii=False))


if __name__ == '__main__':
    play_game()
