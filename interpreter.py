import json
import re

class DMNInterpreter:
    def __init__(self, ruleset_path: str):
        with open(ruleset_path, 'r') as file:
            self.ruleset = json.load(file)
        self.variables = self.ruleset.get('variables', []) # returns an empty list if no variables found
        self.rules = self.ruleset.get('rules', [])
        self.default = self.ruleset.get('default', 'DEFAULT')
    
    def lint(self):
        warnings = []
        seen_conditions = set()
        only_true = False
        prev_condition_sets = [] #list of sets for finding subsets such as condition A in rule 1 and then condition A AND B in rule 2 or after

        for i, rule in enumerate(self.rules):
            rule_id = rule['id']
            condition = rule['when'].strip().lower()
            
            if only_true: # if a rule is simply only true/always true, no rule after that will ever be evaluated and is unreachable
                warnings.append(f"Warning: Rule {rule_id} is unreachable because previous rule is always true")
            
            if condition == "true":
                only_true = True

            #check for duplicate conditions
            if condition in seen_conditions:
                warnings.append(f"Warning: Rule {rule_id} is unreachable because it is a duplicate of another rule's condition: {condition}")
            seen_conditions.add(condition)

            #checking if there is a broader condition in a previous rule like A first and then A and B, if A is true then A and B will never run
            current_vars = set(re.findall(r'\b\w+\b', condition)) #returns a list of all substrings that seem like words and turns them into a set
            current_vars -= {'and', 'or', 'not', 'true', 'false'}

            for prev in prev_condition_sets:
                #if previous rule's condition is a subset of the current rule's condition, then the current rule might not be reachable so we print
                if prev and prev.issubset(current_vars):
                    warnings.append(f"WARNING: Rule {rule['id']} may be shadowed by a previous rule. " f"Logic in {prev} already captures these cases.")
            
            prev_condition_sets.append(current_vars)
        
        if not warnings:
            print("No warnings found. Ruleset is valid.")
        else:
            print("\nLinting results:")
            for warning in warnings:
                print(warning)
            print("\nPlease review the warnings and adjust the ruleset accordingly.")
        
        return warnings


    def evaluate_condition(self, condition, patient):
        words = condition.replace('(', ' ( ').replace(')', ' ) ').split() #tokenize
        for word in words:
            if word not in ['AND', 'OR', 'NOT', '(', ')', 'true', 'false'] and word not in self.variables:
                raise ValueError(f"Error: Unknown variable referenced: {word}")
        #convert to python syntax
        condition_py = condition.replace('OR', ' or ').replace('AND', ' and ').replace('NOT', ' not ').replace('true', 'True').replace('false', 'False')

        try:
            return eval(condition_py, {"__builtins__": None}, patient)
        except Exception as e:
            raise ValueError(f"Error: Invalid expression syntax '{condition}': {e}")

    def run_patient(self, patient):
        path = []
        match_rule = None
        outcome = self.default #default outcome

        for v in self.variables:
            if v not in patient:
                raise ValueError(f"Error: Patient {patient.get('id')} is missing variable: {v}")
        
        #evaluate rules
        for rule in self.rules:
            path.append(rule['id'])
            if self.evaluate_condition(rule['when'], patient):
                match_rule = rule['id']
                outcome = rule['then']
                break

        return {
            "patient_id": patient.get('id'),
            "outcome": outcome,
            "matched_rule": match_rule or "default",
            "path": path,
        }
if __name__ == "__main__":
    interpreter = DMNInterpreter("sample_ruleset.json")