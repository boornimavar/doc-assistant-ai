import pickle

with open("documents.pkl", "rb") as f:
    data = pickle.load(f)

print("Type of data:", type(data))
print()

if isinstance(data, list):
    print(f"It's a list with {len(data)} items.")
    print("First item:")
    print(data[0])
elif isinstance(data, dict):
    print(f"It's a dictionary with {len(data)} keys.")
    print("First few keys:", list(data.keys())[:5])
    first_key = list(data.keys())[0]
    print(f"Value for '{first_key}':")
    print(data[first_key])
else:
    print("Contents:")
    print(data)
