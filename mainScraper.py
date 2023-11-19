from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup

#Here you can change the name of the file desired
filename = "products.csv"

# Get the the first url and just grab the number of pages and then leave
url = "https://ldc.lloyds.com/market-directory/results?cobc=&cob=&loc=&ltti=&bro=0&cov=1&man=0&mem=0&omc=0&run=0&name=&c_page=1"
uClient = ureq(url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, 'html.parser')
pages = page_soup.findAll("ul",{"class":"table-listing-list-pagination-pages"})[0].findAll("li")
number_of_pages = pages[len(pages)-1].a.text
print(f"There are {number_of_pages} pages to Scrape")
# The function of oppening a url and adding data
def open_url_and_fill(this_page):
	url = f"https://ldc.lloyds.com/market-directory/results?cobc=&cob=&loc=&ltti=&bro=0&cov=1&man=0&mem=0&omc=0&run=0&name=&c_page={this_page}"
	#opening up connection and grabbing the link  
	uClient = ureq(url)
	page_html = uClient.read()
	uClient.close()
	#html parsing
	page_soup = soup(page_html, 'html.parser')
	containers = page_soup.findAll("div",{"class":"contact-details"})
	data = ""
	for container in containers:
		try:
			name = str(container.findAll("h2")[0].text)
		except:
			name = ""
		try:
			obj = container.findAll("address")[0].stripped_strings
			address = ""
			for line in obj:
				address += line.replace(","," ") + " "
			address = str(address)
		except:
			address = ""
		try:
			website = str(container.p.findAll("a")[0].text)
		except:
			website = ""
		data += name + "," + address + "," + website + "\n"
	print(f"Page {this_page} / {number_of_pages} Successfully Scraped!")
	return data


f = open(filename, "w")
for i in range(1,int(number_of_pages)+1):
	if i == 1:
		#write the headers to csv
		headers = "name, address, website\n"
		f.write(headers)
	f.write(open_url_and_fill(i))
f.close()
