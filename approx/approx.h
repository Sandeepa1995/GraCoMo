#include <omp.h>
#include <math.h>
#include <chrono>
#include <unistd.h>
#include <thread>

#include "../objects/csrc_matrix.h"
#include "../objects/dense_matrix.h"

template<class SM>
//void gat_forward(const SM * graph, const DM* h_l0, const DM* w_l0, DM* h_l, DM* w_l){
void approx_range(const SM * graph, int prec, int* min_max){
    auto start = std::chrono::high_resolution_clock::now();


    typedef typename SM::itype iT; // Node IDs
    typedef typename SM::ntype nT; // Edge IDs
    typedef typename SM::vtype vT; // Value of node

    int cores = 16;
    int rows = (int)graph->nrows();
    int mins[16] = {rows};
    int maxs[16] = {0};
    int rows_per_thread = rows / cores;

    double percen = (double) prec / 100.0;

//    std::cout << "Start" << std::endl;
//    #pragma omp parallel for
//    for (int i=0; i<16; i++){
////        std::this_thread::sleep_for(std::chrono::seconds(1));
//        double x = 0;
//        for (int j = 0; j < 1000000000; j++){
//            x += j;
//        }
//        std::cout << i << " " << omp_get_thread_num() << " " << x << std::endl;
//    }

    int limit[16];
    #pragma omp parallel for
    for (int i=0; i<16; i++){
        if ((rows - rows_per_thread*i)<rows_per_thread){
            limit[i] = rows;
        } else {
            limit[i] = rows_per_thread * i + (int)(rows_per_thread * percen);
        }
    }

    #pragma omp parallel for
    for(int i=0; i<cores; i++){
        nT sum = 0;
        for(nT j=rows_per_thread*i; j<limit[i]; j++){
            nT e_0=graph->offset_ptr()[j];
            nT e_1=graph->offset_ptr()[j+1];
            nT diff_e = e_1 - e_0;
            if (diff_e < mins[i]){
                mins[i] = diff_e;
            }
            if (diff_e > maxs[i]){
                maxs[i] = diff_e;
            }
        }
    }

    int min_val = *std::min_element( std::begin(mins), std::end(mins));
    int max_val = *std::max_element( std::begin(maxs), std::end(maxs));
//    std::cout << "min: " << min_val << ", max: " << max_val << std::endl;
    min_max[0] = min_val;
    min_max[1] = max_val;
    std::cout << min_val << " " << max_val << " ";

    auto stop = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);

//    std::cout << "Time taken by min max approx function: "
//         << duration.count() << " microseconds" << std::endl;
}

template<class SM>
//void gat_forward(const SM * graph, const DM* h_l0, const DM* w_l0, DM* h_l, DM* w_l){
void approx_sdiv(const SM * graph, int prec){
    auto start = std::chrono::high_resolution_clock::now();


    typedef typename SM::itype iT; // Node IDs
    typedef typename SM::ntype nT; // Edge IDs
    typedef typename SM::vtype vT; // Value of node

    int cores = 16;
    int rows = (int)graph->nrows();
    double sq_sum[16] = {0};
    double mean[16] = {0};
    double nm[16] = {0};
    int rows_per_thread = rows / cores;

    double percen = (double) prec / 100.0;

    int limit[16];
#pragma omp parallel for
    for (int i=0; i<16; i++){
        if ((rows - rows_per_thread*i)<rows_per_thread){
            limit[i] = rows;
        } else {
            limit[i] = rows_per_thread * i + (int)(rows_per_thread * percen);
        }
    }

#pragma omp parallel for
    for(int i=0; i<cores; i++){
        double sum_val = 0;
        double itered_over_val = 0;
        double sq_sum_val = 0;
        for(nT j=rows_per_thread*i; j<limit[i]; j++){
            nT e_0=graph->offset_ptr()[j];
            nT e_1=graph->offset_ptr()[j+1];
            nT diff_e = e_1 - e_0;

            sum_val += diff_e;
            sq_sum_val += diff_e*diff_e;
            itered_over_val += 1;
        }
        sq_sum[i] = sq_sum_val;
        nm[i] = itered_over_val;
        mean[i] = sum_val;
    }

    double sq_sum_vals = 0;
    double mean_sq_mul_n = 0;
    double denom_n = 0;
    for(int i=0; i<cores; i++){
        sq_sum_vals += sq_sum[i];
        mean_sq_mul_n += mean[i];
        denom_n += nm[i];
    }
    mean_sq_mul_n = mean_sq_mul_n * mean_sq_mul_n / denom_n;

    double std_approx = sqrt((sq_sum_vals - mean_sq_mul_n)/denom_n);
//    std::cout << "std: " << std_approx << std::endl;
    std::cout << std_approx << " ";

    auto stop = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);

//    std::cout << "Time taken by std approx function: "
//              << duration.count() << " microseconds" << std::endl;
}

template<class SM>
//void gat_forward(const SM * graph, const DM* h_l0, const DM* w_l0, DM* h_l, DM* w_l){
void approx_edge_entr(const SM * graph, int prec, double ver_num, double edge_num){
    auto start = std::chrono::high_resolution_clock::now();

    typedef typename SM::itype iT; // Node IDs
    typedef typename SM::ntype nT; // Edge IDs
    typedef typename SM::vtype vT; // Value of node

    int cores = 16;
    int rows = (int)graph->nrows();
    double entr[16] = {0};
    double edges[16] = {0};

    int rows_per_thread = rows / cores;

    double percen = (double) prec / 100.0;

    int limit[16];
#pragma omp parallel for
    for (int i=0; i<16; i++){
        if ((rows - rows_per_thread*i)<rows_per_thread){
            limit[i] = rows;
        } else {
            limit[i] = rows_per_thread * i + (int)(rows_per_thread * percen);
        }
    }

#pragma omp parallel for
    for(int i=0; i<cores; i++){
        double sum = 0;
        for(nT j=rows_per_thread*i; j<limit[i]; j++){
            nT e_0=graph->offset_ptr()[j];
            nT e_1=graph->offset_ptr()[j+1];
            nT diff_e = e_1 - e_0;

//            sum += ((-1) * diff_e * log( diff_e / edge_num ) / edge_num);
            sum += diff_e;
        }
        edges[i] = sum;
    }

    double prec_edges = 0;
    for(int i=0; i<cores; i++){
        prec_edges += edges[i];
    }

#pragma omp parallel for
    for(int i=0; i<cores; i++){
        double sum = 0;
        for(nT j=rows_per_thread*i; j<limit[i]; j++){
            nT e_0=graph->offset_ptr()[j];
            nT e_1=graph->offset_ptr()[j+1];
            nT diff_e = e_1 - e_0 + 1;

//            sum += ((-1) * diff_e * log( diff_e / edge_num ) / edge_num);
            sum += ((-1) * log( diff_e / prec_edges ) * diff_e);
        }
        entr[i] = sum;
    }

    double total_sum = 0;
    for(int i=0; i<cores; i++){
//        std::cout <<  i << " sum is: " << entr[i] << std::endl;
        total_sum += entr[i];
    }

    double entr_val = total_sum / prec_edges;
//    std::cout << "edge entr: " << entr_val << std::endl;
//    std::cout << "normalized edge entr: " << entr_val / log (ver_num) << std::endl;
    std::cout << entr_val << " " << entr_val / log (ver_num * percen) << " ";

    auto stop = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);
//
//    std::cout << "Time taken by edge entr approx function: "
//              << duration.count() << " microseconds" << std::endl;
}

template<class SM>
//void gat_forward(const SM * graph, const DM* h_l0, const DM* w_l0, DM* h_l, DM* w_l){
void approx_vert_entr(const SM * graph, int prec, double ver_num, double edge_num, int max_nm){
    auto start = std::chrono::high_resolution_clock::now();

    typedef typename SM::itype iT; // Node IDs
    typedef typename SM::ntype nT; // Edge IDs
    typedef typename SM::vtype vT; // Value of node

    int rows = (int)graph->nrows();
    nT* nodes_with_deg = new nT[max_nm];
    for(int i=0; i<max_nm; i++){
        nodes_with_deg[i] = 0;
    }

    int rows_per_thread = rows;

    double percen = (double) prec / 100.0;
    long iter_nm = (long)rows_per_thread * percen;

    for(nT j=0; j<iter_nm; j++){
        nT e_0=graph->offset_ptr()[j];
        nT e_1=graph->offset_ptr()[j+1];
        nT diff_e = e_1 - e_0;

        nodes_with_deg[diff_e] += 1;
    }

    double total_sum = 0;
    double per_ver_num = (double)iter_nm;
    for(nT i=0; i<max_nm; i++){
        nT vl = 1;
        if (nodes_with_deg[i] != 0){
            vl = nodes_with_deg[i];
        }
        total_sum += ((-1) * log( vl / per_ver_num ) * nodes_with_deg[i]);;
    }

    double entr_val = (total_sum / per_ver_num);
//    std::cout << "edge entr: " << entr_val << std::endl;
//    std::cout << "normalized edge entr: " << entr_val / log (ver_num) << std::endl;
    std::cout << entr_val << std::endl;

    auto stop = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);
//
//    std::cout << "Time taken by edge entr approx function: "
//              << duration.count() << " microseconds" << std::endl;
}

// TODO Edge entropy and degree entropy?

/*
* inc_mxv
* inc_mTxv
* SDDMM
*   specialize SDDMM
*     1. regular inner product based
*     2. where the input dense matrices are Nx1
* SPMM
*/
