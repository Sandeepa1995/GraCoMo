import os
import time

import math

import subprocess
import multiprocessing as mp


graphit_path = "/home/damitha/CLionProjects/graphit/"
# graphit_path = "/home/damitha2/graphit/"
graphitc_path = graphit_path + "build/bin/graphitc.py"
runtime_path = graphit_path + "src/runtime_lib/"

current_path = "/home/damitha/PycharmProjects/GraCoMo/"
# current_path = "/home/damitha2/GraCoMo/"
algo_path = current_path + "bfs_benchmark.gt"
shed_prefix = current_path + "/sheds/shed"
shed_suffix = ".gt"
inp_folder = current_path + "data_save2/"
inp_prefix = inp_folder + "out"
inp_suffix = ".el"
data_path = current_path + "csv_data/data"
graphit_files_path = current_path + "graphit/"
graphitcpp_pre_path = graphit_files_path + "test"
graphitcpp_ext = ".cpp"
graphito_pre_path = graphit_files_path + "test"

parmat_path = "/home/damitha/CLionProjects/PaRMAT/Release/PaRMAT"
# parmat_path = "/home/damitha2/PaRMAT/Release/PaRMAT"

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


all_possible_sheds = gen_all_scheds()


def gen_shed(s, x):
    f = open(shed_prefix + "_" + str(x) + "_" + shed_suffix, "w")

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
    f.write(";")
    f.close()


def exec_sheds_for_graph(graph_inp):
    inp_path = inp_folder + graph_inp
    graph_name = graph_inp[3:-3]
    d_f = open(data_path + "_" + graph_name, "w")
    graph_feats = graph_name.split("_")
    node_val = int(graph_feats[0])
    edge_val = int(graph_feats[1])
    for filename in sorted(os.listdir(graphit_files_path)):
        graphito_path = graphit_files_path + filename

        sh_i = int(filename.split(".")[0].split("_")[1])
        sh = all_possible_sheds[sh_i]

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
        d_f.write(str(sh[0][0]) + ","
                  + str(sh[1][0]) + "," + str(sh[1][1]) + ","
                  + str(sh[2][0]) + "," + str(sh[2][1]) + "," + str(sh[2][2]) + ","
                  + str(node_val) + "," + str(edge_val) + ","
                  + '{:.7f}'.format(t1 / nm) + "," + graph_name + "\n")
        d_f.flush()
    d_f.close()

if __name__ == '__main__':
    graphs_at_config = [
        ["0.45", "0.22", "0.22"],
        ["0.7", "0.1", "0.1"],
        ["0.25", "0.25", "0.25"],
        ["0.40", "0.40", "0.1"],
        ["0.3", "0.3", "0.3"]
    ]

    # TODO for actual runs make max nodes 1 MIL and edge mul 1 K
    min_nodes = 1000
    max_nodes = 100000

    min_mul_edge = 10
    max_mul_edge = 1000

    node_r = int(math.log(max_nodes) // math.log(10)) - int(math.log(min_nodes) // math.log(10)) + 1
    edge_r = int(math.log(max_mul_edge) // math.log(10)) - int(math.log(min_mul_edge) // math.log(10)) + 2

    total_calcs = 0

    # resa = os.system("mkdir data_save2")
    # resb = os.system("mkdir csv_data")
    # resc = os.system("mkdir sheds")
    # resd = os.system("mkdir graphit")
    #
    # for nr in range(node_r):
    #     node_val = min_nodes * (10**nr)
    #
    #     for er in range(edge_r):
    #         edge_val = node_val * min_mul_edge * (10**er)
    #         for cg in graphs_at_config:
    #             inp_name = str(node_val) + "_" + str(edge_val) + "_" + cg[0] + "_" + cg[1] + "_" + cg[2]
    #             inp_path = inp_prefix + inp_name + inp_suffix
    #             res1 = os.system(parmat_path + " -nVertices " + str(node_val) + " -nEdges "
    #                              + str(edge_val) + " -output " + inp_path + " -a " + cg[0]
    #                              + " -b " + cg[1] + " -c " + cg[2])

    # for x in range(len(all_possible_sheds)):
    #     sh = all_possible_sheds[x]
    #
    #     gen_shed(sh, x)
    #
    #     shed_path_complete = shed_prefix + "_" + str(x) + "_" + shed_suffix
    #     graphitcpp_complete = graphitcpp_pre_path + "_" + str(x) + "_" + graphitcpp_ext
    #     graphito_complete = graphito_pre_path + "_" + str(x)
    #
    #     res2 = os.system("python " + graphitc_path + " -a " +
    #                      algo_path + " -f " + shed_path_complete + " -o " +
    #                      graphitcpp_complete)
    #     if res2 == 0:
    #         res3 = os.system("g++ -std=c++14 -I " + runtime_path +
    #                          " -O3 " + graphitcpp_complete + " -o " + graphito_complete + ".shed")
    cores = mp.cpu_count()
    pool = mp.Pool(cores//2)

    for graph_inp in sorted(os.listdir(inp_folder)):
        # print(graph_inp)
        pool.apply_async(exec_sheds_for_graph, args=(graph_inp,))

    pool.close()
    pool.join()

    # for filename in os.listdir(graphit_files_path):
    #     sh_i = int(filename.split(".")[0].split("_")[1])
    #     sh = all_possible_sheds[sh_i]
    #
    #     total_calcs += 1
    #     cnt = 0
    #     nm = 0
    #     t1 = 0
    #     cmd = [graphito_path, inp_path]
    #     res4 = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    #     for line in iter(res4.stdout.readline, b''):
    #         if cnt > 2:
    #             t1 += float(line.rstrip().decode('utf-8'))
    #             nm += 1
    #         cnt += 1
    #     feat_data = [node_val, edge_val]
    #     d_f.write(str(sh[0][0]) + ","
    #               + str(sh[1][0]) + "," + str(sh[1][1]) + ","
    #               + str(sh[2][0]) + "," + str(sh[2][1]) + "," + str(sh[2][2]) + ","
    #               + str(node_val) + "," + str(edge_val) + ","
    #               + '{:.7f}'.format(t1/nm) + "," + inp_name + "\n")

    #             if res3 == 0:
    #                 total_calcs += 1
    #                 cnt = 0
    #                 nm = 0
    #                 t1 = 0
    #                 cmd = [graphito_path, inp_path]
    #                 res4 = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    #                 for line in iter(res4.stdout.readline, b''):
    #                     if cnt > 2:
    #                         t1 += float(line.rstrip().decode('utf-8'))
    #                         nm += 1
    #                     cnt += 1
    #                 feat_data = [node_val, edge_val]
    #                 d_f.write(str(sh[0][0]) + ","
    #                           + str(sh[1][0]) + "," + str(sh[1][1]) + ","
    #                           + str(sh[2][0]) + "," + str(sh[2][1]) + "," + str(sh[2][2]) + ","
    #                           + str(node_val) + "," + str(edge_val) + ","
    #                           + '{:.7f}'.format(t1/nm) + "," + inp_name + "\n")
    #                 d_f.flush()
    # d_f.close()
    # print(len(all_possible_sheds))
    # print(total_calcs)
