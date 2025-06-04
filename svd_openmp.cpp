#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <omp.h>

using namespace std;

typedef vector<vector<double>> Matrix;

// Matrix multiplication: C = A * B
Matrix matmul(const Matrix& A, const Matrix& B) {
    int m = A.size(), n = B[0].size(), p = B.size();
    Matrix C(m, vector<double>(n, 0.0));
    #pragma omp parallel for
    for (int i = 0; i < m; ++i)
        for (int k = 0; k < p; ++k)
            for (int j = 0; j < n; ++j)
                C[i][j] += A[i][k] * B[k][j];
    return C;
}

// Transpose of a matrix
Matrix transpose(const Matrix& A) {
    int m = A.size(), n = A[0].size();
    Matrix AT(n, vector<double>(m));
    #pragma omp parallel for
    for (int i = 0; i < m; ++i)
        for (int j = 0; j < n; ++j)
            AT[j][i] = A[i][j];
    return AT;
}

// Jacobi eigenvalue algorithm for symmetric matrices (for simplicity, not optimized)
void jacobi_eigen(const Matrix& A, Matrix& V, vector<double>& eigvals, int max_iter = 100, double tol = 1e-10) {
    int n = A.size();
    Matrix D = A;
    V.assign(n, vector<double>(n, 0.0));
    for (int i = 0; i < n; ++i) V[i][i] = 1.0;

    for (int iter = 0; iter < max_iter; ++iter) {
        int p = 0, q = 1;
        double max_offdiag = 0.0;
        // Find largest off-diagonal element
        for (int i = 0; i < n; ++i)
            for (int j = i+1; j < n; ++j)
                if (fabs(D[i][j]) > max_offdiag) {
                    max_offdiag = fabs(D[i][j]);
                    p = i; q = j;
                }
        if (max_offdiag < tol) break;

        double phi = 0.5 * atan2(2 * D[p][q], D[q][q] - D[p][p]);
        double c = cos(phi), s = sin(phi);

        // Rotate
        for (int i = 0; i < n; ++i) {
            double dpi = D[i][p], dqi = D[i][q];
            D[i][p] = c * dpi - s * dqi;
            D[i][q] = s * dpi + c * dqi;
        }
        for (int i = 0; i < n; ++i) {
            double dip = D[p][i], diq = D[q][i];
            D[p][i] = c * dip - s * diq;
            D[q][i] = s * dip + c * diq;
        }
        D[p][p] = c * c * D[p][p] - 2 * s * c * D[p][q] + s * s * D[q][q];
        D[q][q] = s * s * D[p][p] + 2 * s * c * D[p][q] + c * c * D[q][q];
        D[p][q] = D[q][p] = 0.0;

        // Update eigenvectors
        for (int i = 0; i < n; ++i) {
            double vip = V[i][p], viq = V[i][q];
            V[i][p] = c * vip - s * viq;
            V[i][q] = s * vip + c * viq;
        }
    }
    eigvals.resize(n);
    for (int i = 0; i < n; ++i) eigvals[i] = D[i][i];
}

// SVD: A = U * S * V^T
void svd(const Matrix& A, Matrix& U, Matrix& S, Matrix& V) {
    int m = A.size(), n = A[0].size();
    Matrix AT = transpose(A);
    Matrix ATA = matmul(AT, A);

    // Eigen-decomposition of ATA to get V and singular values
    vector<double> eigvals;
    jacobi_eigen(ATA, V, eigvals);

    // Sort eigenvalues and corresponding vectors in descending order
    vector<pair<double, vector<double>>> eig_pairs;
    for (int i = 0; i < n; ++i)
        eig_pairs.push_back({eigvals[i], vector<double>(n)});
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            eig_pairs[i].second[j] = V[j][i];
    sort(eig_pairs.rbegin(), eig_pairs.rend());

    // Build V and singular values
    V.assign(n, vector<double>(n));
    vector<double> sigma(n, 0.0);
    for (int i = 0; i < n; ++i) {
        sigma[i] = sqrt(max(eig_pairs[i].first, 0.0));
        for (int j = 0; j < n; ++j)
            V[j][i] = eig_pairs[i].second[j];
    }

    // Build S (m x n diagonal)
    S.assign(m, vector<double>(n, 0.0));
    for (int i = 0; i < min(m, n); ++i)
        S[i][i] = sigma[i];

    // Compute U = (1/sigma_i) * A * v_i
    U.assign(m, vector<double>(m, 0.0));
    #pragma omp parallel for
    for (int i = 0; i < n; ++i) {
        if (sigma[i] > 1e-10) {
            vector<double> Av(m, 0.0);
            for (int row = 0; row < m; ++row)
                for (int col = 0; col < n; ++col)
                    Av[row] += A[row][col] * V[col][i];
            for (int row = 0; row < m; ++row)
                U[row][i] = Av[row] / sigma[i];
        }
    }
    // Fill remaining U columns with orthonormal vectors if needed (not shown for brevity)
}

void print_matrix(const Matrix& M, const string& name) {
    cout << name << " =\n";
    for (const auto& row : M) {
        for (double val : row)
            cout << val << "\t";
        cout << "\n";
    }
    cout << endl;
}

int main() {
    // Example: 3x2 matrix
    Matrix A = {{1, 2},
                {3, 4},
                {5, 6}};
    Matrix U, S, V;
    svd(A, U, S, V);

    print_matrix(U, "U");
    print_matrix(S, "S");
    print_matrix(V, "V");
    return 0;
}