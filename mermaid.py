import json

def generate_mermaid_diagram(path):
    with open(path, 'r') as file:
        data = json.load(file)
    rules = data.get('rules', [])
    default = data.get('default', 'DEFAULT')

    diagram = ["flowchart TD", "   Start(Start) --> R1"] #start diagram by going through the first rule

    for i, rule in enumerate(rules):
        rule_id = rule['id']
        condition = rule['when']
        outcome = rule['then']

        #current
        diagram.append(f"    {rule_id}{{{rule_id}: {condition}}}")

        #yes path
        diagram.append(f"    {rule_id} -- Yes --> {rule_id}_OUT[{outcome}]")
        #no path, go to next rule or if at the end, then default
        if i < len(rules) - 1:
            next_id = rules[i+1]['id']
            diagram.append(f"    {rule_id} -- No --> {next_id}") #point to next rule
        else:
            diagram.append(f"    {rule_id} -- No --> Default[{default}]") #point to default
    return "\n".join(diagram)

if __name__ == "__main__":
    output = generate_mermaid_diagram('sample_ruleset.json')
    print(output)
    with open('ruleset_flowchart.mmd', 'w') as f:
        f.write(output)


