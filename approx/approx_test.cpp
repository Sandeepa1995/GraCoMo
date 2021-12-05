#include "../utils/mtx_io.h"
#include "../objects/csrc_matrix.h"
#include "../gnn/approx.h"

#include <iostream>

// definitions for data types
typedef uint32_t ind1_t; // Node ids
typedef uint64_t ind2_t; // Edge ids
typedef double val_t; // Values

int main(int argc, char** argv) {
    using namespace std;

    // Load graph / adjacency matrix
    std::cout << "Size of value data type = " << sizeof(val_t) << std::endl;
    std::cout << "Size of col/row id data type = " << sizeof(ind1_t) << std::endl;
    std::cout << "Size of edge id data type = " << sizeof(ind2_t) << std::endl;
    std::string filename = argv[1];
    MtxIO<ind1_t, ind2_t, val_t> reader;
    reader.readMtx(filename);
    ind1_t nrows, ncols;
    ind2_t nvals;
    ind2_t size;
    ind1_t *col_ids, *row_ids;
    val_t* vals;
    reader.getData(nrows, ncols, nvals, size, row_ids, col_ids, vals);
    cout << "Matrix: " << reader.mtx_name() << endl;
    cout << "Nrows: " << nrows << " Ncols: " << ncols << " Nvals: " << nvals << " size: " << size << endl;
    CSRCMatrix<ind1_t, ind2_t, val_t> mtx;
    mtx.build(nrows, ncols, nvals, row_ids, col_ids, vals, CSRCMatrix<ind1_t, ind2_t, val_t>::CSRC_TYPE::CSR);

    int prec = 100;
    if (nrows <= 1000){
        prec = 80;
    } else if (nrows <= 10000){
        prec = 50;
    } else if (nrows <= 100000){
        prec = 30;
    } else if (nrows <= 1000000){
        prec = 10;
    } else {
        prec = 1;
    }

    int min_max[2] = {0};
    double edge_num = (double)nvals;
    approx_range<CSRCMatrix<ind1_t, ind2_t, val_t>>(&mtx, prec, min_max);
    approx_sdiv<CSRCMatrix<ind1_t, ind2_t, val_t>>(&mtx, prec);
    approx_edge_entr<CSRCMatrix<ind1_t, ind2_t, val_t>>(&mtx, prec, nrows, edge_num);
    approx_vert_entr<CSRCMatrix<ind1_t, ind2_t, val_t>>(&mtx, prec, nrows, edge_num, min_max[1]);

//    std::cout << "Can get min max out: " << min_max[1] << std::endl;

    return 0;
}