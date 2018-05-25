import boto3
from scraper import scrape_in_shorts
from datetime import datetime
import os
import threading

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

def generate_audio(article_count=10):
	client = boto3.client(
		'polly',
		aws_access_key_id="AKIAJMSSNCHY3ZLX2NHA",
        aws_secret_access_key="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",
        region_name="us-east-2"
	)

	num = 0
	articles = scrape_in_shorts()
	threads = []
	for article in articles[1:article_count]:
		t = threading.Thread(target=synthesize_speech, args=(client, article, "polly{}.mp3".format(num)))
		t.start()
		threads.append(t)
		synthesize_speech(client, article, "polly{}.mp3".format(num))
		num += 1

	for t in threads:
		t.join()

	inputs = 'files/polly0.mp3'
	for s in range(1,num):
		inputs += '|audios/split.mp3|files/polly'+str(s)+'.mp3'

	timestr = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
	os.system('ffmpeg -i "concat:'+inputs+'" -acodec copy polly_temp_{}.mp3'.format(timestr))

	#os.system('ffmpeg -i outputfinal.mp3 -i audios/background_low_vol.mp3 -filter_complex amerge -ac 2 -c:a libmp3lame -q:a 4 merged.mp3')
	os.system('ffmpeg -i polly_temp_{}.mp3 -filter_complex "amovie=audios/background_low_vol.mp3:loop=999[s];[0][s]amix=duration=shortest" -ac 2 -c:a libmp3lame -q:a 4 polly_news_{}.mp3'.format(timestr, timestr))
	return 'polly_temp_{}.mp3'.format(timestr), 'polly_news_{}.mp3'.format(timestr)

if __name__ == "__main__":
	tmpfile, audiofile = generate_audio()
	print tmpfile, audiofile