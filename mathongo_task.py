import re
import json

def convert_to_json(text):
    questions = re.findall(r'Question ID: (\d+)(.*?)(?=Question ID: \d+|$)', text, re.DOTALL)
    json_output = []
    
    for i, (question_id, question_text) in enumerate(questions, start=1):
        question_dict = {}
        
        question_dict["questionNumber"] = i
        question_dict["questionId"] = int(question_id)
        
        
        question_match = re.match(r'(.*?)\n(?:\(A\)|\(B\)|\(C\)|\(D\))', question_text, re.DOTALL)
        if question_match:
            question_dict["questionText"] = question_match.group(1).strip()
        
        options = []
        answer = None
        
        
        answer_match = re.search(r'Answer\s*\(([A-D])\)', question_text)
        if answer_match:
            answer = answer_match.group(1)
        
        for line in question_text.strip().split('\n'):
            if line.startswith("(A)") or line.startswith("(B)") or line.startswith("(C)") or line.startswith("(D)"):
                option_text = line[4:]
                
                option_number = int(abs(ord('A')-ord(line[1])))
                
                
                is_correct = (answer == line[1])
                
                options.append({"optionNumber": option_number, "optionText": option_text, "isCorrect": is_correct})
        
        question_dict["options"] = options
        
        solution_text = question_text.split("Sol.")[-1].strip()
        
        solution_text = solution_text.replace("\\section*{", "")
        question_dict["solutionText"] = solution_text
        
        json_output.append(question_dict)
    
    return json_output


with open('task.txt', 'r') as file:
    text = file.read()


json_output = convert_to_json(text)


json_string = json.dumps(json_output, indent=4)


json_file_path = 'output.json'


with open(json_file_path, 'w') as json_file:
    json_file.write(json_string)

print("JSON file saved successfully.")





