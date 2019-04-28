# 放在数据根目录运行
# 需要四个文件
# input_distance_time.txt；
# input_node.csv
# input_vehicle_type.csv
# Result.csv

import pandas as pd
def hour_to_minutes(hours):
    """
    :param hours: sample '15:30'
    :return:    930
    """
    if hours == '-':
        return '-'
    hour, minute = hours.split(':')
    minutes = int(hour) * 60 + int(minute)
    if minutes == 0:
        return int(24 * 60)
    else:
        return int(minutes)


def minutes_to_hour_str(minutes):
    hour = minutes // 60
    minute = minutes % 60
    if hour < 10:
        hour = '0'+ str(hour)
    if minute < 10:
        minute = '0'+ str(minute)
    time_str = str(hour) + ':' + str(minute)
    return time_str


# 数据读取
result = pd.read_csv('Result.csv')

input_distance_time = pd.read_csv('input_distance_time.txt', header=0)
input_distance_time.drop(['ID'], axis=1, inplace=True)

input_node = pd.read_csv('input_node.csv', header=0)
input_node['first_receive_tm'] = pd.Series(list(map(hour_to_minutes, input_node['first_receive_tm'])))
input_node['last_receive_tm'] = pd.Series(list(map(hour_to_minutes, input_node['last_receive_tm'])))

customer_df = input_node[input_node['type'] == 2].copy()
customer_df.loc[:, ('pack_total_weight')] = pd.to_numeric(customer_df['pack_total_weight']).values
customer_df.loc[:, ('pack_total_volume')] = pd.to_numeric(customer_df['pack_total_volume']).values

input_vehicle_type = pd.read_csv('input_vehicle_type.csv', header=0)

# 检验结果写入
f = open('Result_checher.csv', 'w')
f.write('distribute_lea_tm,distribute_arr_tm,distance,trans_cost,charge_cost,wait_cost,fixed_use_cost,total_cost,charge_cnt\n')


# 逐行检测 序列
for idx in result.index:
    print_result = False
    i = result.loc[idx]
    vehicle_type, dist_seq, distribute_lea_tm = i.vehicle_type, i.dist_seq, i.distribute_lea_tm
    vehicle_type_info = input_vehicle_type[input_vehicle_type['vehicle_type_ID'] == vehicle_type]
    ID, name, max_volume, max_weight, cnt, max_range, charge_tm, unit_trans_cost, fixed_use_cost = vehicle_type_info.values[0]
    dist_seq_list = eval(dist_seq.replace(';', ',').join('[]'))
    seq_tuple = tuple(zip(dist_seq_list[:-1], dist_seq_list[1:]))
    end_time = hour_to_minutes(distribute_lea_tm)
    charger_cnt = 0
    distance = 0
    trans_cost = 0
    charge_cost = 0
    wait_cost = 0
    range_remain = max_range
    for node_idx in range(seq_tuple.__len__()):
        from_node, to_node = seq_tuple[node_idx]
        start_time = end_time
        driving_range, driving_time = input_distance_time[(input_distance_time['from_node'] == from_node)&(input_distance_time['to_node'] == to_node)][['distance', 'spend_tm']].values[0]
        range_remain = range_remain - driving_range
        time_arrive = start_time + driving_time
        distance += driving_range
        trans_cost += driving_range * unit_trans_cost / 1000
        if range_remain >= 0:
            if to_node in range(1,1001):
                # 初始化额外等待时间
                wait_time = 0
                # 服务客户时间 卸货30分钟
                serving_time = 30
                # 充电时间 0
                charge_time = 0
                customer_info = customer_df.loc[to_node]
                id, type_, lng, lat, weight, volumne, et, lt = customer_info.values
                # 需要额外等待
                if time_arrive < et:
                    wait_time += et - time_arrive
                    time_arrive = et
                # 无需额外等待
                elif et <= time_arrive <= lt:
                    wait_time += 0
                    time_arrive = time_arrive
                # 超出最晚时刻
                elif time_arrive > lt:
                    print(str(idx) + 'seq ' + str(to_node) + ' is larger than lt')
                    print_result = True
                # 异常
                else:
                    print(str(idx) + 'seq ' + str(to_node) + ' is invalid')

                charger_cnt += 0

            elif to_node in range(1001, 1101):
                # 充电桩即到即用
                wait_time = 0
                # 不服务顾客 服务时间0
                serving_time = 0
                # 充电时间 30分钟
                charge_time = charge_tm*60
                # 充电次数+1
                charger_cnt += 1
                # 充电成本+50
                charge_cost += 50
                range_remain = max_range
            else:
                # 如果不是种到配送中心
                if node_idx < seq_tuple.__len__() - 1:
                    # 额外等待时间+60
                    wait_time = 60
                    # 充电次数+1
                    charger_cnt += 1

                    range_remain = max_range

                else:
                    # print('finished')
                    wait_time = 0

                    charger_cnt = charger_cnt
                # 无服务时间
                serving_time = 0
                # 无充电成本
                charge_time = 0

            # 只有服务顾客早到的等待和中途返回配送中心的等待需要计算等待成本
            wait_cost += wait_time * 0.4

            end_time += driving_time + wait_time + charge_time + serving_time
        else:
            print(range_remain)
            print(idx,'is out of range')
    wait_cost = round(wait_cost, 2)
    trans_cost = round(trans_cost, 2)
    total_cost = round(trans_cost + charge_cost + wait_cost + fixed_use_cost,2)
    distribute_arr_time = minutes_to_hour_str(int(end_time))

    result_line = distribute_lea_tm, distribute_arr_time, distance, trans_cost, charge_cost, wait_cost, fixed_use_cost, total_cost, charger_cnt
    result_line_str = ','.join([str(i) for i in result_line]) + '\n'
    f.write(result_line_str)

f.close()
