def rakal_capacity(instructions, rakal_instructions, images_values, lrt_compatible_phases=None):

    number_of_images = 0
    for r in range(len(images_values)):
        if images_values[r] > 0:
            number_of_images = number_of_images + 1

    cycle_time = rakal_instructions[1]
    train_lost_time = rakal_instructions[2]
    if rakal_instructions[5] > 0:
        lost_time = rakal_instructions[5]
    else:
        lost_time = 14 + 3 * number_of_images
    #lost_time=11
    #20 for two images, 23 for three, 26 for four

    # Split phase volumes into LRT-compatible and LRT-hostile.
    # Phase A is always compatible; phases B-F are compatible only if they
    # contain no LRT-conflicting movements (determined by c_optimization).
    if lrt_compatible_phases is None:
        lrt_compatible_phases = [True] + [False] * (len(images_values) - 1)

    compatible_volume = sum(v for v, c in zip(images_values, lrt_compatible_phases) if c)
    hostile_volume = sum(v for v, c in zip(images_values, lrt_compatible_phases) if not c)
    all_images = compatible_volume + hostile_volume

    capacity = instructions[0]
    frequency = rakal_instructions[3]   #[headway]רכבת כל כמה דקות

    both_directions_frequency = frequency / 2
    trains_per_hour = 60 / both_directions_frequency
    cycles_per_hour = 3600 / cycle_time

    # Green time allocated to LRT-compatible phases (proportional to their volume).
    # LRT can move freely during compatible_green; during hostile_green (+ lost time absorbed)
    # the LRT signal is red.
    compatible_green = (cycle_time - lost_time) * (compatible_volume / all_images) if all_images > 0 else 0
    hostile_green = cycle_time - compatible_green

    if trains_per_hour / cycles_per_hour > 1:
        train_cycle_probability = 1
    else:
        train_cycle_probability = round((trains_per_hour / cycles_per_hour), 3)

    red_probability = hostile_green / cycle_time
    train_red_probability = red_probability * train_cycle_probability
    cycle_train_lost_time = round((train_red_probability * train_lost_time))
    no_train_real_capacity = capacity * (cycle_time - lost_time) / cycle_time
    real_capacity = capacity * (cycle_time - lost_time - cycle_train_lost_time) / cycle_time
    v_over_c = all_images / real_capacity
    #print (no_train_real_capacity)
    print('rakal v/C=' + str(v_over_c))
    print('real capacity=' + str(real_capacity))
    #print(train_red_probability)
    #print(train_cycle_probability)
    #print(red_probability)
    #print(hostile_green)
    #print(lost_time)

    return v_over_c, real_capacity
