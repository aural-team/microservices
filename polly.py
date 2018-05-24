import boto3
from scraper import scrape_in_shorts
import os

def synthesize_speech(client, text, filename):

    response = client.synthesize_speech(
    	Text=text,
	    OutputFormat='mp3',
	    VoiceId='Raveena',
	)

    # The response's audio_content is binary.
    with open('files/'+filename, 'wb') as out:
        out.write(response['AudioStream'].read())
        #print('Audio content '+text+' written to file '+filename)

if __name__ == "__main__":

	client = boto3.client(
		'polly',
		aws_access_key_id="AKIAJGYOL6T2VZSROGMA",
        aws_secret_access_key="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",
        region_name="us-east-2"
	)

	num = 0
	articles = scrape_in_shorts()
	for article in articles[1:15]:
		synthesize_speech(client, article, "polly{}.mp3".format(num))
		print "synthesized {}".format(num)
		num += 1

	inputs = 'files/polly0.mp3'
	for s in range(1,num):
		inputs += '|audios/split.mp3|files/polly'+str(s)+'.mp3'

	os.system('ffmpeg -i "concat:'+inputs+'" -acodec copy polly_temp.mp3')

	#os.system('ffmpeg -i outputfinal.mp3 -i audios/background_low_vol.mp3 -filter_complex amerge -ac 2 -c:a libmp3lame -q:a 4 merged.mp3')
	os.system('ffmpeg -i polly_temp.mp3 -filter_complex "amovie=audios/background_low_vol.mp3:loop=999[s];[0][s]amix=duration=shortest" -ac 2 -c:a libmp3lame -q:a 4 polly_news.mp3')