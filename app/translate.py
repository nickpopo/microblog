import json
import requests
import urllib.parse
from flask import current_app
from flask_babel import _


def detect_language(text):
	"""Detect the language using yandex.translate API"""
	if not len(text):
		return ''

	if 'YX_TRANSLATOR_KEY' not in current_app.config or \
			not current_app.config['YX_TRANSLATOR_KEY']:
		return _('Error: the translation service is not configured.')

	# https://tech.yandex.com/translate/doc/dg/reference/detect-docpage/
	params = {
		'key': current_app['YX_TRANSLATOR_KEY'],
		'text': text
	}
	url = 'https://translate.yandex.net/api/v1.5/tr.json/detect?'
	r = requests.get(url + urllib.parse.urlencode(params))
	if r.status_code != 200:
		return _('Error: the translation service failed.')
	return json.loads(r.content.decode('utf-8'))['lang']


def translate(text, dest_language):
	"""Translate given text to destination language."""	
	if not len(text):
		return ''

	if 'YX_TRANSLATOR_KEY' not in current_app or \
			not current_app['YX_TRANSLATOR_KEY']:
			return _('Error: the translation service is not configured.')
	# Request Yandex Translate API.
	# https://tech.yandex.com/translate/doc/dg/reference/translate-docpage/
	params = {
		'key': current_app['YX_TRANSLATOR_KEY'],
		'text': text,
		'lang': dest_language
	} 
	url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
	r = requests.get(url + urllib.parse.urlencode(params))
	if r.status_code != 200:
		return _('Error: the translation service failed.')
	return json.loads(r.content.decode('utf-8'))['text'][0]