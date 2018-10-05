# encoding=utf8

class Rule:
    def __init__(self, frameName, question, answer) :
        self.question = question
        self.answer = answer
        self.frameName = frameName
        self.optional = []
        self.mandatory = []
        optional = False
        for word in question:
            if word == '[' :
                optional = True
            elif word == ']' :
                optional = False
            elif word[0] == '$' :
                if optional :
                    self.optional.append(word[1:])
                else:
                    self.mandatory.append(word[1:])                
        for word in answer:
            if word == '[' :
                optional = True
            elif word == ']' :
                optional = False
            elif word[0] == '$' :
                if optional :
                    self.optional.append(word[1:])
                else:
                    self.mandatory.append(word[1:])                

    def isApplicable(self, frame) :
        if self.frameName != frame.semanticFrame:
            return False
        for m in self.mandatory :
            if m not in frame.frameElements:
                return False
        return True
        
             
    def apply(self, frame, corefs):
        questions = []
        answers = []
        if not self.isApplicable(frame) :
            return questions, answers
        newQuestion = ''
        newAnswer = ''
        optional = False
        tmp = ''
        for word in self.question :
            if word == '[' :
                flag = False
                optional = True
            elif word == ']' :
                optional = False
                if flag :
                    newQuestion += tmp 
            elif word[0] != '$' :
                if optional :
                    tmp += word + ' '
                else : 
                    newQuestion += word + ' '
            else :    
                frameElement = word[1:]
                if optional : 
                    if frameElement in frame.frameElements:
                        flag = True
                        tmp += frame.frameElements[frameElement].getStringOfSuperficialForm()
                else :
                    newQuestion += frame.frameElements[frameElement].getStringOfSuperficialForm() 


        for word in self.answer :
            if word == '[' :
                flag = False
                optional = True
            elif word == ']' :
                optional == False
                if flag :
                    newAnswer += tmp 
            elif word[0] != '$' :
                if optional :
                    tmp += word
                else : 
                    newAnswer += word + ' '
            else :    
                frameElement = word[1:]
                if optional : 
                    if frameElement in frame.frameElements:
                        flag = True
                        tmp += frame.frameElements[frameElement].getStringOfSuperficialForm() 
                else :
                    newAnswer += frame.frameElements[frameElement].getStringOfSuperficialForm() 

            
        questions.append(newQuestion)
        answers.append(newAnswer)
               
        return questions, answers
    
    def __str__(self) :
        s = "Question applicable à la frame : " + self.frameName + '\nQuestion : ' 
        for word in self.question :
            s += word + ' '
        s += '\nRéponse : '
        for word in self.answer :
            s += word + ' '
        return s
