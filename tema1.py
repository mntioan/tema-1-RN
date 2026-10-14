
import pathlib

def load_system(path: pathlib.Path) -> tuple[list[list[float]], list[float]]:
    A = []
    B = []
    with open(path) as f:
        for l in f:
            if l.strip() == "":
                continue
            t = l.split()
            B.append(float(t[-1]))
            st = "".join(t[:-2])  
            rd = []
            c = ""
            for ch in st:
                if ch in "xyz":
                    if c == "" or c == "+":
                        rd.append(1.0)
                    elif c == "-":
                        rd.append(-1.0)
                    else:
                        rd.append(float(c))
                    c = ""
                else:
                    c += ch
            A.append(rd)
    return A, B

A, B = load_system(pathlib.Path("system.txt"))
print(f"{A=} {B=}")


def determinant(matrix: list[list[float]]) -> float:
    a = matrix
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))

print(f"{determinant(A)=}")


def trace(matrix: list[list[float]]) -> float:
    s = 0
    for i in range(3):
        s += matrix[i][i]
    return s

print(f"{trace(A)=}")


def norm(vector: list[float]) -> float:
    s = 0
    for v in vector:
        s += v ** 2
    return s ** 0.5

print(f"{norm(B)=}")


def transpose(matrix: list[list[float]]) -> list[list[float]]:
    t = []
    for i in range(3):
        t.append([matrix[0][i], matrix[1][i], matrix[2][i]])
    return t

print(f"{transpose(A)=}")


def multiply(matrix: list[list[float]], vector: list[float]) -> list[float]:
    r = []
    for rd in matrix:
        r.append(rd[0] * vector[0] + rd[1] * vector[1] + rd[2] * vector[2])
    return r

print(f"{multiply(A, B)=}")


def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det = determinant(matrix)
    sol = []
    for k in range(3):
        m = [rd[:] for rd in matrix]
        for i in range(3):
            m[i][k] = vector[i]
        sol.append(determinant(m) / det)
    return sol

print(f"{solve_cramer(A, B)=}")


def minor(matrix: list[list[float]], i: int, j: int) -> list[list[float]]:
    M = []
    for r in range(3):
        if r == i:
            continue
        M.append([matrix[r][c] for c in range(3) if c != j])
    return M

def cofactor(matrix: list[list[float]]) -> list[list[float]]:
    C = []
    for i in range(3):
        rd = []
        for j in range(3):
            M = minor(matrix, i, j)
            d = M[0][0] * M[1][1] - M[0][1] * M[1][0]
            rd.append((-1) ** (i + j) * d)
        C.append(rd)
    return C

def adjoint(matrix: list[list[float]]) -> list[list[float]]:
    return transpose(cofactor(matrix))

def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det = determinant(matrix)
    adj = adjoint(matrix)
    inv = [[x / det for x in rd] for rd in adj]
    return multiply(inv, vector)

print(f"{solve(A, B)=}")