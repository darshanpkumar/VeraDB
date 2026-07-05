from backend.services.embedding_services import embed

# 1. Generate the feature embedding coordinates from the string input
vector = embed("Hello VeraDB")

# 2. Run system diagnostic print assertions
print(type(vector))
print(len(vector))
print(vector[:10])  # Show the first 10 floating point dimensional slices