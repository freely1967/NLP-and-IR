import re
"""Boolean Search with Debugging."""
def boolean_search(query, docs):
    """Boolean-Search with simple use of  AND, OR, NOT operators."""
    query = query.lower().strip()
   
    results = []
    
    for title, content in docs.items():
        content = content.lower()
        
        if " and " in query:
            terms = [term.strip() for term in query.split(" and ")]
            match = all(term in content for term in terms)
            print(f"🔎 AND-Search: {title} | Terms: {terms} | Match: {match}")  # Debugging
            if match:
                results.append(title)
        
        elif " or " in query:
            terms = [term.strip() for term in query.split(" or ")]
            match = any(term in content for term in terms)
            print(f"🔎 OR-Search: {title} | Terms: {terms} | Match: {match}")  # Debugging
            if match:
                results.append(title)

        elif " not " in query:
            term1, term2 = [term.strip() for term in query.split(" not ")]
            match = term1 in content and term2 not in content
            print(f"🔎 NOT-Search: {title} | {term1} found: {term1 in content}, {term2} excluded: {term2 not in content}")  # Debugging
            if match:
                results.append(title)

        else:
            match = query in content
            print(f"🔎 Simple Search: {title} | Query: {query} | Match: {match}")  # Debugging
            if match:
                results.append(title)
    
    return results
