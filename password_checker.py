#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 13:52:19 2020

@author: hannahannuniemi
"""

import requests
import hashlib
import sys

filename = str(sys.argv[1])

def request_api_data(query_char):
  url = 'https://api.pwnedpasswords.com/range/' + query_char
  res = requests.get(url)
  if res.status_code != 200:
    raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
  return res

def get_password_leaks_count(hashes, hash_to_check):
  hashes = (line.split(':') for line in hashes.text.splitlines())
  for h, count in hashes:
    if h == hash_to_check:
      return count
  return 0

def pwned_api_check(password):
  sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
  first5_char, tail = sha1password[:5], sha1password[5:]
  response = request_api_data(first5_char)
  return get_password_leaks_count(response, tail)

def main(filename):
  with open (filename, "r") as file:
    for password in file:
        count = pwned_api_check(password.strip())
        if count:
          print(f'{password} was found {count} times... you should probably change your password!')
        else:
          print(f'{password} was NOT found. Carry on!')
  return 'done!'

  
if __name__ == '__main__':
  sys.exit(main(sys.argv[1]))