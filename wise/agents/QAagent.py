import os

from attr.validators import optional
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.core.output_parsers import LangchainOutputParser
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
import json
import ast


class QAagent:
    def __init__(self, data_dir="data"):
        api_key = os.environ["GROQ_API_KEY"]

        embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
        Settings.embedding_model = embed_model

        Settings.context_window = 4096
        Settings.num_output = 256

        documents = SimpleDirectoryReader(data_dir).load_data()
        self.index = VectorStoreIndex.from_documents(documents, embed_model=embed_model,)

        response_schemas = [
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
                            "description": "The answer found in the context."
                        },
                        "answer_xpath": {
                            "type": "string",
                            "description": "The XPath corresponding to the answer or input box."
                        }
                    },
                    "required": ["answer", "answer_xpath"]
                }
            ),
            ResponseSchema(
                name="input_data_type",
                description="Data type of the input required for the question.",
            ),
        ]
        lc_output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        self.llm = Groq(
            model="mixtral-8x7b-32768",
            api_key=api_key,
            temperature=0.5,
            output_parser= LangchainOutputParser(lc_output_parser)
        )
        self.query_engine = self.index.as_query_engine(llm=self.llm)

    def chat(self, prompt: str):
        response = self.query_engine.query(prompt)

        try:
            data_dict = ast.literal_eval(str(response))
            json_response = json.dumps(data_dict, indent=4)
            return json_response
        except json.JSONDecodeError:
            return f"Invalid JSON response: {type(str(response))}"


if __name__ == "__main__":
    agent = QAagent("/home/kausthub-kannan/Projects/WISE/data")
    prompt = """
    You are assisting in filling a form using the given raw HTML of the form as well as the context given by the user. 
    The context given by the user contains answers to the questions in the form. You have to provide the following from the
    given data:
    1. Question text
    2. Answer text (if the question is multiple choice, send the text of the option(s) otherwise send a text for the input)
    3. Answer XPath (if the question is multiple choice, send the XPath of the option(s) otherwise send a XPath for the input box)
    4. Data type of the input (text, integer, click for options)
    
    Note that if you are unable to find answer you have to return 'None'. Sometimes answers with multiple choice can have 
    multiple answers, hence send the answers and their xpaths as lists.
    
    <div class="Qr7Oae" role="listitem"><div jsmodel="CP1oW" data-params="%.@.[1795050495,&quot;Are you a new or existing customer?&quot;,&quot;&quot;,2,[[1000057,[[&quot;I am a new customer&quot;,null,null,null,false],[&quot;I am an existing customer&quot;,null,null,null,false]],true,null,null,null,null,null,false,null,[]]],null,null,null,null,null,null,[null,&quot;Are you a new or existing customer?&quot;],[null,&quot;&quot;]],&quot;i1&quot;,&quot;i2&quot;,&quot;i3&quot;,false]"><div jscontroller="sWGJ4b" jsaction="EEvAHc:yfX9oc;" jsname="WsjYwc" class="geS5n"><div class="z12JJ"><div class="M4DNQ"><div id="i1" class="HoXoMd D1wxyf RjsPE" role="heading" aria-level="3" aria-describedby="i4"><span class="M7eMe">Are you a new or existing customer?</span><span class="vnumgf" id="i4" aria-label="Required question"> *</span></div><div class="gubaDc OIC90c RjsPE" id="i2"></div></div></div><div jscontroller="UmOCme" jsaction="rcuQ6b:vZc4S;O22p3e:zjh6rb;b2trFe:eVidQc;JIbuQc:RgMCxe(YlCLKb);sPvj8e:d3sQLd;TYy3Ne:RgMCxe;" class="oyXaNc" jsname="GCYh9b"><input type="hidden" name="entry.1000057_sentinel" jsname="DTMEae"><div jscontroller="eFy6Rc" jsaction="sPvj8e:Gh295d" jsname="cnAzRb"><div class="lLfZXe fnxRtf cNDBpf" jscontroller="wPRNsd" jsshadow="" jsaction="keydown:I481le;JIbuQc:JIbuQc;rcuQ6b:rcuQ6b" jsname="wCJL8" aria-labelledby="i1" aria-describedby="i2 i3" aria-required="true" role="radiogroup"><span jsslot="" role="presentation" jsname="bN97Pc" class="H2Gmcc tyNBNd"><div class="SG0AAe"><div class="nWQGrd zwllIb"><label for="i5" class="docssharedWizToggleLabeledContainer ajBQVb RDPZE"><div class="bzfPab wFGF8"><div class="d7L4fc bJNwt  FXLARc aomaEc ECvBRb"><div id="i5" class="Od2TWd hYsg7c RDPZE" jscontroller="EcW08c" jsaction="keydown:I481le;dyRcpb:dyRcpb;click:cOuCgd; mousedown:UX7yZ; mouseup:lbsD7e; mouseenter:tfO1Yc; mouseleave:JywGue; focus:AHmuwe; blur:O22p3e; contextmenu:mg9Pef;touchstart:p6p2H; touchmove:FwuNnf; touchend:yfqBxc(preventDefault=true); touchcancel:JMtRjd;" jsshadow="" aria-label="I am a new customer" aria-disabled="true" data-value="I am a new customer" role="radio" aria-checked="false"><div class="x0k1lc MbhUzd"></div><div class="uyywbd"></div><div class="vd3tt"><div class="AB7Lab Id5V1"><div class="rseUEf nQOrEb"></div></div></div></div></div><div class="YEVVod"><div class="ulDsOb"><span dir="auto" class="aDTYNe snByac OvPDhc OIC90c">I am a new customer</span></div></div></div></label></div><div class="nWQGrd zwllIb"><label for="i8" class="docssharedWizToggleLabeledContainer ajBQVb RDPZE"><div class="bzfPab wFGF8"><div class="d7L4fc bJNwt  FXLARc aomaEc ECvBRb"><div id="i8" class="Od2TWd hYsg7c RDPZE" jscontroller="EcW08c" jsaction="keydown:I481le;dyRcpb:dyRcpb;click:cOuCgd; mousedown:UX7yZ; mouseup:lbsD7e; mouseenter:tfO1Yc; mouseleave:JywGue; focus:AHmuwe; blur:O22p3e; contextmenu:mg9Pef;touchstart:p6p2H; touchmove:FwuNnf; touchend:yfqBxc(preventDefault=true); touchcancel:JMtRjd;" jsshadow="" aria-label="I am an existing customer" aria-disabled="true" data-value="I am an existing customer" role="radio" aria-checked="false"><div class="x0k1lc MbhUzd"></div><div class="uyywbd"></div><div class="vd3tt"><div class="AB7Lab Id5V1"><div class="rseUEf nQOrEb"></div></div></div></div></div><div class="YEVVod"><div class="ulDsOb"><span dir="auto" class="aDTYNe snByac OvPDhc OIC90c">I am an existing customer</span></div></div></div></label></div></div></span></div></div></div><div jsname="Rfh2Tc" class="SL4Sz" id="i3" role="alert"></div></div></div></div>
    """
    response = agent.chat(prompt)
    print("Agent:", response)
