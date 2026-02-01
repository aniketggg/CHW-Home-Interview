import json

class DMNInterpreter:
    def __init__(self, ruleset_path: str):
        with open(ruleset_path, 'r') as file:
            self.ruleset = json.load(file)
        self.variables = self.ruleset.get('variables', []) # returns an empty list if no variables found
        self.rules = self.ruleset.get('rules', [])
        self.default = self.ruleset.get('default', 'DEFAULT')

    def evaluate_condition(self, condition, patient):
        words = condition.replace('(', ' ( ').replace(')', ' ) ').split() #tokenize
        for word in words:
            if word not in ['AND', 'OR', 'NOT', '(', ')', 'true', 'false'] and word not in self.variables:
                raise ValueError(f"Error: Unknown variable referenced: {word}")
        #convert to python syntax
        condition_py = condition.replace('OR', ' or ').replace('AND', ' and ').replace('NOT', ' not ')

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