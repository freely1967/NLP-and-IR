import re

"""Boolean Search with Case-Sensitive Operators."""
def boolean_search(query, docs):
    """Boolean-Search with case-sensitive AND, OR, NOT operators."""
    
    # Suche nach den case-sensitive Operatoren mit Regex
    and_match = re.search(r"\bAND\b", query)
    or_match = re.search(r"\bOR\b", query)
    not_match = re.search(r"\bNOT\b", query)

    results = []
    
    for title, content in docs.items():
        content_lower = content.lower()  # Dokumente bleiben case-insensitive
        
        if and_match:
            terms = [term.strip() for term in re.split(r"\bAND\b", query)]
            match = all(term.lower() in content_lower for term in terms)
            print(f"🔎 AND-Search: {title} | Terms: {terms} | Match: {match}")  # Debugging
            if match:
                results.append(title)
        
        elif or_match:
            terms = [term.strip() for term in re.split(r"\bOR\b", query)]
            match = any(term.lower() in content_lower for term in terms)
            print(f"🔎 OR-Search: {title} | Terms: {terms} | Match: {match}")  # Debugging
            if match:
                results.append(title)

        elif not_match:
            term1, term2 = [term.strip() for term in re.split(r"\bNOT\b", query)]
            match = term1.lower() in content_lower and term2.lower() not in content_lower
            print(f"🔎 NOT-Search: {title} | {term1} found: {term1.lower() in content_lower}, {term2} excluded: {term2.lower() not in content_lower}")  # Debugging
            if match:
                results.append(title)

        else:
            match = query.lower() in content_lower
            print(f"🔎 Simple Search: {title} | Query: {query} | Match: {match}")  # Debugging
            if match:
                results.append(title)
    
    return results
