#include <iostream>
#include <vector>
#include <iomanip>
#include <lapacke.h>

using namespace std;

typedef vector<vector<double>> Matrix;

// Helper to print a matrix
void print_matrix(const Matrix& M, const string& name) {
    cout << name << " =\n";
    for (const auto& row : M) {
        for (double val : row)
            cout << setw(12) << val << " ";
        cout << "\n";
    }
    cout << endl;
}

int main() {
    // Example: 3x2 matrix
    int m = 3, n = 2;
    Matrix A = {{1, 2},
                {3, 4},
                {5, 6}};

    // LAPACK uses column-major order, so flatten A accordingly
    vector<double> a(m * n);
    for (int i = 0; i < m; ++i)
        for (int j = 0; j < n; ++j)
            a[j * m + i] = A[i][j];

    // Prepare outputs
    int lda = m;
    int ldu = m;
    int ldvt = n;
    vector<double> s(min(m, n));         // singular values
    vector<double> u(ldu * m);           // left singular vectors
    vector<double> vt(ldvt * n);         // right singular vectors (transposed)
    vector<double> superb(min(m, n) - 1);

    // Compute SVD using LAPACKE_dgesvd (all singular vectors)
    int info = LAPACKE_dgesvd(LAPACK_COL_MAJOR, 'A', 'A',
                              m, n, a.data(), lda,
                              s.data(), u.data(), ldu,
                              vt.data(), ldvt, superb.data());

    if (info > 0) {
        cout << "SVD did not converge.\n";
        return 1;
    }

    // Convert results to Matrix form for printing
    Matrix U(m, vector<double>(m));
    Matrix S(m, vector<double>(n, 0.0));
    Matrix VT(n, vector<double>(n));

    // U is m x m, column-major
    for (int i = 0; i < m; ++i)
        for (int j = 0; j < m; ++j)
            U[i][j] = u[j * m + i];

    // S is diagonal
    for (int i = 0; i < min(m, n); ++i)
        S[i][i] = s[i];

    // VT is n x n, column-major
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            VT[i][j] = vt[j * n + i];

    print_matrix(U, "U");
    print_matrix(S, "S");
    print_matrix(VT, "VT");

    return 0;
}