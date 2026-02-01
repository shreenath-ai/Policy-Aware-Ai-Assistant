from rag import retrieve_policy

query = "What are the compliance requirements?"

result = retrieve_policy(query)

if result is None:
    print("❌ REFUSED: No policy evidence found")
else:
    print("✅ POLICY FOUND")
    for item in result:
        print(item[1])
