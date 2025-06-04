#include <mpi.h>
#include <cmath>
#include <iostream>
#include <vector>
#include <algorithm>
extern "C" {
#include <scalapack.h>
#include <blacs.h>
#include <blacspp.h>
}

using namespace std;

// Helper to print local matrix (for debugging)
void print_local_matrix(const vector<double>& local_A, int mloc, int nloc, int myrow, int mycol) {
    cout << "Local matrix on process (" << myrow << "," << mycol << "):\n";
    for (int i = 0; i < mloc; ++i) {
        for (int j = 0; j < nloc; ++j)
            cout << local_A[i + j * mloc] << " ";
        cout << endl;
    }
}

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int nprocs, myrank;
    MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);

    // Set up BLACS context and process grid
    int nprow = (int)std::sqrt(nprocs), npcol = nprocs / nprow;
    int myrow, mycol, ictxt, info;
    blacs_pinfo_(&myrank, &nprocs);
    blacs_get_(&ictxt, &ictxt, &ictxt);
    blacs_gridinit_(&ictxt, "Row", &nprow, &npcol);
    blacs_gridinfo_(&ictxt, &nprow, &npcol, &myrow, &mycol);

    // Global matrix size (example: 4x2)
    int m = 4, n = 2;
    int nb = 2; // Block size

    // Compute local matrix sizes
    int mloc = numroc_(&m, &nb, &myrow, &0, &nprow);
    int nloc = numroc_(&n, &nb, &mycol, &0, &npcol);

    // Allocate local matrix and fill with data (row-major for simplicity)
    vector<double> local_A(mloc * nloc, 0.0);
    // Only process 0 initializes the global matrix and distributes it
    if (myrank == 0) {
        vector<double> A = {
            1, 2,
            3, 4,
            5, 6,
            7, 8
        };
        // Distribute A to local_A (use pdelset or your own scatter)
        // For brevity, this is omitted here; see ScaLAPACK docs for details.
    }

    // Set up ScaLAPACK descriptors
    int descA[9], descU[9], descVT[9];
    int ZERO = 0, ONE = 1;
    int info_desc;
    descinit_(descA, &m, &n, &nb, &nb, &ZERO, &ZERO, &ictxt, &mloc, &info_desc);

    // Allocate output arrays
    int min_mn = std::min(m, n);
    vector<double> S(min_mn), U(mloc * mloc), VT(nloc * nloc), work(1);
    int lwork = -1;
    vector<double> rwork(1);
    int lrwork = -1;
    vector<int> iwork(8 * min_mn);

    // Workspace query
    pdgesvd_("V", "V", &m, &n, local_A.data(), &ONE, &ONE, descA,
             S.data(), U.data(), &ONE, &ONE, descU,
             VT.data(), &ONE, &ONE, descVT,
             work.data(), &lwork, rwork.data(), &lrwork, iwork.data(), &info);

    lwork = (int)work[0];
    work.resize(lwork);
    lrwork = (int)rwork[0];
    rwork.resize(lrwork);

    // Actual SVD computation
    pdgesvd_("V", "V", &m, &n, local_A.data(), &ONE, &ONE, descA,
             S.data(), U.data(), &ONE, &ONE, descU,
             VT.data(), &ONE, &ONE, descVT,
             work.data(), &lwork, rwork.data(), &lrwork, iwork.data(), &info);

    if (myrank == 0) {
        cout << "Singular values: ";
        for (int i = 0; i < min_mn; ++i)
            cout << S[i] << " ";
        cout << endl;
    }

    blacs_gridexit_(&ictxt);
    MPI_Finalize();
    return 0;
}