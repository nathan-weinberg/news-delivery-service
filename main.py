#!/usr/bin/python3

import os
import sys
import yaml
import jinja2
import datetime
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

NBC_YOUTUBE_CHANNEL_ID = 'UCeY0bbntWzzVIaj2z3QigXg'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def generate_query():
	''' generates YouTube API search term to be used in query
	'''
	yesteday_object = datetime.datetime.now() - datetime.timedelta(days=1)
	yesterday_day_number = int(datetime.datetime.strftime(yesteday_object, '%d'))
	yesterday_suffix = get_suffix(yesterday_day_number)
	yesterdate = datetime.datetime.strftime(yesteday_object, '%B %-d{}, %Y'.format(yesterday_suffix))
	search_term = "Nightly News {}".format(yesterdate)
	return search_term


def generate_content(search_term, videos):
	''' populates and returns jinja2 template with video data
	'''

	# initialize jinja2 vars
	loader = jinja2.FileSystemLoader('./template.html')
	env = jinja2.Environment(loader=loader)
	template = env.get_template('')

	# generate HTML report
	content = template.render(
		search_term=search_term,
		videos=videos
	)

	return content


def get_suffix(day):
	''' returns proper suffix for given day number
	'''
	return 'th' if 11 <= day <=13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')


def send_mail(content):
	''' sends email with given content
		content should be HTML
	'''

	# parse recipients
	recipients = config['recipients'].split(',')

	# construct email
	msg = MIMEMultipart()
	msg['From'] = config['sender_email']
	msg['Subject'] = 'Daily News Delivery'
	msg['To'] = ", ".join(recipients)
	msg.attach(MIMEText(content, 'html'))

	# create SMTP session
	with SMTP_SSL(host=config['smtp_host'], port=465) as smtp:

		# login
		smtp.login(config['sender_email'], config['sender_password'])

		# send email to all addresses
		response = smtp.sendmail(msg['From'], recipients, msg.as_string())

		# log success if all recipients recieved report, otherwise raise exception
		if response == {}:
			print("Report successfully accepted by mail server for delivery")
		else:
			raise Exception("Mail server cannot deliver report to following recipients: {}".format(response))


def youtube_search(search_term):

	# create youtube build object
	youtube = build(
		YOUTUBE_API_SERVICE_NAME,
		YOUTUBE_API_VERSION,
		developerKey=config['youtube_api_key']
	)

	# search youtube for video matches 
	search_response = youtube.search().list(
		q=search_term,
		part='id,snippet'
	).execute()

	# parse search results and return list of desired video titles and URLs
	videos = []
	for search_result in search_response.get('items', []):
		if search_result['id']['kind'] == 'youtube#video' and search_result['snippet']['channelId'] == NBC_YOUTUBE_CHANNEL_ID:
			video_link = 'https://www.youtube.com/watch?v=' + search_result['id']['videoId']
			videos.append({'title': search_result['snippet']['title'], 'url' : video_link})
	return videos


if __name__ == '__main__':

	# get configuration data
	try:
		with open("config.yaml", 'r') as file:
			config = yaml.safe_load(file)
	except Exception as e:
		print("Error loading configuration data: ", e)
		sys.exit()

	# generate seach term
	search_term = generate_query()

	# get YouTube videos via API search
	try:
		videos = youtube_search(search_term)
	except HttpError as e:
		print('An HTTP error {} occurred:\n{}'.format(e.resp.status, e.content))
		sys.exit()
	
	# generate email content
	content = generate_content(search_term, videos)

	# send email
	try:
		send_mail(content)
	except Exception as e:
		print('Error sending email report: {}'.format(e))
		sys.exit()
