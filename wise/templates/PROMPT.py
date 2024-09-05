qaPrompt = """
    You are assisting in filling a form using the given raw HTML of the form as well as the context given by the user. 
    The context given by the user contains answers to the questions in the form. You have to provide the following from the
    given data:
    1. Question text
    2. Answer text (if the question is multiple choice, send the text of the option(s) otherwise send a text for the input)
    3. Answer Relative XPath (if the question is multiple choice, send the XPath of the option(s) otherwise send a Relative XPath for the input box)
    4. The type of input (it is 'click' if it is a multiple choice question else return it as 'input' for short answer and long answer) else return None
    
    Note that if you are unable to find answer you have to return 'None'. Sometimes answers with multiple choice can have 
    multiple answers, hence send the answers and their relative XPath as lists.
    
    RAW HTML data:
    {raw_html}
    
    User Data:
    {prompt}
"""
