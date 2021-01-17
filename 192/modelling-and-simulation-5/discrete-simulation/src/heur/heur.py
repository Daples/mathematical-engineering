import random
<<<<<<< HEAD
import sim
=======
import copy

>>>>>>> 1b3ed241a558fac686c4ed0a6549d37a8e6e71a5

initial_array = [[4, 9, 5],
                 [4, 5, 9],
                 [3, 8, 7, 10], [3, 8, 7, 10], [3, 8, 7, 10], [3, 8, 7, 10],
                 [3, 7, 8, 10], [3, 7, 8, 10], [3, 7, 8, 10], [3, 7, 8, 10], [3, 7, 8, 10],
                 [7, 3, 8, 10], [7, 3, 8, 10],
                 [10]]
array_pruebita = [[4, 9, 5],
                  [4, 5, 9],
                  [3, 8, 7, 10],
                  [3, 7, 8, 10],
                  [7, 3, 8, 10]]

m = sim.Manager(2 ** 32 - 1)

<<<<<<< HEAD

=======
# In-Route
def swap_in_route(array, z, p=0.01):
    best_i = None
    best_j = None
    for pri in array:
        for i in range(len(pri) - 1):
            for j in range(i, len(pri)):
                if random.random() < p:
                    pri[i], pri[j] = pri[j], pri[i]
                    new_z = 3  # Objective function
                    if new_z < z:
                        z = new_z
                        best_i = i
                        best_j = j
                        pri[i], pri[j] = pri[j], pri[i]
                    else:
                        pri[i], pri[j] = pri[j], pri[i]

            if best_i is not None:
                pri[best_i], pri[best_j] = pri[best_j], pri[best_i]
                best_i = None
                best_j = None
    return array, z


def move_in_route(array, z, p=0.01):
    best_i = None
    best_j = None
    for pri in array:
        for i in range(len(pri)):
            for j in range(len(pri)):
                if random.random() < p:
                    pri.insert(i, pri.pop(j))
                    new_z = 3  # Objective function
                    if new_z < z:
                        z = new_z
                        best_i = i
                        best_j = j
                        pri.insert(j, pri.pop(i))
                    else:
                        pri.insert(j, pri.pop(i))

            if best_i is not None:
                pri.insert(best_i, pri.pop(best_j))
                best_i = None
                best_j = None
    return array, z


# Inter-Route
def swap_inter_route(array, z, p=0.01):
    best_pri = None
    best_i = None
    best_j = None
    for s in range(len(array)):
        source_pri = array[s]
        for i in range(len(source_pri)):
            for o in range(s, len(array)):
                obj_pri = array[o]
                for j in range(len(obj_pri)):
                    if random.random() < p:
                        source_pri[i], obj_pri[j] = obj_pri[j], source_pri[i]

                        from_obj_in_source = [i for i, x in enumerate(source_pri) if x == obj_pri[j]]
                        from_source_in_obj = [i for i, x in enumerate(obj_pri) if x == source_pri[j]]

                        if len(from_obj_in_source) > 1:
                            rnd = random.randint(0, 2)
                            index_pop_source = from_obj_in_source[rnd]
                            elem_pop_source = source_pri[index_pop_source]
                            source_pri.pop(index_pop_source)

                        if len(from_source_in_obj) > 1:
                            rnd = random.randint(0, 2)
                            index_pop_obj = from_source_in_obj[rnd]
                            elem_pop_obj = source_pri[index_pop_obj]
                            obj_pri.pop(index_pop_obj)

                        new_z = 3  # Objective function
                        if new_z < z:
                            z = new_z
                            best_i = i
                            best_j = j
                            best_pri = o
                            if not len(from_source_in_obj) == 2 and not len(from_source_in_obj) == 2:
                                source_pri[i], obj_pri[j] = obj_pri[j], source_pri[i]
                            else:
                                if len(from_source_in_obj) == 2:
                                    obj_pri.insert(index_pop_obj, elem_pop_obj)
                                if len(from_obj_in_source) == 2:
                                    source_pri.insert(index_pop_source, elem_pop_source)
                                source_pri[i], obj_pri[j] = obj_pri[j], source_pri[i]
                        else:
                            if not len(from_source_in_obj) == 2 and not len(from_source_in_obj) == 2:
                                source_pri[i], obj_pri[j] = obj_pri[j], source_pri[i]
                            else:
                                if len(from_source_in_obj) == 2:
                                    obj_pri.insert(index_pop_obj, elem_pop_obj)
                                if len(from_obj_in_source) == 2:
                                    source_pri.insert(index_pop_source, elem_pop_source)
                                source_pri[i], obj_pri[j] = obj_pri[j], source_pri[i]

            if best_i is not None:
                obj_pri = array[best_pri]
                source_pri[best_i], obj_pri[best_j] = obj_pri[best_j], source_pri[best_i]

    return array, z


def prueita(array, p=0.01):
    neigh = []
    for s in range(len(array)):
        source_pri = array[s]
        for i in range(len(source_pri)):
            for o in range(s, len(array)):
                obj_pri = array[o]
                for j in range(len(obj_pri)):
                    if random.random() < p:
                        source_pri[i], obj_pri[j] = obj_pri[j], source_pri[i]

                        from_obj_in_source = [y for y, x in enumerate(source_pri) if x == obj_pri[j]]
                        from_source_in_obj = [y for y, x in enumerate(obj_pri) if x == source_pri[i]]

                        if len(from_obj_in_source) > 1:
                            rnd = random.randint(0, 2)
                            index_pop_source = from_obj_in_source[rnd]
                            elem_pop_source = source_pri[index_pop_source]
                            source_pri.pop(index_pop_source)

                        if len(from_source_in_obj) > 1:
                            rnd = random.randint(0, 2)
                            index_pop_obj = from_source_in_obj[rnd]
                            elem_pop_obj = source_pri[index_pop_obj]
                            obj_pri.pop(index_pop_obj)

                        neigh.append(copy.deepcopy(array))

                        if not len(from_source_in_obj) == 2 and not len(from_source_in_obj) == 2:
                            source_pri[i], obj_pri[j] = obj_pri[j], source_pri[i]
                        else:
                            if len(from_source_in_obj) == 2:
                                obj_pri.insert(index_pop_obj, elem_pop_obj)
                            if len(from_obj_in_source) == 2:
                                source_pri.insert(index_pop_source, elem_pop_source)
                            source_pri[i], obj_pri[j] = obj_pri[j], source_pri[i]

    return neigh


def move_inter_route(array, z):
    best_i = None
    best_j = None
    best_obj = None
    for index_source in range(len(array) - 1):
        source = array[index_source]
        for i in range(len(source)):
            for index_obj in range(index_source, len(array)):
                obj = array[index_obj]
                for j in range(len(obj)):
                    if source[i] not in obj:
                        obj.insert(j, source.pop(i))
                        new_z = 3 # Objective function
                        if new_z < z:
                            z = new_z
                            best_i = i
                            best_j = j
                            best_obj = index_obj
                            source.insert(i, obj.pop(j))
                        else:
                            source.insert(i, obj.pop(j))
            if best_obj is not None:
                array[best_obj].insert(best_j, source.pop(best_i))


def vnd(array, z, max_it=5):
    i = 0
    zetas = []
    while i <= max_it:
        array, z = swap_inter_route(array, z)
        r = random.randint(0, 2)
        if r == 1:
            array, z = swap_in_route(array, z)
            array, z = move_in_route(array, z)
        else:
            array, z = move_in_route(array, z)
            array, z = swap_in_route(array, z)
        i += 1
        zetas.append(z)
    return array, z, zetas

out = prueita(initial_array)
j = 0
for i in out:
    j += 1
    print(i)
print(j)
>>>>>>> 1b3ed241a558fac686c4ed0a6549d37a8e6e71a5
