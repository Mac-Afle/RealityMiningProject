from parse import get_location_data
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

def counter_intersection(c1, c2) :
    intersection_dict = dict()
    for k in c1.keys() :
        if c2.has_key(k) :
            intersection_dict[k] = min(c1[k], c2[k])
    return intersection_dict

def count_loops(c1) :
    loops = 0
    for k in c1.keys() :
        loops += c1[k] #** 2
    return loops

def user_location_count(location_data) :
    # [User [Location [Count]]]
    count_dict = dict()
    for user in location_data.keys() :
        visited_locations = location_data[user]["wireless_mac"]
        counter = Counter(visited_locations)
        count_dict[user] = dict()
        for key,val in counter.items() :
            count_dict[user][key] = val #** 2
    return count_dict

location_data = get_location_data()
user_visited_dict = user_location_count(location_data)
user_list = location_data.keys()

# Ego-network based feature
# Bag-of-locations + cosine similarity.
for user in user_list :
    cosine_out = open("cosine/"+str(user), "w")
    user_locations = user_visited_dict[user]
    scores = dict()
    for dst_user in user_list :
        dst_locations = user_visited_dict[dst_user]
        unique_locations = set(user_locations.keys()).union(set(dst_locations.keys()))
        id_locations = dict(zip(unique_locations, range(len(unique_locations))))
        user_vec = [0]*len(unique_locations)
        dst_vec = [0]*len(unique_locations)
        for loc in unique_locations :
            for loc_dict,vec in [(dst_locations,dst_vec),(user_locations,user_vec)] :
                if loc_dict.has_key(loc) :
                    vec[id_locations[loc]] = loc_dict[loc]
        sim = cosine_similarity(user_vec, dst_vec)
        scores[dst_user] = sim
    scores = sorted(scores.items(), reverse=True, key=lambda x:x[1])
    for dst_user, score in scores :
        cosine_out.write(str(dst_user) + '\t' + str(score[0]) + '\n')
    cosine_out.close()


# Reachability based feature
# Pathsim
for user in user_list :
    pathsim_out = open("pathsim2/"+str(user), "w")
    scores = dict()
    for dst_user in user_list :
        src_visited_locations_counter = user_visited_dict[user]
        dst_visited_locations_counter = user_visited_dict[dst_user]
        intersection_counts = counter_intersection(
                                    src_visited_locations_counter,
                                    dst_visited_locations_counter)
        a_b = sum(intersection_counts.values())
        a_a = count_loops(src_visited_locations_counter) # n->n^2 b/c of intersec.
        b_b = count_loops(dst_visited_locations_counter)
        pathsim = 2*float(a_b)/(a_a + b_b)
        scores[dst_user] = pathsim
    for dst_user, score in sorted(scores.items(), reverse=True, key=lambda x:x[1]) :
        pathsim_out.write(str(dst_user) + '\t' + str(score) + '\n')
    pathsim_out.close()


