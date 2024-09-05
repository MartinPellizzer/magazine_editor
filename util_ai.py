import util

def prompt_normalize(prompt):
    return '\n'.join([line.strip() for line in prompt.split('\n') if line.strip() != ''])

def reply_list_to_paragraph(reply):
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue

        if not line[0].isdigit(): continue
        if '. ' not in line: continue
        else: line = '. '.join(line.split('. ')[1:]).strip()
        
        reply_formatted.append(line)

    return ' '.join(reply_formatted)

def text_to_paragraph(reply):
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue

        if line[0].isdigit(): 
            if '. ' in line: 
                line = '. '.join(line.split('. ')[1:]).strip()
        
        reply_formatted.append(line.strip())

    return ' '.join(reply_formatted)




