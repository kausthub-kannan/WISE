import os
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.core.output_parsers import LangchainOutputParser
from wise.templates.SCHEMA import qa_response_schema
from langchain.output_parsers import StructuredOutputParser
from wise.templates.PROMPT import qaPrompt
import json
import ast


class QAagent:
    def __init__(self, data_dir="dummy_data"):
        api_key = os.environ["GROQ_API_KEY"]

        embed_model = HuggingFaceEmbedding(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        Settings.embedding_model = embed_model

        Settings.context_window = 4096
        Settings.num_output = 256

        documents = SimpleDirectoryReader(data_dir).load_data()
        self.index = VectorStoreIndex.from_documents(
            documents,
            embed_model=embed_model,
        )

        lc_output_parser = StructuredOutputParser.from_response_schemas(
            qa_response_schema
        )
        self.llm = Groq(
            model="mixtral-8x7b-32768",
            api_key=api_key,
            temperature=0.5,
            output_parser=LangchainOutputParser(lc_output_parser),
        )
        self.query_engine = self.index.as_query_engine(llm=self.llm)

    def chat(self, data: str, prompt: str):
        prompt = qaPrompt.format(raw_html=data, prompt=prompt)
        response = self.query_engine.query(prompt)

        try:
            data_dict = ast.literal_eval(str(response))
            json_response = json.dumps(data_dict, indent=4)
            return json_response
        except json.JSONDecodeError:
            return f"Invalid JSON response: {type(str(response))}"


if __name__ == "__main__":
    agent = QAagent()
    raw_html = """<div class="Qr7Oae" role="listitem"><div jsmodel="CP1oW" data-params="%.@.[1941031617,&quot;What are the item(s) you would like to order?&quot;,null,4,[[1000027,[[&quot;Pen&quot;,null,null,null,false],[&quot;Eraser&quot;,null,null,null,false],[&quot;Notebook&quot;,null,null,null,false],[&quot;Sharpener&quot;,null,null,null,false]],true,null,null,null,null,null,false,null,[]]],null,null,null,null,null,null,[null,&quot;What are the item(s) you would like to order?&quot;]],&quot;i11&quot;,&quot;i12&quot;,&quot;i13&quot;,false]"><div jscontroller="sWGJ4b" jsaction="EEvAHc:yfX9oc;" jsname="WsjYwc" class="geS5n"><div class="z12JJ"><div class="M4DNQ"><div id="i11" class="HoXoMd D1wxyf RjsPE" role="heading" aria-level="3" aria-describedby="i14"><span class="M7eMe">What are the item(s) you would like to order?</span><span class="vnumgf" id="i14" aria-label="Required question"> *</span></div><div class="gubaDc OIC90c RjsPE" id="i12"></div></div></div><div jscontroller="sW52Ae" jsaction="rcuQ6b:vZc4S;O22p3e:zjh6rb;b2trFe:eVidQc;sPvj8e:sEDvJ;JIbuQc:d3sQLd(MPu53c);" class="Y6Myld"><input type="hidden" name="entry.1000027_sentinel" jsname="DTMEae"><div role="list" aria-labelledby="i11" aria-describedby="i12 i13 i15" class=""><div class="eBFwI" role="listitem" jsaction="JIbuQc:aj0Jcf" jscontroller="lWjoT" jsname="MPu53c"><label for="i16" class="docssharedWizToggleLabeledContainer Yri8Nb"><div class="bzfPab wFGF8"><div id="i16" class="uVccjd aiSeRd FXLARc wGQFbe BJHAP oLlshd" jscontroller="EcW08c" jsaction="keydown:I481le;dyRcpb:dyRcpb;click:cOuCgd; mousedown:UX7yZ; mouseup:lbsD7e; mouseenter:tfO1Yc; mouseleave:JywGue; focus:AHmuwe; blur:O22p3e; contextmenu:mg9Pef;touchstart:p6p2H; touchmove:FwuNnf; touchend:yfqBxc(preventDefault=true); touchcancel:JMtRjd;" jsshadow="" jsname="FkQz1b" aria-label="Pen" data-answer-value="Pen" role="checkbox" aria-checked="false" tabindex="0"><div class="PkgjBf MbhUzd"></div><div class="uHMk6b fsHoPb"></div><div class="rq8Mwb"><div class="TCA6qd"><div class="MbUTNc oyD5Oc"></div><div class="Ii6cVc oyD5Oc"></div></div></div></div><div class="YEVVod"><div class="ulDsOb"><span dir="auto" class="aDTYNe snByac n5vBHf OIC90c">Pen</span></div></div></div></label></div><div class="eBFwI" role="listitem" jsaction="JIbuQc:aj0Jcf" jscontroller="lWjoT" jsname="MPu53c"><label for="i19" class="docssharedWizToggleLabeledContainer Yri8Nb"><div class="bzfPab wFGF8"><div id="i19" class="uVccjd aiSeRd FXLARc wGQFbe BJHAP oLlshd" jscontroller="EcW08c" jsaction="keydown:I481le;dyRcpb:dyRcpb;click:cOuCgd; mousedown:UX7yZ; mouseup:lbsD7e; mouseenter:tfO1Yc; mouseleave:JywGue; focus:AHmuwe; blur:O22p3e; contextmenu:mg9Pef;touchstart:p6p2H; touchmove:FwuNnf; touchend:yfqBxc(preventDefault=true); touchcancel:JMtRjd;" jsshadow="" jsname="FkQz1b" aria-label="Eraser" data-answer-value="Eraser" role="checkbox" aria-checked="false" tabindex="0"><div class="PkgjBf MbhUzd"></div><div class="uHMk6b fsHoPb"></div><div class="rq8Mwb"><div class="TCA6qd"><div class="MbUTNc oyD5Oc"></div><div class="Ii6cVc oyD5Oc"></div></div></div></div><div class="YEVVod"><div class="ulDsOb"><span dir="auto" class="aDTYNe snByac n5vBHf OIC90c">Eraser</span></div></div></div></label></div><div class="eBFwI" role="listitem" jsaction="JIbuQc:aj0Jcf" jscontroller="lWjoT" jsname="MPu53c"><label for="i22" class="docssharedWizToggleLabeledContainer Yri8Nb"><div class="bzfPab wFGF8"><div id="i22" class="uVccjd aiSeRd FXLARc wGQFbe BJHAP oLlshd" jscontroller="EcW08c" jsaction="keydown:I481le;dyRcpb:dyRcpb;click:cOuCgd; mousedown:UX7yZ; mouseup:lbsD7e; mouseenter:tfO1Yc; mouseleave:JywGue; focus:AHmuwe; blur:O22p3e; contextmenu:mg9Pef;touchstart:p6p2H; touchmove:FwuNnf; touchend:yfqBxc(preventDefault=true); touchcancel:JMtRjd;" jsshadow="" jsname="FkQz1b" aria-label="Notebook" data-answer-value="Notebook" role="checkbox" aria-checked="false" tabindex="0"><div class="PkgjBf MbhUzd"></div><div class="uHMk6b fsHoPb"></div><div class="rq8Mwb"><div class="TCA6qd"><div class="MbUTNc oyD5Oc"></div><div class="Ii6cVc oyD5Oc"></div></div></div></div><div class="YEVVod"><div class="ulDsOb"><span dir="auto" class="aDTYNe snByac n5vBHf OIC90c">Notebook</span></div></div></div></label></div><div class="eBFwI" role="listitem" jsaction="JIbuQc:aj0Jcf" jscontroller="lWjoT" jsname="MPu53c"><label for="i25" class="docssharedWizToggleLabeledContainer Yri8Nb"><div class="bzfPab wFGF8"><div id="i25" class="uVccjd aiSeRd FXLARc wGQFbe BJHAP oLlshd" jscontroller="EcW08c" jsaction="keydown:I481le;dyRcpb:dyRcpb;click:cOuCgd; mousedown:UX7yZ; mouseup:lbsD7e; mouseenter:tfO1Yc; mouseleave:JywGue; focus:AHmuwe; blur:O22p3e; contextmenu:mg9Pef;touchstart:p6p2H; touchmove:FwuNnf; touchend:yfqBxc(preventDefault=true); touchcancel:JMtRjd;" jsshadow="" jsname="FkQz1b" aria-label="Sharpener" data-answer-value="Sharpener" role="checkbox" aria-checked="false" tabindex="0"><div class="PkgjBf MbhUzd"></div><div class="uHMk6b fsHoPb"></div><div class="rq8Mwb"><div class="TCA6qd"><div class="MbUTNc oyD5Oc"></div><div class="Ii6cVc oyD5Oc"></div></div></div></div><div class="YEVVod"><div class="ulDsOb"><span dir="auto" class="aDTYNe snByac n5vBHf OIC90c">Sharpener</span></div></div></div></label></div></div><div id="i15" class="fKfAyc">Required</div></div><div jsname="Rfh2Tc" class="SL4Sz" id="i13" role="alert"></div></div></div></div>"""
    prompt = """
    Hey, I am an existing customer, and I want to order pens and notebooks of red and blue colors. Quantity of the items should be 4. As per details about me, I’m Kavan, and I’m available at 9548565487 / kavan@gmail.com. Preferred mode of communication is either phone or email. Thanks!
    """
    print(agent.chat(raw_html, prompt))
