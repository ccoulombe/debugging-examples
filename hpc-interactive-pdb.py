def heavy_computation_with_bug(matrix_size):
    print(f"Allocating a {matrix_size}x{matrix_size} matrix...")
    breakpoint()
    return matrix_size * 2

if __name__ == "__main__":
    result = heavy_computation_with_bug(10000)
    print(f"Result: {result}")
