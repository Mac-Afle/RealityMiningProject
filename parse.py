import numpy as np
def parse_data(filename, col_names, separator=",") :
    f = open(filename)
    num_cols = len(col_names)
    entries = []
    for line in f :
        line = line.strip().split(separator)
        pairs = dict(zip(col_names, line))
        entries.append(pairs)
    return entries

def filtered_parse_data(filename, col_names, keep_col_names, separator=",") :
    data = parse_data(filename, col_names, separator)
    filtered_data = dict()
    for item in data :
        user_id = item["user_id"]
        user_dict = dict()
        for category in keep_col_names :
            user_dict[category] = [item[category]]
        if filtered_data.has_key(user_id) :
            for category in keep_col_names :
                filtered_data[user_id][category].extend(user_dict[category])
        else :
            filtered_data[user_id] = user_dict
    return filtered_data

def get_health_data() :
    cols = ["user_id","current_weight","current_height","salads_per_week","veggies_fruits_per_day","healthy_diet","aerobic_per_week","sports_per_week","current_smoking","survey.month"]
    categorical_cols = ["healthy_diet", "current_smoking"]
    return filtered_parse_data("Health.csv", cols, categorical_cols)

def get_location_data() :
    cols = ["user_id","time","wireless_mac","strength","unix_time"]
    categorical_cols = ["wireless_mac"]
    return filtered_parse_data("WLAN2.csv", cols, categorical_cols)

def location_data_statistics() :
    location_data = get_location_data()
    user_visited_locations = location_data.values()
    locations_with_duplicates = []
    for location_list in user_visited_locations :
        locations_with_duplicates.extend(location_list["wireless_mac"])
    locations = set(locations_with_duplicates)
    print "num_locations " + str(len(locations))
    unique_visited = []
    total_visited = []
    for user_id in location_data.keys() :
        num_checkins = len(location_data[user_id]["wireless_mac"])
        print num_checkins
        num_unique_checkins = len(set(location_data[user_id]["wireless_mac"]))
        unique_visited.append(num_unique_checkins)
        total_visited.append(num_checkins)
    avg_unique_checkins = sum(unique_visited) / float(len(unique_visited))
    avg_checkins = sum(total_visited) / float(len(total_visited))

    print "avg wifi checkings:" + str(avg_checkins)
    print "std dev:" + str(np.std(total_visited))
    print "unique wifi checkins:" + str(avg_unique_checkins)
    print "std dev:" + str(np.std(unique_visited))
