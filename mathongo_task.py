import re
import json
with open('task.txt', 'r') as file:
    text = file.read()
def convert_to_json(text):
    
    questions = re.findall(r'Question ID: (\d+)(.*?)(?=Question ID: \d+|$)',
                           text, re.DOTALL)
   
    print(questions)
    json_output = []
    
    for i, (question_id, question_text) in enumerate(questions, start=1):
        question_dict = {}
        
        question_dict["questionNumber"] = i
        question_dict["questionId"] = int(question_id)
        question_dict["questionText"] = question_text.strip()
        
        options = []
        correct_option = None
        for line in question_text.strip().split('\n'):
            if line.startswith("(A)") or line.startswith("Answer"):
                correct_option = line.split()[-1].replace("(", "").replace(")", "")
            elif line.startswith("(B)") or line.startswith("(C)") or line.startswith("(D)"):
                option_text = line[4:]
                option_number = int(abs(ord('A')-ord(line[1])))
                is_correct = option_text.startswith(correct_option)
                options.append({"optionNumber": option_number, "optionText": option_text, "isCorrect": is_correct})
        
        question_dict["options"] = options
        
        solution_text = question_text.split("Sol.")[-1].strip()
        question_dict["solutionText"] = solution_text
        
        json_output.append(question_dict)
    
    return json_output

json_output = convert_to_json(text)
print(json_output)
# Convert the JSON output to a string
json_string = json.dumps(json_output, indent=4)

# Specify the file path where you want to save the JSON file
json_file_path = 'output.json'

# Write the JSON string to the file
with open(json_file_path, 'w') as json_file:
    json_file.write(json_string)

print("JSON file saved successfully.")



