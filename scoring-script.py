# import pandas as pd
# import numpy as np

# metadata_dict = {
#    'readme': 0,
#    'setup': 0,
#    'documentation': 0,
#    'average %issues closed': 0,
#    'number_contributors': 0,
#    'average time': 13,
#    'license': 0
# }


def scoring(arg):
    weight_ramp = 0.15  # ramp up score checks if the repository has a readme, a setup, and documentation to reduce
    # ramp-up time
    weight_correct = 0.2  # correctness uses the average percentage of issues closed per month over the last year
    weight_busfactor = 0.3  # the number of contributors over the last month.
    weight_active = 0.2  # active uses the average time taken to close or respond to an open issue.
    weight_license = 0.15  # average number of contributors over the last year.

    key = 'readme'
    key1 = 'setup'
    key2 = 'documentation'
    unw_ramp = (arg.get(key) + arg.get(key1) + arg.get(key2)) / 3
    avg_iss_clsd = arg.get('average %issues closed')  # number of average issues closed

    if avg_iss_clsd == 0:
        correctness_sc = 0
    elif avg_iss_clsd <= 50:
        if avg_iss_clsd > 0:
            correctness_sc = 0.5
        else:
            correctness_sc = 0
    else:
        correctness_sc = 1

    num_contributors = (arg.get('number_contributors'))
    if num_contributors >= 150:
        bus_score = 1
    elif 150 > num_contributors >= 75:
        bus_score = 0.5
    elif 75 > num_contributors >= 20:
        bus_score = 0.2
    elif num_contributors < 20:
        bus_score = 0
    else:
        bus_score = 0

    time_taken = (arg.get('average time'))
    if time_taken <= 3:
        active = 1
    elif 3 < time_taken <= 7:
        active = 0.5
    elif 7 < time_taken <=14:
        active = 0.2
    elif time_taken > 14:
        active = 0

    license_boo = (arg.get('license'))
    if license_boo == 0:
        license_unw = 0
    else:
        license_unw = 1

    ramp_up_score = unw_ramp
    correctness_score = correctness_sc
    bus_factor_score = bus_score
    responsive_maintainer_score = active
    license_score = license_unw

    net_score = (weight_ramp * ramp_up_score) + (weight_correct * correctness_score) + (
                weight_busfactor * bus_factor_score) + (weight_active * responsive_maintainer_score) + (
                            weight_license * license_score)  # calculating the weighted sum
    print(net_score)
    pass


scoring(metadata_dict)
