import json
import os
from interpreter import DMNInterpreter
from mermaid import generate_mermaid_diagram
from compiler import compile_manual_to_ruleset

def run_project():
    MANUAL_PATH = 'sample_manual_excerpt.jsonl'
    #MANUAL_PATH = 'test_lint.jsonl'
    PATIENTS_PATH = 'sample_patients.jsonl'
    ORIGINAL_RULESET_PATH = 'sample_ruleset.json' # Used for Mermaid generation
    
    #Compile manual to ruleset
    print("Compiling manual to ruleset:")
    reconstructed_ruleset = compile_manual_to_ruleset(MANUAL_PATH)
    with open('reconstructed_ruleset.json', 'w') as f:
        json.dump(reconstructed_ruleset, f, indent=2)
    
    # generate mermaid diagram
    print("Generating mermaid diagram:")
    mermaid_diagram = generate_mermaid_diagram(ORIGINAL_RULESET_PATH)
    with open('ruleset_flowchart.mmd', 'w') as f:
        f.write(mermaid_diagram)
    
    evidence_map = {r['id']: r.get('evidence') for r in reconstructed_ruleset['rules']}
    
    #initialize interpreter with ruleset
    interpreter = DMNInterpreter('reconstructed_ruleset.json')
    results = []

    #running lint mode:
    print("Running lint mode:")
    lint_warnings = interpreter.lint()
    print("\n")
    
    #running patient mode:
    print("Running patient mode:")
    if not os.path.exists(PATIENTS_PATH):
        print(f"Error: Patients file not found at {PATIENTS_PATH}")
        return
    
    with open(PATIENTS_PATH, 'r') as f:
        for line in f:
            if not line.strip(): continue
            patient_data = json.loads(line)
            res = interpreter.run_patient(patient_data)
            matched_rule = res['matched_rule']

            if matched_rule != "default":
                res['justification'] = f"Patient met criteria for Rule {matched_rule}."
                res['evidence'] = evidence_map.get(matched_rule)
            else:
                res['justification'] = "No clinical rules matched. Applied fallback/default classification."
                res['evidence'] = "C4"
            results.append(res)
    # save results in output JSON file
    with open('interpreter_output.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Success: processed {len(results)} patients into 'interpreter_output.json'")

    print("\nAnalysis complete!")

if __name__ == "__main__":
    try:
        run_project()
    except Exception as e:
        print(f"Error: {e}")
        print("Please check the file paths and try again.")