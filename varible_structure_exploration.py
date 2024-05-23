# from GPT-4o

import scipy.io

# Load the .mat file
mat_file_path = 'example.mat'
data = scipy.io.loadmat(mat_file_path)

# Assuming 'V' is one of the keys
V = data['V']

# Function to explore the structure of the variable
def explore_variable_structure(var):
    print("Type of variable:", type(var))
    
    if isinstance(var, np.ndarray):
        print("Shape of variable:", var.shape)
        print("Data type of variable:", var.dtype)
        print("First few elements of variable:", var.flat[:5])
    elif isinstance(var, dict):
        print("Keys in variable:", var.keys())
        for key in var:
            print(f"Key: {key}, Type of value: {type(var[key])}")
            explore_variable_structure(var[key])  # Recursive exploration
    elif hasattr(var, 'dtype') and var.dtype.names is not None:  # Structured array
        print("Fields in variable:", var.dtype.names)
        for field in var.dtype.names:
            print(f"Field: {field}, Data type: {var[field].dtype}, Shape: {var[field].shape}")
    else:
        print("Contents of variable:", var)

# Explore the structure of V
explore_variable_structure(V)
