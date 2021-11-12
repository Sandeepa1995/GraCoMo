import os
from os.path import exists
import time

import math

import subprocess

# graphit_path = "/home/damitha/CLionProjects/graphit/"
graphit_path = "/home/damitha2/graphit/"
graphitc_path = graphit_path + "build/bin/graphitc.py"
runtime_path = graphit_path + "src/runtime_lib/"

# current_path = "/home/damitha/PycharmProjects/GraCoMo/"
current_path = "/home/damitha2/GraCoMo/"
algo_path = current_path + "bfs_benchmark.gt"
shed_path = current_path + "shed.gt"
inp_folder = current_path + "data_save/"
inp_prefix = inp_folder + "out"
inp_suffix = ".el"
data_path = current_path + "data1"
graphitcpp_path = current_path + "test.cpp"
graphito_path = current_path + "test"

# parmat_path = "/home/damitha/CLionProjects/PaRMAT/Release/PaRMAT"
parmat_path = "/home/damitha2/PaRMAT/Release/PaRMAT"

# TODO check if no schedule is always correct

# Dictionary sets for classifications, 0 is not in dict to be used for instances where the optimization
# is not used at all <- TODO check if used or not


dict_dirs = {
    1: "SparsePush",
    2: "DensePush",
    3: "DensePull",
    4: "DensePull-SparsePush",
    5: "DensePush-SparsePush"
}

# 1
dict_apply_dir = {
    0: "SparsePush",
    1: "DensePull",
    2: "DensePull-SparsePush",
    3: "DensePush-SparsePush"
}

# 2, needs dir
dict_apply_parallel = {
    0: "serial",
    1: "dynamic-vertex-parallel",
    2: "static-vertex-parallel",
    3: "edge-aware-dynamic-vertex-parallel"
    #4: "edge-parallel" # TODO Not a part of it??
}

# 3, needs dir
dict_apply_dvs_conf = {
    0: "bool-array",
    1: "bitvector"
}

dict_apply_dvs_vset = {
    0: "both",
    1: "src-vertexset",
    2: "dst-vertexset"
}

# 4, needs direction and numbers (1 - 20)
dict_apply_numssg = {
    1: "fixed-vertex-count",
    2: "edge-aware-vertex-count"
}

# 5, needs direction
dict_apply_numa = {
    0: "serial",
    1: "static-parallel",
    2: "dynamic-parallel"
}


# TODO skipping directions for now
def gen_all_scheds_f():
    all_sheds =[]
    for x1 in range(6):
        for x2 in range(6):
            if x2 != 0:
                for x2_1 in range(2, 9, 2):
                    for x3 in range(3):
                        if x3 != 0:
                            for x3_1 in range(3):
                                for x3_2 in range(4):
                                    for x4 in range(3):
                                        if x4 != 0:
                                            for x4_1 in range(1, 20, 2):
                                                for x4_2 in range(4):
                                                    for x5 in range(4):
                                                        if x5 != 0:
                                                            for x5_1 in range(4):
                                                                all_sheds.append([[x1], [x2, x2_1], [x3, x3_1, x3_2],
                                                                                  [x4, x4_1, x4_2], [x5, x5_1]])
                                                        else:
                                                            x5_1 = 0
                                                            all_sheds.append(
                                                                [[x1], [x2, x2_1], [x3, x3_1, x3_2], [x4, x4_1, x4_2],
                                                                 [x5, x5_1]])
                                        else:
                                            x4_1 = 0
                                            x4_2 = 0
                                            for x5 in range(4):
                                                if x5 != 0:
                                                    for x5_1 in range(4):
                                                        all_sheds.append([[x1], [x2, x2_1], [x3, x3_1, x3_2],
                                                                          [x4, x4_1, x4_2], [x5, x5_1]])
                                                else:
                                                    x5_1 = 0
                                                    all_sheds.append(
                                                        [[x1], [x2, x2_1], [x3, x3_1, x3_2], [x4, x4_1, x4_2],
                                                         [x5, x5_1]])
                        else:
                            x3_1 = 0
                            x3_2 = 0
                            for x4 in range(3):
                                if x4 != 0:
                                    for x4_1 in range(1, 20):
                                        for x4_2 in range(4):
                                            for x5 in range(4):
                                                if x5 != 0:
                                                    for x5_1 in range(4):
                                                        all_sheds.append([[x1], [x2, x2_1], [x3, x3_1, x3_2],
                                                                          [x4, x4_1, x4_2], [x5, x5_1]])
                                                else:
                                                    x5_1 = 0
                                                    all_sheds.append(
                                                        [[x1], [x2, x2_1], [x3, x3_1, x3_2], [x4, x4_1, x4_2],
                                                         [x5, x5_1]])
                                else:
                                    x4_1 = 0
                                    x4_2 = 0
                                    for x5 in range(4):
                                        if x5 != 0:
                                            for x5_1 in range(4):
                                                all_sheds.append([[x1], [x2, x2_1], [x3, x3_1, x3_2],
                                                                  [x4, x4_1, x4_2], [x5, x5_1]])
                                        else:
                                            x5_1 = 0
                                            all_sheds.append(
                                                [[x1], [x2, x2_1], [x3, x3_1, x3_2], [x4, x4_1, x4_2],
                                                 [x5, x5_1]])
            else:
                x2_1 = 0
                for x3 in range(3):
                    if x3 != 0:
                        for x3_1 in range(3):
                            for x3_2 in range(4):
                                for x4 in range(3):
                                    if x4 != 0:
                                        for x4_1 in range(1, 20):
                                            for x4_2 in range(4):
                                                for x5 in range(4):
                                                    if x5 != 0:
                                                        for x5_1 in range(4):
                                                            all_sheds.append([[x1], [x2, x2_1], [x3, x3_1, x3_2],
                                                                              [x4, x4_1, x4_2], [x5, x5_1]])
                                                    else:
                                                        x5_1 = 0
                                                        all_sheds.append(
                                                            [[x1], [x2, x2_1], [x3, x3_1, x3_2], [x4, x4_1, x4_2],
                                                             [x5, x5_1]])
                                    else:
                                        x4_1 = 0
                                        x4_2 = 0
                                        for x5 in range(4):
                                            if x5 != 0:
                                                for x5_1 in range(4):
                                                    all_sheds.append([[x1], [x2, x2_1], [x3, x3_1, x3_2],
                                                                      [x4, x4_1, x4_2], [x5, x5_1]])
                                            else:
                                                x5_1 = 0
                                                all_sheds.append(
                                                    [[x1], [x2, x2_1], [x3, x3_1, x3_2], [x4, x4_1, x4_2],
                                                     [x5, x5_1]])
                    else:
                        x3_1 = 0
                        x3_2 = 0
                        for x4 in range(3):
                            if x4 != 0:
                                for x4_1 in range(1, 20):
                                    for x4_2 in range(4):
                                        for x5 in range(4):
                                            if x5 != 0:
                                                for x5_1 in range(4):
                                                    all_sheds.append([[x1], [x2, x2_1], [x3, x3_1, x3_2],
                                                                      [x4, x4_1, x4_2], [x5, x5_1]])
                                            else:
                                                x5_1 = 0
                                                all_sheds.append(
                                                    [[x1], [x2, x2_1], [x3, x3_1, x3_2], [x4, x4_1, x4_2],
                                                     [x5, x5_1]])
                            else:
                                x4_1 = 0
                                x4_2 = 0
                                for x5 in range(4):
                                    if x5 != 0:
                                        for x5_1 in range(4):
                                            all_sheds.append([[x1], [x2, x2_1], [x3, x3_1, x3_2],
                                                              [x4, x4_1, x4_2], [x5, x5_1]])
                                    else:
                                        x5_1 = 0
                                        all_sheds.append(
                                            [[x1], [x2, x2_1], [x3, x3_1, x3_2], [x4, x4_1, x4_2],
                                             [x5, x5_1]])
    return all_sheds

def gen_all_scheds_ssg():
    all_sheds =[]
    for x1 in range(5):
        for x2 in range(4):
            if x2 != 0:
                for x2_1 in [1, 8, 16, 64, 256]:   # Problems: Grain size, default is 256?? (That's big)
                        for x3 in range(2):
                            for x3_1 in range(3):
                                for x3_2 in range(6):
                                    for x4 in range(3):
                                        if x4 != 0:
                                            for x4_1 in [1, 5, 7, 10, 20]:
                                                for x4_2 in range(6):
                                                    x5 = 0
                                                    x5_1 = 0
                                                    all_sheds.append(
                                                        [[x1], [x2, x2_1], [x3, x3_1, x3_2], [x4, x4_1, x4_2],
                                                         [x5, x5_1]])
                                        else:
                                            x4_1 = 0
                                            x4_2 = 0
                                            x5 = 0
                                            x5_1 = 0
                                            all_sheds.append(
                                                [[x1], [x2, x2_1], [x3, x3_1, x3_2], [x4, x4_1, x4_2],
                                                 [x5, x5_1]])
            else:
                x2_1 = 0
                for x3 in range(2):
                    for x3_1 in range(3):
                        for x3_2 in range(6):
                            for x4 in range(3):
                                if x4 != 0:
                                    for x4_1 in [1, 5, 7, 10, 20]:
                                        for x4_2 in range(6):
                                            x5 = 0
                                            x5_1 = 0
                                            all_sheds.append(
                                                [[x1], [x2, x2_1], [x3, x3_1, x3_2], [x4, x4_1, x4_2],
                                                 [x5, x5_1]])
                                else:
                                    x4_1 = 0
                                    x4_2 = 0
                                    x5 = 0
                                    x5_1 = 0
                                    all_sheds.append(
                                        [[x1], [x2, x2_1], [x3, x3_1, x3_2], [x4, x4_1, x4_2],
                                         [x5, x5_1]])
    return all_sheds

def gen_all_scheds():
    all_sheds =[]
    for x1 in range(4):
        for x2 in range(4):
            if x2 != 0:
                for x2_1 in [1, 8, 16, 64, 256]:   # Problems: Grain size, default is 256?? (That's big)
                        for x3 in range(2):
                            for x3_1 in range(3):
                                for x3_2 in range(6):
                                    x4 = 0
                                    x4_1 = 0
                                    x4_2 = 0
                                    x5 = 0
                                    x5_1 = 0
                                    all_sheds.append(
                                        [[x1], [x2, x2_1], [x3, x3_1, x3_2], [x4, x4_1, x4_2],
                                         [x5, x5_1]])

            else:
                x2_1 = 0
                for x3 in range(2):
                    for x3_1 in range(3):
                        for x3_2 in range(6):
                            x4 = 0
                            x4_1 = 0
                            x4_2 = 0
                            x5 = 0
                            x5_1 = 0
                            all_sheds.append(
                                [[x1], [x2, x2_1], [x3, x3_1, x3_2], [x4, x4_1, x4_2],
                                 [x5, x5_1]])
    return all_sheds


def gen_shed(s):
    f = open(shed_path, "w")

    f.write('schedule:\n')
    f.write('\tprogram')
    f.write('\n\t->configApplyDirection("s1", "' + dict_apply_dir[s[0][0]] + '")')
    if s[1][0] != 0:
        f.write('\n\t->configApplyParallelization("s1", "' + dict_apply_parallel[s[1][0]] + '", ' + str(s[1][1]) + ')')
    else:
        f.write('\n\t->configApplyParallelization("s1", "' + dict_apply_parallel[s[1][0]] + '")')
    if s[2][2] == 0:
        f.write('\n\t->configApplyDenseVertexSet("s1","' + dict_apply_dvs_conf[s[2][0]] + '", "'
                + dict_apply_dvs_vset[s[2][0]] + '")')
    else:
        f.write('\n\t->configApplyDenseVertexSet("s1","' + dict_apply_dvs_conf[s[2][0]] + '", "'
                + dict_apply_dvs_vset[s[2][0]] + '", "' + dict_dirs[s[2][2]] + '")')
    # if s[3][0] != 0:
    #     if s[3][2] == 0:
    #         f.write('\n\t->configApplyNumSSG("s1","' + dict_apply_numssg[s[3][0]] + '", '
    #                 + str(s[3][1]) + ')')
    #     else:
    #         f.write('\n\t->configApplyNumSSG("s1","' + dict_apply_numssg[s[3][0]] + '", '
    #                 + str(s[3][1]) + ', "' + dict_dirs[s[2][2]] + '")')
    f.write(";")
    f.close()


if __name__ == '__main__':
    graphs_at_config = [
        ["0.45", "0.22", "0.22"],
        ["0.7", "0.1", "0.1"],
        ["0.25", "0.25", "0.25"],
        ["0.40", "0.40", "0.1"],
        ["0.3", "0.3", "0.3"]
    ]
    all_possible_sheds = gen_all_scheds()

    # TODO for actual runs make max nodes 1 MIL and edge mul 1 K
    min_nodes = 1000
    max_nodes = 100000

    min_mul_edge = 10
    max_mul_edge = 1000

    node_r = int(math.log(max_nodes) // math.log(10)) - int(math.log(min_nodes) // math.log(10)) + 1
    edge_r = int(math.log(max_mul_edge) // math.log(10)) - int(math.log(min_mul_edge) // math.log(10)) + 2

    total_calcs = 0

    # res1 = os.system("mkdir data_save")

    d_f = open(data_path, "w")
    for nr in range(node_r):
        node_val = min_nodes * (10**nr)

        for er in range(edge_r):
            edge_val = node_val * min_mul_edge * (10**er)
            # Removed the node^2 > edges check here
            for cg in graphs_at_config:
                inp_name = str(node_val) + "_" + str(edge_val) + "_" + cg[0] + "_" + cg[1] + "_" + cg[2]
                inp_path = inp_prefix + inp_name + inp_suffix
                # res1 = os.system(parmat_path + " -nVertices " + str(node_val) + " -nEdges "
                #                  + str(edge_val) + " -output " + inp_path + " -a " + cg[0]
                #                  + " -b " + cg[1] + " -c " + cg[2])

                if exists(inp_path):
                    # Generate schedule here
                    for sh in all_possible_sheds:
                        if sh[4][0] != 0:
                            continue
                        else:
                            gen_shed(sh)
                            tt1 = time.time()
                            res2 = os.system("python " + graphitc_path + " -a " +
                                             algo_path + " -f " + shed_path + " -o " + graphitcpp_path)
                            if res2 == 0:
                                tt2 = time.time()
                                res3 = os.system("g++ -I " + runtime_path +
                                                 " -O3 " + graphitcpp_path + " -o " + graphito_path)
                                if res3 == 0:
                                    total_calcs += 1
                                    cnt = 0
                                    nm = 0
                                    t1 = 0
                                    cmd = [graphito_path, inp_path]
                                    res4 = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                                    for line in iter(res4.stdout.readline, b''):
                                        if cnt > 2:
                                            t1 += float(line.rstrip().decode('utf-8'))
                                            nm += 1
                                        cnt += 1
                                    feat_data = [node_val, edge_val]
                                    d_f.write(str(sh[0][0]) + ","
                                              + str(sh[1][0]) + "," + str(sh[1][1]) + ","
                                              + str(sh[2][0]) + "," + str(sh[2][1]) + "," + str(sh[2][2]) + ","
                                              + str(node_val) + "," + str(edge_val) + ","
                                              + '{:.7f}'.format(t1/nm) + "," + inp_name + "\n")
                                    d_f.flush()
                                # d_f.write(str(sh[0][0]) + ","
                                #           + str(sh[1][0]) + "," + str(sh[1][1]) + ","
                                #           + str(sh[2][0]) + "," + str(sh[2][1]) + "," + str(sh[2][2]) + ","
                                #           + str(sh[3][0]) + "," + str(sh[3][1]) + "," + str(sh[3][2]) + ","
                                #           + str(node_val) + "," + str(edge_val) + ","
                                #           + str(time.time() - t1) + "\

    # d_f.close()
    # print(len(all_possible_sheds))
    print(total_calcs)
