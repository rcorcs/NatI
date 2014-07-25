"""This file is concerned with handling with numbers"""

import string
import types

import nltk
import en
import sympy

def isNumber(text):
	text = nltk.word_tokenize(text.lower())
	if len(text)==0:
		return False
	answer = True
	for word in text:
		if word not in ['a', 'and'] and not en.is_number(word):
			answer = False
			break
	return answer

def exp2words(expstr):
	expstr = nltk.word_tokenize(expstr.lower())
	text = ''
	operators = {'+': 'plus', '-': 'minus', '/': 'divided by', '*': 'multiplied by', '=': 'is equal to', '**': 'to the power of', 'log':'the logarithm of'}
	lw = None
	for w in expstr:
		if lw!=None:
			if en.is_number(lw):
				text += en.number.spoken(lw)+' '
			elif lw=='*' and w=='*':
				w = '**'
			elif lw in operators:
				text += operators[lw]+' '
		lw = w
	if en.is_number(lw):
		text += en.number.spoken(w)+' '
	elif lw=='*' and w=='*':
		w = '**'
	elif lw in operators:
		text += operators[lw]+' '
	return text.strip()
			

def __parsePreOrderExp(text):
	expstr = ''
	num = ''
	op = None
	brackets = 0
	operators = {'add':'+', 'subtract':'-', 'multiply':'*', 'divide':'/'}
	for w in text:
		word = en.spelling.suggest(w)[0]
		if word in operators:
			if len(num)>0:
				brackets += 1
				if isNumber(num) and num!='and':
					expstr += str(words2num(num.strip()))+' '+op+' ('
				else:
					return None
				num = ''
			op = operators[word]
		elif isNumber(word) and word!='and':
			num += word+' '
		elif word in ['and', ',']:
			if len(num)>0:
				if isNumber(num) and num!='and':
					expstr += str(words2num(num.strip()))+' '+op+' '
				else:
					return None
			else:
				return None
			num = ''
		else:
			return None
	if len(num)>0:
		expstr += str(words2num(num.strip()))
	while brackets>0:
		expstr += ')'
		brackets -= 1
	if len(expstr)>0:
		return expstr
	else:
		return None

def __parseInOrderExp(text):
	text = [w for w in text if w!='by']
	operators = {'plus':'+', 'minus':'-', 'multiplied':'*', 'divided':'/'}
	expstr = ''
	num = ''
	for w in text:
		word = en.spelling.suggest(w)[0]
		if word in operators:
			if len(num)>0:
				if isNumber(num):
					expstr += str(words2num(num.strip()))+' '+operators[word]+' '
				else:
					return None
				num = ''
		elif isNumber(word):
			num += word+' '
		else:
			return None
	if len(num)>0:
		expstr += str(words2num(num.strip()))

	if len(expstr)>0:
		return expstr
	else:
		return None

def words2exp(text):
	#text = nltk.word_tokenize(text.lower())
	#alreadyExp = True
	#for word in text:
	#	if not (word.isdigit() or word in ['+', '-', '*', '/', '**', '(', ')']):
	#		alreadyExp = False
	#		break
	#if alreadyExp and len(text)>0:
	#	return ' '.join(text)
	isExp = False
	try:
		isExp = en.is_number(str(sympy.simplify(text).evalf()))
	except Exception, e:
		isExp = False
	if isExp:
		return text
	else:
		text = nltk.word_tokenize(text.lower())
		if len(text)==0:
			return None
		elif text[0] in ['add', 'subtract', 'multiply', 'divide']:
			return __parsePreOrderExp(text)
		else:
			return __parseInOrderExp(text)

#how to write n out in words?
def num2words(n):
   dic = { 1:'one', 2:'two', 3:'three', 4:'four', 5:'five', 6:'six', 7:'seven', 8:'eight', 9:'nine', 10:'ten',
           11:'eleven', 12:'twelve', 13:'thirteen', 14:'fourteen', 15:'fifteen', 16:'sixteen', 17:'seventeen', 18:'eighteen', 19:'nineteen',
           20:'twenty', 30:'thirty', 40:'forty', 50:'fifty', 60:'sixty', 70:'seventy', 80:'eighty', 90:'ninety',
           100:'hundred', 1000:'thousand', 1000000:'million', 1000000000:'billion', 1000000000000:'trillion', 1000000000000000:'quadrillion' }
   words = ''
   numstr = str(n)
   numlen = len(numstr)
   i = 0

   if n==0:
      return 'zero'
   
   while i<numlen:
      index = numlen - i
      num = n%(10**index)
      if num == 0:
         break
      if index==1:
         words = words + dic[num]
      elif index==2:
         if num <= 20:
            if numlen > 2:
               if numstr[i-1]!='0':
                  words = words + ' and '
                  #words = words + (' ',' and ')[ands]
               else:
                  words = words + ' '
            words = words + dic[num]
            break
         elif numstr[i]!='0':
            if numlen > 2:
               if numstr[i-1]!='0':
                  words = words + ' and '
                  #words = words + (' ',' and ')[ands]
               else:
                  words = words + ' '
            words = words + dic[(int(numstr[i])*10)]
            if numstr[i+1]!='0':
               words = words + '-'
      elif index==3:
         if numstr[i]!='0':
            if numlen > 3:
               words = words + ' '
               #words = words + ' and '
            words = words + dic[(int(numstr[i]))] + ' ' + dic[100]
      elif index<=6:
         wds = num2words(num/1000)
         if wds != 'zero':
            if numlen > 6:
               words = words + ' '
            words = words + wds + ' ' + dic[1000]
         i = i + 2 + (index-6)
      elif index<=9:
         wds = num2words(num/1000000)
         if wds != 'zero':
            if numlen > 9:
               words = words + ' '
            words = words + wds + ' ' + dic[1000000]
         i = i + 2 + (index-9)
      elif index<=12:
         wds = num2words(num/1000000000)
         if wds != 'zero':
            if numlen > 12:
               words = words + ' '
            words = words + wds + ' ' + dic[1000000000]
         i = i + 2 + (index-12)
      elif index<=15:
         wds = num2words(num/1000000000000)
         if wds != 'zero':
            if numlen > 15:
               words = words + ' '
            words = words + wds + ' ' + dic[1000000000000]
         i = i + 2 + (index-15)
      elif index<=18:
         words = words + num2words(num/1000000000000000) + ' ' + dic[1000000000000000]
         i = i + 2 + (index-18)
      else:
         raise ValueError('%s is too big to write out in words' % (numstr))
      i = i + 1
   return words

def words2num(words):
   dic = { 'zero':0, 'a':1, 'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9, 'ten':10,
           'eleven':11, 'twelve':12, 'thirteen':13, 'fourteen':14, 'fifteen':15, 'sixteen':16, 'seventeen':17, 'eighteen':18, 'nineteen':19,
           'twenty':20, 'thirty':30, 'forty':40, 'fifty':50, 'sixty':60, 'seventy':70, 'eighty':80, 'ninety':90,
           'hundred':100, 'thousand':1000, 'million':1000000, 'billion':1000000000, 'trillion':1000000000000, 'quadrillion':1000000000000000 }
   num = 0
   nums = [0]
   tokens = string.split(words, ' ')

   count_ands = tokens.count('and')
   for i in range(count_ands):
      tokens.remove('and')

   for i in range(len(tokens)):
      token = tokens[i]
      if token=='a':
         if i==(len(tokens)-1):
            raise ValueError('misuse of the \'a\' in the number \'%s\'' % (words))
         elif tokens[i+1]!='hundred' and tokens[i+1]!='thousand' and tokens[i+1]!='million' and tokens[i+1]!='billion' and tokens[i+1]!='trillion' and tokens[i+1]!='quadrillion':
            raise ValueError('misuse of the \'a\' in the number \'%s\'' % (words))

      if token=='hundred':
         num = num*dic[token]
      elif token=='thousand' or token=='million' or token=='billion' or token=='trillion' or token=='quadrillion':
         num = num*dic[token]
         nums.append(num)
         num = 0
      else:
         if string.find(token, '-')>=0:
            num = num + dic[token[:string.find(token, '-')]] + dic[token[string.find(token, '-')+1:]]
         else:
            num = num + dic[token]

   for n in nums:
      num += n

   return num

#
# FUNCTION FOR TESTING THE CONVERTION FUNCTIONS
#

def testNums(n):
   wds = num2words(n)
   print n, ': ', wds, ': ', words2num(wds)

def testWords(s):
   print s, ': ', words2num(s)

def tests():
   testNums(0)
   testNums(1)
   testNums(8)
   testNums(11)
   testNums(200)
   testNums(2500)
   testNums(102021)
   testNums(123)
   testNums(958)
   testNums(4002)
   testNums(4720)
   testNums(1432)
   testNums(21547)
   testNums(999999)
   testNums(1000000)
   testNums(1402167)
   testNums(2000105)
   testNums(10001010)
   testNums(120010712)
   testNums(1000000000)
   testNums(1001001001)
   testNums(100000000000000)
   testNums(100000000001001)
   testNums(100000000001501)
   testNums(987654321012345)
   try:
      testNums(1000000000000000)
   except ValueError as error:
      print error

   testWords('eleven hundred')
   testWords('twenty-five hundred')
   testWords('twenty five hundred')
   testWords('five hundred forty one thousand sixty nine')
   testWords('twenty five hundred')
   testWords('a hundred')
   testWords('a thousand a hundred')

   try:
      testWords('a')
   except ValueError as error:
      print error

   try:
      testWords('a five')
   except ValueError as error:
      print error

