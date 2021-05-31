import sys, os
sys.path.append('/Users/yemishin/Desktop/Final-Project-carlcs322s01s21-2/InferKit') # for Yemi's local
#sys.path.append('/home/runner/Final-Project-carlcs322s01s21-2/InferKit') # for repl

import requests
import InferErrors as errors
import InferLog as log

class InferKit:
	__URL_PREFIX = 'https://api.inferkit.com/v1/models/'
	__URL_SUFFIX = '/generate'

	def __init__(self, api_key: str, model: str = 'standard'):
		self.url = self.__URL_PREFIX + model + self.__URL_SUFFIX
		self._headers = {'Authorization': 'Bearer ' + api_key}

	def generate(self, prompt: str, length: int = 100):
		data = {
			'prompt': {
				'text': prompt,
				'isContinuation': True
			},
			'length': length
		}

		try:
			r = requests.post(self.url, headers=self._headers, json=data)
			r.raise_for_status()
		except requests.exceptions.RequestException as e:
			log.error('RequestException: ' + str(e))
			return None

		try:
			reply = r.json()
		except errors.JSONDecodeError as e:
			log.error('JSONDecodeError: ' + str(e))
			return None

		if ('data' in reply) and ('text' in reply['data']):
			return reply['data']['text']

		return None

