import requests, bs4, os
url = 'http://threewordphrase.com'

#setting directory for saving file
os.chdir("Specified Directory")
os.makedirs('Comics', exist_ok=True)

while not url.endswith('#'):

    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'lxml')

    # identify .gif within website
    for comicImg in soup.findAll("div", {"align": "center"}):
        for findImg in comicImg.findAll("table", {"width": "403"}):
            getImg = findImg.findAll("img")

    # identify previous comic URL
    for comicPrev in soup.findAll("div", {"align": "center"}):
        for checkPrev in comicPrev.findAll("td", {"width": "173"}):
            for prevUrl in checkPrev.findAll("a"):
                prevUrl = prevUrl['href']

    # ensure that img object has found a picture
    if (comicImg == []) or (getImg == []):
        print('No image boys.')

    # parse the comic url and verify it's valid
    else:
        try:
            comicUrl = "http://threewordphrase.com/" + getImg[0].get('src')
            print('Lets DL this: %s' % (comicUrl))
            res = requests.get(comicUrl)
            res.raise_for_status()

        except requests.exceptions.MissingSchema:

            url = 'http://threewordphrase.com' + prevUrl
            continue

    #write the picture to the drive
    imageFile = open(os.path.join('Comics', os.path.basename(comicUrl)), 'wb')
    for chunk in res.iter_content(1000000):
        imageFile.write(chunk)


    imageFile.close()
    url = 'http://threewordphrase.com' + prevUrl

print('Done.')
