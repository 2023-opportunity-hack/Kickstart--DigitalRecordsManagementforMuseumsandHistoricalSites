import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import PyPDF2
# test change
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = T5ForConditionalGeneration.from_pretrained("Michau/t5-base-en-generate-headline")
tokenizer = T5Tokenizer.from_pretrained("Michau/t5-base-en-generate-headline")
model = model.to(device)

article = '''
In 1905 textile businessman Colonel George Fabyan and his wife Nelle purchased 10 acres with a c.1870 farmhouse on the Fox River in Geneva, Illinois.  Originally from Boston, he and his wife had been living in Chicago since 1892.
 In 1907 they hired Frank Lloyd Wright to redesign and expand the simple farm house.  They then decided to live in Geneva year-round. The redesigned house has many features of Prairie Style architecture that Frank Lloyd Wright made famous.  To George and Nelle, it was their country home, and they called it the Villa. 
Over time, the Villa became part of a 300-acre estate the Fabyans named Riverbank.  Riverbank was developed by the George and Nelle so they could spend their time on their own interests.  Among George’s interests was scientific research and technological development.  He created a private laboratory, where experts, scientists and other workers worked on a wide variety of ideas, including trying to prove the authorship of Shakespeare's plays, helping the U.S. government with code breaking during World War I, groundbreaking acoustic research, development and production of tuning forks, medical research. He also collected unusual artifacts and had a small private museum at the Laboratory.  
Mrs. Fabyan grew roses and peonies, and tended the rose arbors and formal gardens, including the Centennial Garden and Japanese Garden.  Two banks of greenhouses existed on the estate to support the massive gardening efforts.  She also loved animals, raised national award winning Jersey cattle and show dogs and trained carrier pigeons.  The estate also sported a zoo which included bears, deer, monkeys, a wolf, prairie dogs, alligators and exotic birds.    
Many other features of the estate indicate the Fabyans enjoyed the outdoors.  On the west lawn of the Villa, there was a cement firepit surrounded by hammocks and chairs. Paths and benches lined the Villa grounds.  Fountains and grottoes were created in natural ravines and depressions. A large swimming pool sat at the south end of their island in the river.  A boathouse on the west bank housed a canoe, rowboat and sailboat.  Tennis courts and an outdoor amphitheater were installed for guests and parties. 
One of the Fox Valley’s most famous landmarks is also a Fabyan relic.  Fabyan had a Dutch windmill moved to his property in 1914 from York Center (near Lombard, Illinois).  The windmill ground grain for the Fabyans and local farmers until about 1920 when it was no longer operated regularly.  The windmill has been restored and turns when there is enough wind.  


JAPANESE GARDEN

A Japanese Garden was built for the Fabyans around 1910 by Taro Otsuka, a well-known Japanese landscape architect.  This style of garden was very popular with wealthy people around the turn of the century.  They could afford the unusual plants and skilled gardeners to maintain a garden of this type.  After the Fabyan’s deaths, the Japanese Garden fell into disrepair. The garden still exists in a modified form today.  In 1972, the Geneva Garden Club undertook a renovation of the Fabyan’s Japanese Garden.  In 1994 a second renovation took place under the guidance of the Forest Preserve District of Kane County.  The current Japanese Garden is not an exact replica of the Fabyans’ garden, but has kept many of the same features, ideas, and a few of the original plants.   In recent years the Torii gate, Waiting Bench, Half Moon Bridge, pond steps, waterfall and East gate have been rebuilt.  The restored Tea House and large Japanese Lantern are original to the Fabyan time period. 
The Villa and windmill are recognized on the National Register of Historic Places. 
The Fabyan Villa Museum and Japanese Garden are owned and maintained by the Kane County Forest Preserve District, and operated for public visitation by Preservation Partners of the Fox Valley.





'''

text = "headline: " + article

max_len = 256

encoding = tokenizer.encode_plus(text, return_tensors="pt")
input_ids = encoding["input_ids"].to(device)
attention_masks = encoding["attention_mask"].to(device)

beam_outputs = model.generate(
    input_ids=input_ids,
    attention_mask=attention_masks,
    max_length=64,
    num_beams=3,
    early_stopping=True,
)

result = tokenizer.decode(beam_outputs[0])
print(result)
