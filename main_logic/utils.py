import urllib.request


def handle_uploaded_file(filename):
    questions = {}
    count = 0
    for i in filename:
        line = i.decode('utf-8')
        if line.startswith('#'):
            count += 1
            questions["question_" + str(count)] = [{"question": line[1:]}]
        elif line.startswith('$'):
            questions["question_" + str(count)].append({"option": line[1:]})
        elif line.startswith('&'):
            questions["question_" + str(count)].append({"answer": line[1:]})
    return questions
