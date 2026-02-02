import json
import re

def compile_manual_to_ruleset(manual_path, ruleset_name = "default_ruleset"):
    rules = []
    variables = set()
    default_outcome = None

    #regEx patter: if CONDITION is true, classify as OUTCOME, \. is literal period
    rule_pattern = re.compile(r"If (.*) is true, classify as (.*)\.")
    default_pattern = re.compile(r"Otherwise classify as (.*)\.")

    with open(manual_path, 'r') as file:
        for line in file:
            chunk = json.loads(line)
            text = chunk['text']
            chunk_id = chunk['chunk_id']
            match = rule_pattern.match(text) #check if standard rule
            if match:
                condition = match.group(1).strip()
                outcome = match.group(2).strip()
                rule_id = f"R{len(rules) + 1}"
                rules.append({"id": rule_id, "when": condition, "then": outcome, "evidence": chunk_id})

                for v in re.split(r' AND | OR | NOT |\(|\)', condition): #split string at every occurance of AND OR NOT
                    clean_v = v.strip()
                    if clean_v and clean_v not in ['true', 'false']:
                        variables.add(clean_v)
                continue

            match = default_pattern.match(text)
            if match:
                default_outcome = match.group(1).strip()
    return {"name": ruleset_name, "variables": list(variables), "rules": rules, "default": default_outcome}

if __name__ == "__main__":
    # Path to your sample_manual_excerpt.jsonl
    reconstructed = compile_manual_to_ruleset('sample_manual_excerpt.jsonl')
    
    # Save the output
    with open('reconstructed_ruleset.json', 'w') as f:
        json.dump(reconstructed, f, indent=2)
    
    print("Reconstructed Ruleset created successfully!")