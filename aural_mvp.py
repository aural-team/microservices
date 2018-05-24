from gensim.summarization.summarizer import summarize
from gtts import gTTS
import json
import os
from pprint import pprint
import requests
from google.cloud import language
from google.cloud import texttospeech
from google.cloud.language import enums
from google.cloud.language import types
import six


#url = 'https://newsapi.org/v2/top-headlines?sources=techcrunch,the-verge,wired&pageSize=40&apiKey=6746db3f285a482eb943507c56d56898'
url = 'https://newsapi.org/v2/top-headlines?country=in&apiKey=6746db3f285a482eb943507c56d56898'
VOICES = {'en-GB-Standard-A','en-GB-Standard-B','en-GB-Standard-C','en-GB-Standard-D','en-US-Wavenet-A','en-US-Wavenet-B','en-US-Wavenet-C','en-US-Wavenet-D','en-US-Wavenet-E','en-US-Wavenet-F','en-US-Standard-B','en-US-Standard-C','en-US-Standard-D','en-US-Standard-E'}
client = texttospeech.TextToSpeechClient()

def entities_text(text):
    """Detects entities in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

    for entity in entities:
        '''print('=' * 20)
        print(u'{:<16}: {}'.format('name', entity.name))
        print(u'{:<16}: {}'.format('type', entity_type[entity.type]))
        print(u'{:<16}: {}'.format('metadata', entity.metadata))
        print(u'{:<16}: {}'.format('salience', entity.salience))
        print(u'{:<16}: {}'.format('wikipedia_url',
              entity.metadata.get('wikipedia_url', '-'))) '''
        if entity_type[entity.type] == 'ORGANIZATION' or entity_type[entity.type] == 'LOCATION' or entity_type[entity.type] == 'EVENT':
            text = text.replace(entity.name,'<emphasis level="moderate">'+entity.name+"</emphasis>")
            print('{}-----{}'.format(entity.name,entity_type[entity.type]))
    return text

def synthesize_text(text, filename, voice_str):

    text = '<speak>'+text+'</speak>'
    input_text = texttospeech.types.SynthesisInput(ssml=text)
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        name=voice_str,#'en-US-Wavenet-A',
        #name='en-GB-Standard-B',        
        ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)

    audio_config = texttospeech.types.AudioConfig(
        speaking_rate=0.85,
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is binary.
    with open('files/'+filename, 'wb') as out:
        out.write(response.audio_content)
        #print('Audio content '+text+' written to file '+filename)



#text = 'To get to the Uber conference on flying cars in Los Angeles last week, where I was scheduled to interview Uber CEO Dara Khosrowshahi,'+str('I hailed a Lyft. My driver was understandably amused about where I was going.\'Flying cars?\' he said, laughing. \'That makes more sense than the self-driving ones.\'My driver was right: these days, it seems likely Uber will have flying cars before it has self-driving cars. The fatal crash involving one of the ride-hailing company’s autonomous test vehicles in Tempe, Arizona this past March was a huge blow to the company’s self-driving program. Federal investigators are still digging into what happened, but the death of Elaine Herzberg forced Uber to shut down its testing program nationwide. Khosrowshahi is already looking beyond the investigation, though.''In a “fireside chat” with Bloomberg’s Brad Stone at the end of the Elevate conference, he said autonomous testing was likely to resume “in a few months.” Regardless of what federal crash investigators finds, Khosrowshahi is already planning for the future.''This is typical of the 48-year-old, who, in some ways, is always looking to the horizon. Born in Tehran into a wealthy Muslim family, Khosrowshahi and his family were forced to flee right before the Iranian Revolution, first to Southern France, and then to Upstate New York. After a stint in investment banking, he became CEO of Expedia in 2001, where he grew the business to a massive scale and became one of the highest paid chief executives in the country, with compensation totaling $94.6 million.''Since taking the reins at Uber in August 2017, Khosrowshahi has focused on two things: apologizing for the sins of his predecessor, Travis Kalanick; and making a series of deals to grow Uber beyond app-based ride-hailing. The past few months have been a flurry of activity as Khosrowshahi puts his own stamp on the troubled company. Ride-hailing is and will remain Uber’s core business for the near term — but Khosrowshahi sees a whole world of potential outside the car.''The first part of the job, well, you’ve probably read all about Uber’s disastrous 2017. Every day seemed to bring a fresh allegation, a new self-inflicted humiliation or scandal, and the further deterioration of the company’s responsibility to operate in good faith on behalf of its drivers and customers. Khosrowshahi has made plenty of apologies. And now he’s trying to focus on making Uber a better company.''He’s made some pretty good progress. Uber bought dockless bike-share company Jump for a reported $150–200 million. Uber’s also making moves to add car-sharing vehicles, as well as public transportation like buses and trains, to its app. The company will also share more of its data on traffic patterns and curbside usage with cities in an effort to become “true partners to cities for the long term,” Khosrowshahi said. And, of course, there are the flying cars.''Though the 2017 scandals got more press, Uber lost $4.5 billion last year, a staggering figure for a global company with tens of thousands of employees and millions of drivers. The company closed the year with around $6 billion in cash, 13 percent below the prior year’s total — indicating that new investments aren’t keeping up with the company’s expenditures. And it continues to face a host of legal and regulatory challenges, both in the US and abroad.''Meanwhile, Lyft continues to grow its share of the ride-hailing business, finishing the year with 30 percent of the market’s revenue, creeping up behind Uber’s 70 percent.'
text = 'To get to the Uber conference on flying cars in Los Angeles last week, where I was scheduled to interview Uber CEO Dara Khosrowshahi, I hailed a Lyft. My driver was understandably amused about where I was going.\'Flying cars?\' he said, laughing. \'That makes more sense than the self-driving ones.\'My driver was right: these days, it seems likely Uber will have flying cars before it has self-driving cars. The fatal crash involving one of the ride-hailing company’s autonomous test vehicles in Tempe, Arizona this past March was a huge blow to the company’s self-driving program. Federal investigators are still digging into what happened, but the death of Elaine Herzberg forced Uber to shut down its testing program nationwide. Khosrowshahi is already looking beyond the investigation, though.''In a “fireside chat” with Bloomberg’s Brad Stone at the end of the Elevate conference, he said autonomous testing was likely to resume “in a few months.” Regardless of what federal crash investigators finds, Khosrowshahi is already planning for the future.''This is typical of the 48-year-old, who, in some ways, is always looking to the horizon. Born in Tehran into a wealthy Muslim family, Khosrowshahi and his family were forced to flee right before the Iranian Revolution, first to Southern France, and then to Upstate New York. After a stint in investment banking, he became CEO of Expedia in 2001, where he grew the business to a massive scale and became one of the highest paid chief executives in the country, with compensation totaling $94.6 million.''Since taking the reins at Uber in August 2017, Khosrowshahi has focused on two things: apologizing for the sins of his predecessor, Travis Kalanick; and making a series of deals to grow Uber beyond app-based ride-hailing. The past few months have been a flurry of activity as Khosrowshahi puts his own stamp on the troubled company. Ride-hailing is and will remain Uber’s core business for the near term — but Khosrowshahi sees a whole world of potential outside the car.''The first part of the job, well, you’ve probably read all about Uber’s disastrous 2017. Every day seemed to bring a fresh allegation, a new self-inflicted humiliation or scandal, and the further deterioration of the company’s responsibility to operate in good faith on behalf of its drivers and customers. Khosrowshahi has made plenty of apologies. And now he’s trying to focus on making Uber a better company.''He’s made some pretty good progress. Uber bought dockless bike-share company Jump for a reported $150–200 million. Uber’s also making moves to add car-sharing vehicles, as well as public transportation like buses and trains, to its app. The company will also share more of its data on traffic patterns and curbside usage with cities in an effort to become “true partners to cities for the long term,” Khosrowshahi said. And, of course, there are the flying cars.''Though the 2017 scandals got more press, Uber lost $4.5 billion last year, a staggering figure for a global company with tens of thousands of employees and millions of drivers. The company closed the year with around $6 billion in cash, 13 percent below the prior year’s total — indicating that new investments aren’t keeping up with the company’s expenditures. And it continues to face a host of legal and regulatory challenges, both in the US and abroad.''Meanwhile, Lyft continues to grow its share of the ride-hailing business, finishing the year with 30 percent of the market’s revenue, creeping up behind Uber’s 70 percent.So when Khosrowshahi says he wants to transform Uber into a multi-modal company that connects people to bikes, buses, car rentals, and maybe even flying taxis, it’s a little confusing. Bikes and buses seem like a distraction from the main mission of building a profitable ride-sharing business, one not deeply dependent on capital-backed subsidies. Should this unprofitable company with a litany of internal issues really be putting people into these drone-helicopter things and send them whizzing across cities at hundreds of miles an hour? I quickly realized in coming here that the future of Uber couldn’t be just about cars,” Khosrowshahi told me, sitting in a small room in LA’s Skirball Cultural Center, a few hours before his scheduled “fireside chat.” He’d just left a meeting with actor and venture capitalist Ashton Kutcher — Khosrowshahi wouldn’t say what the two discussed, but Kutcher is an early investor in Uber — and appeared excited to talk about Uber’s future and its plans for a commercial “urban air mobility” service by 2023. But it won’t be flying taxis or bike-share that save Uber from itself. Khosrowshahi will need to show a concerted effort to correct the mistakes of the past and rebuild Uber as a company deserving of people’s trust and money. Otherwise its piece of the pie will continue to shrink, and Uber will go from ride-sharing giant to just another bit player in a crowded market.'
text2 = 'HTC is the latest to hop onto the blockchain bandwagon, with the company announcing plans to make a new blockchain-powered Android phone, as first reported by TheNextWeb. The company is naming it Exodus and giving it a universal wallet and hardware support for cryptocurrencies and decentralized apps. To start with, the Exodus phone will have support for bitcoin, ethereum, and other major networks, with more partnerships expected to come later on. HTC envisions a native blockchain network that uses Exodus phones as nodes that support cryptocurrency trading between users. HTC is also reportedly considering allowing people to purchase the Exodus phone with cryptocurrency. No price has been set yet for the phone.HTC Vive founder Phil Chen will be heading all blockchain initiatives. The move follows the recent trend of Facebook Messenger and Instagram executives switching over to lead a blockchain division for Facebook. Accordingly, Chen’s new title will be “decentralized chief officer.” We’ve also reached out to HTC for more information. Chen said during the New York City blockchain conference, Consensus 2018, today: “We envision a phone where you hold your own keys, you own your own identity and data, and your phone is the hub.”HTC’s Exodus might be the world’s second blockchain-powered phone. The first one, created by Sirin Labs, called Finney, is a phone that lets people store and use digital currencies while skipping transaction fees. It costs $1,000. It’s interesting to note the range of companies that have launched their own blockchain initiatives, from established companies seeking more profits and to remain competitive to decentralized networks, to those seeking novelty, and others that are trying to rescue their images. HTC, which laid off a significant portion of its US staff this year and merged its smartphone and virtual reality divisions, might fall in the last category of companies.'
text3 = 'The highlight of Google’s  I/O keynote earlier this month was the reveal of Duplex, a system that can make calls to set up a salon appointment or a restaurant reservation for you by calling those places, chatting with a human and getting the job done. That demo drew lots of laughs at the keynote, but after the dust settled, plenty of ethical questions popped up because of how Duplex tries to fake being human. Over the course of the last few days, those were joined by questions from people like writer John Gruber about whether the demo was staged or edited. Axios then asked Google a few simple questions about the demo that Google has refused to answer. We have reached out to Google with a number of very specific questions about this and have not heard back. As far as I can tell, the same is true for other outlets that have contacted the company. If you haven’t seen the demo, take a look at this before you read on. So did Google fudge this demo? Here is why people are asking and what we know so far. During his keynote, Google CEO Sundar Pichai noted multiple times that we were listening to real calls and real conversations (“What you will hear is the Google Assistant actually calling a real salon.”). The company made the same claims in a blog post (“While sounding natural, these and other examples are conversations between a fully automatic computer system and real businesses.”). Google has so far declined to disclose the name of the businesses it worked with and whether it had permission to record those calls. California is a two-consent state, so our understanding is that permission to record these calls would have been necessary (unless those calls were made to businesses in a state with different laws). So on top of the ethics questions, there are also a few legal questions here. We have some clues, though. In the blog post, Google Duplex lead Yaniv Leviathan and engineering manager Matan Kalman posted a picture of themselves eating a meal “booked through a call from Duplex.” Thanks to the wonder of crowdsourcing and a number of intrepid sleuths, we know that this restaurant was Hongs Gourmet in Saratoga, California. We called Hongs Gourmet last night, but the person who answered the phone referred us to her manager, who she told us had left for the day. (We’ll give it another try today.) Sadly, the rest of Google’s audio samples don’t contain any other clues as to which restaurants were called. What prompted much of the suspicion here is that nobody who answers the calls from the Assistant in Google’s samples identifies their name or the name of the business. My best guess is that Google cut those parts from the conversations, but it’s hard to tell. Some of the audio samples do however sound as if the beginning was edited out. Google clearly didn’t expect this project to be controversial. The keynote demo was clearly meant to dazzle — and it did so in the moment because, if it really works, this technology represents the culmination of years of work on machine learning. But the company clearly didn’t think through the consequences. My best guess is that Google didn’t fake these calls. But it surely only presented the best examples of its tests. That’s what you do in a big keynote demo, after all, even though in hindsight, showing the system fail or trying to place a live call would have been even better (remember Steve Job’s Starbucks call?). For now, we’ll see if we can get more answers, but so far all of our calls and emails have gone unanswered. Google could easily do away with all of those questions around Duplex by simply answering them, but so far, that’s not happening.'

#with open('temp.json') as f:
#    data = json.load(f)

resp = requests.get(url=url)
data = resp.json()

pprint(data)

#print(str(client.list_voices()[0]['name']))
for voice in VOICES:
    num = 0
    for article in data['articles']:
        text_to_tts = str(article['title'])#str(article['title'])+'. '+str(article['description'])
        print(text_to_tts+'\n')
        filename = str(num)+'.mp3'
        num += 1
        #text_to_tts = entities_text(text_to_tts)
        synthesize_text(text_to_tts, filename, voice)

    inputs = 'files/0.mp3'
    for s in range(1,num):
        inputs += '|audios/split.mp3|files/'+str(s)+'.mp3'

    os.system('ffmpeg -i "concat:'+inputs+'" -acodec copy '+voice+'_temp.mp3')

    #os.system('ffmpeg -i outputfinal.mp3 -i audios/background_low_vol.mp3 -filter_complex amerge -ac 2 -c:a libmp3lame -q:a 4 merged.mp3')
    os.system('ffmpeg -i '+voice+'_temp.mp3 -filter_complex "amovie=audios/background_low_vol.mp3:loop=999[s];[0][s]amix=duration=shortest" -ac 2 -c:a libmp3lame -q:a 4 '+voice+'_news.mp3')
#summary = summarize(text3)
#print(summary)
#synthesize_text(summary)
#tts = gTTS(text=summary)
#tts.save("summary.mp3")
