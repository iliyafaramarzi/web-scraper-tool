from bs4 import BeautifulSoup
import requests as rq
from os.path  import basename

url = input("Enter Url: ")


response = rq.get(url)
soup = BeautifulSoup(response.text, "html.parser")
while True:
	inp = input(">> ")
	inp = inp.strip().lower()
	
	li = inp.split(' ')
	
	if inp == 'exit':
		break
	
	elif inp == 'url':
		print(url)
		continue
	
	elif inp == 'title':
		title = soup.find('title')
		print(title.text)
		continue
	
	elif inp == 'links':
		links = soup.find_all('link')
		print('total links: ', len(links))	
		print('links address: ')
		for link in links:
			print(link['href'], ' - ', link['rel'])
	
	elif inp == 'scripts':
		scripts = soup.find_all('script')
		print('total scripts: ', len(scripts))	
		print('scripts: ')
		for script in scripts:
			print(script)
	
	elif inp == 'help':
		print('url - get page url')
		print('title - get page title')
		print('links - get all links in page')
		print('scripts - get all scripts in page')
		print('addresses - get all addresses in page')
		print('[tag] texts - return all texts of [tag]')
		print('[tag] count - return how many times [tag] used')
		print('download images - Download all images in page|\n\t\t\t\t\t     | -sl : If use -sl don\'t get links like : [url]/[image address]\n\t\t\t\t\t     | Image format : you can change image format to save (not recommended)\n\t\t\t\t\t     | -- : Detect Image format and save with right format\n\t\t\t\t\t     | Command Type: download images [-sl] [--] ["png", "jpg", "svg", ...]')


	elif inp == 'addresses':
		addresses = soup.find_all('a')
		print('total addresses: ', len(addresses))
		for address in addresses:
			print(address['href'],  ' - ', address.text)

	elif li[0] == 'download' and li[1] == 'images':
		links = soup.find_all('img')
		if len(li) == 2:
			for counter, link in enumerate(links):
				pic = rq.get(f"{url}/{link['src']}").content
				with open(f'{counter + 1}.jpg', 'wb') as picture: 
					picture.write(pic) 
					print(f"{url}/{link['src']} Downloaded")
		
		elif len(li) == 3:
			for counter, link in enumerate(links):
				if link['src'] == '':
					continue
				

				if li[2] == '--':
					pic = rq.get(f"{url}/{link['src']}").content
					splited = str(link['src']).split('.')
					with open(f'{counter + 1}.{splited[-1]}', 'wb') as picture: 
						picture.write(pic) 
						print(f"{url}/{link['src']} Downloaded as {splited[-1]}")

				elif li[2] == '-sl':
					pic = rq.get(f"{link['src']}").content
					with open(f'{counter + 1}.jpg', 'wb') as picture: 
						picture.write(pic) 
						print(f"{link['src']} Downloaded")
				
				elif li[2] != '-sl' and li[2] != '--':
					pic = rq.get(f"{url}/{link['src']}").content
					with open(f'{counter + 1}.{li[2]}', 'wb') as picture: 
						picture.write(pic) 
						print(f"{url}/{link['src']} Downloaded")

		elif len(li) == 4:
			for counter, link in enumerate(links):
				if link['src'] == '':
					continue
				if 'http' in str(link['src']):
					pic = rq.get(f"{link['src']}").content
				else:
					pic = rq.get(f"{url}/{link['src']}").content
				
				if li[2] == '-sl':
					if len(li) == 4 and li[3] == '--':
						splited = str(link['src']).split('.')
						with open(f'{counter + 1}.{splited[-1]}', 'wb') as picture: 
							picture.write(pic) 
							print(f"{link['src']} Downloaded as {splited[-1]}")
					
					elif len(li) == 4 and li[3] != '--':
							with open(f'{counter + 1}.{li[3]}', 'wb') as picture: 
								picture.write(pic) 
								print(f"{link['src']} Downloaded")

					

		print('done')

	elif li[1] == 'texts':
		texts = soup.find_all(li[0])
		print('total texts: ', len(texts))
		for text in texts:
			print(text.text)
			
	elif li[1] == 'count':
		h1 = soup.find_all(li[0])
		print(len(h1))
		continue
	
	else:
		print("Invalid Command")
		
