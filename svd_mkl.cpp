#include <iostream>
#include <vector>
#include <iomanip>
#include <mkl.h>
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

// Matrix multiplication using MKL BLAS (C = A * B)
Matrix matmul(const Matrix& A, const Matrix& B) {
    int m = A.size();
    int k = A[0].size();
    int n = B[0].size();
    Matrix C(m, vector<double>(n, 0.0));
    vector<double> a(m * k), b(k * n), c(m * n);

    // Convert A and B to column-major 1D arrays
    for (int i = 0; i < m; ++i)
        for (int j = 0; j < k; ++j)
            a[j * m + i] = A[i][j];
    for (int i = 0; i < k; ++i)
        for (int j = 0; j < n; ++j)
            b[j * k + i] = B[i][j];

    // C = A * B
    cblas_dgemm(CblasColMajor, CblasNoTrans, CblasNoTrans,
                m, n, k, 1.0, a.data(), m, b.data(), k, 0.0, c.data(), m);

    // Convert result back to Matrix
    for (int i = 0; i < m; ++i)
        for (int j = 0; j < n; ++j)
            C[i][j] = c[j * m + i];
    return C;
}

// SVD using Intel MKL LAPACKE_dgesvd
bool compute_svd_mkl(const Matrix& A, Matrix& U, Matrix& S, Matrix& VT) {
    int m = A.size();
    int n = A[0].size();
    vector<double> a(m * n);

    // Flatten A to column-major
    for (int i = 0; i < m; ++i)
        for (int j = 0; j < n; ++j)
            a[j * m + i] = A[i][j];

    int lda = m;
    int ldu = m;
    int ldvt = n;
    vector<double> s(min(m, n));
    vector<double> u(ldu * m);
    vector<double> vt(ldvt * n);
    vector<double> superb(min(m, n) - 1);

    int info = LAPACKE_dgesvd(LAPACK_COL_MAJOR, 'A', 'A',
                              m, n, a.data(), lda,
                              s.data(), u.data(), ldu,
                              vt.data(), ldvt, superb.data());

    if (info > 0) {
        cout << "SVD did not converge.\n";
        return false;
    }

    // Convert results to Matrix form
    U.assign(m, vector<double>(m));
    S.assign(m, vector<double>(n, 0.0));
    VT.assign(n, vector<double>(n));

    for (int i = 0; i < m; ++i)
        for (int j = 0; j < m; ++j)
            U[i][j] = u[j * m + i];

    for (int i = 0; i < min(m, n); ++i)
        S[i][i] = s[i];

    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            VT[i][j] = vt[j * n + i];

    return true;
}

int main() {
    // Example: 3x2 matrix
    int m = 3, n = 2;
    Matrix A = {{1, 2},
                {3, 4},
                {5, 6}};

    Matrix U, S, VT;
    if (!compute_svd_mkl(A, U, S, VT)) {
        return 1;
    }

    print_matrix(U, "U");
    print_matrix(S, "S");
    print_matrix(VT, "VT");

    // Example: Multiply U * S * VT using MKL BLAS
    Matrix US = matmul(U, S);
    Matrix USVT = matmul(US, VT);
    print_matrix(USVT, "U*S*VT (should approximate original A)");

    return 0;
}