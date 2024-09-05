from langchain.output_parsers import ResponseSchema

qa_response_schema = [
    ResponseSchema(
        name="question",
        description="The question extracted from the HTML.",
    ),
    ResponseSchema(
        name="answer_pairs",
        description="List of pairs containing the answer and its corresponding XPath.",
        type="array",
        items={
            "type": "object",
            "properties": {
                "answer": {
                    "type": "string",
                    "description": "The answer found in the context.",
                },
                "answer_xpath": {
                    "type": "string",
                    "description": "The XPath corresponding to the answer or input box.",
                },
            },
            "required": ["answer", "answer_xpath"],
        },
    ),
    ResponseSchema(
        name="input_data_type",
        description="Data type of the input required for the question.",
    ),
]
