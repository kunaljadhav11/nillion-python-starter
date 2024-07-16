# /content/nillion-python-starter/quickstart/client_code/run_my_first_program.py


import os
from dotenv import load_dotenv
from py_nillion_client import NillionClient, Party, ProgramInputs

# Load environment variables
load_dotenv("/root/.config/nillion/nillion-devnet.env")

# Initialize Nillion client
client = NillionClient(
    cluster_id=os.getenv("NILLION_CLUSTER_ID"),
    bootnode_multiaddress=os.getenv("NILLION_BOOTNODE_MULTIADDRESS"),
    nilchain=os.getenv("NILLION_NILCHAIN_JSON_RPC"),
)

# Define parties
author = Party(name="Author", private_key=os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))
reviewers = [
    Party(name=f"Reviewer{i}", private_key=os.getenv(f"NILLION_NILCHAIN_PRIVATE_KEY_{i+1}"))
    for i in range(3)
]
committee = Party(name="Committee", private_key=os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_4"))

# Prepare inputs
inputs = ProgramInputs()
# In the Python client code (run_peer_review.py)
inputs.add_secret_input("paper_quality", 8.0, author)  # Use float values
inputs.add_secret_input("review0", 7.0, reviewers[0])
inputs.add_secret_input("review1", 9.0, reviewers[1])
inputs.add_secret_input("review2", 8.0, reviewers[2])

# Run the program
result = client.run_program(
    program_name="main",
    program_path="/content/nillion-python-starter/quickstart/nada_quickstart_programs/target/main.nada.bin",
    inputs=inputs,
)

# Print the results
print(f"Final Score: {result['final_score']}")
print(f"Author's self-assessment was realistic: {result['realistic_self_assessment']}")
for i in range(3):
    print(f"Reviewer {i} is an outlier: {result[f'reviewer{i}_outlier']}")