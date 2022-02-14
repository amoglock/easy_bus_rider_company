import json
import re

errors = {"bus_id": 0, "stop_id": 0, "stop_name": 0, "next_stop": 0, "stop_type": 0, "a_time": 0}
# bus_info = json.loads(input())
with open("example.txt", "r") as bus_info_1:
    bus_info = json.load(bus_info_1)


my_list, stops, all_stop_type,  = [], [], []
start_stops, transfer_stops, finish_stops, on_demand_stops = set(), set(), set(), set()


def bus_line_info():
    for line in bus_info:
        my_list.append(line['bus_id'])
        stops.append(line['stop_name'])
        all_stop_type.append(line['stop_type'])
    print('Line names and number of stops:')
    for number in set(my_list):
        print(f'bus_id: {number}, stops: {my_list.count(number)}')
    for line_number in set(my_list):
        stop_type_list = []
        for line in bus_info:
            if line['bus_id'] == line_number and (line['stop_type'] == 'S' or line['stop_type'] == 'F'):
                stop_type_list.append(line['stop_type'])
        if len(stop_type_list) != 2:
            return print(f'There is no start or end stop for the line: {line_number}.')
    for type_, stop in zip(all_stop_type, stops):
        if type_ == 'S':
            start_stops.add(stop)
        elif type_ == 'F':
            finish_stops.add(stop)
        elif type_ == 'O':
            on_demand_stops.add(stop)
        if stops.count(stop) > 1:
            transfer_stops.add(stop)
    print(f'Start stops: {len(start_stops)} {list(sorted(start_stops))}')
    print(f'Transfer stops: {len(transfer_stops)} {list(sorted(transfer_stops))}')
    print(f'Finish stops: {len(finish_stops)} {list(sorted(finish_stops))}')


def on_demand():
    print('On demand stops test:')
    all_stops = start_stops.union(transfer_stops).union(finish_stops)
    print(sorted(list(on_demand_stops.intersection(all_stops))) if on_demand_stops.intersection(all_stops) else 'OK')


def check_time():
    print('Arrival time test:')
    all_good = True
    for number in set(my_list):
        single_bus_line = {"bus_id": number, "a_time": [], "stop_name": []}
        for line in bus_info:
            if line['bus_id'] == number:
                single_bus_line['a_time'].append(line['a_time'])
                single_bus_line['stop_name'].append(line['stop_name'])
        for count, time in enumerate(single_bus_line['a_time'][:-1]):
            if time > single_bus_line['a_time'][count + 1]:
                print(f"bus_id line {number}: wrong time on station {single_bus_line['stop_name'][count + 1]}")
                all_good = False
                break
    if all_good:
        print('OK')


def check_int(bus_id, stop_id, next_stop):
    id_tuple = (bus_id, stop_id, next_stop)
    for index, value in enumerate(id_tuple):
        if re.match(r'[\d]+', str(value)) is None:
            errors[index] += 1


def check_strings(stop_name, stop_type, a_time):
    pattern_stop_name = '[A-Z].* (?=(Road|Avenue|Boulevard|Street)$)'
    pattern_time = '(^[01][0-9]|2[0-3]):([0-5][0-9]$)'
    if re.match(pattern_stop_name, stop_name) is None:
        errors['stop_name'] += 1
    if stop_type:
        if re.match('^[SOF]$', stop_type) is None:
            errors['stop_type'] += 1
    if re.match(pattern_time, a_time) is None:
        errors['a_time'] += 1


bus_line_info()
check_time()
on_demand()

for bus_line in bus_info:
    check_int(bus_line['bus_id'], bus_line['stop_id'], bus_line['next_stop'])
    check_strings(bus_line['stop_name'], bus_line['stop_type'], bus_line['a_time'])

print(f'Format validation: {sum(errors.values())} errors')
print(f'stop_name: {errors["stop_name"]}\nstop_type: {errors["stop_type"]}\na_time: {errors["a_time"]}')
