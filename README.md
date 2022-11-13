# Hack-Your-Way

# Problem Statement

Create a Family Tree of all families in India (Pan India) using Electoral Roll Pdf.

# Overview of our approach

Our approach is divided into 4 parts:
1) Scrapped the Voter Information Portal and got the user state, district and assembly constituency details.
2) Scrapped the Statewise Electoral Rolls Portal to get the voters list for the all the users in the user state. 
3) Parsed the pdf obtained from the statewise portal and then stored the details for each voter in a csv file.
4) Used the csv file and then used binary search trees, maps and set data structures and recursive algorithms to generate the final family tree. 

# Stepwise details

## Scrapping the Voter Information Portal
### Giving the user input

  ***Detailed Search***
      
    Inputs Required
      1) Name
      2) Father's or Husband's name
      3) Age
      4) State
      5) District (Optional)
      6) Assembly Constituency (Optional)
        
  ***EPIC Search***
    
    Inputs Required
      1) Voter Id / Epic No 
      2) State
      
### OCR of the Captcha
After giving the user input the next thing is we use Google Vision API to get the captcha extracted from image of the portal. This captcha is then sent to the website so that we can further get the details.

### Getting the User Data
Then the next step is we click the submit button using the scraper and once that is done the results appear in the HTML and then using the appropriate tags the data is scraped from the screen and sent back to the server.

## Scrapping the Statewise Electoral Portal
## Input the State, Assembly Constituency data.
The data that was obtained regarding the user from the previous step is used in this step to scrape the electoral roll data for the state of the user.

## OCR of Captcha
Once again performed the PhotoOCR of the captcha available on this portal and used that to 

## Pdf Parsing

### Problems faced while parsing

After we receive the polling booth pdf from web scrapping, we observe that the pdf was formed of images. To overcome this issue, we use Document-AI API as OCR file
reader to convert the images to characters. But Document-AI was restraining us from parsing more than 10 pages at once. So we divide our input file into batches of pdf
each of size 10 and concatanate them to get the parsed file.

### Translation of Indic Languages

In most states, we observed that the Electoral Roll pdf is obtained in that state's regional language for most of the polling booths. Thus we needed to transliterate
the information into English so we could process the information in a uniform way. We used the Googletrans library in python to translate the contents of the electoral
roll to translate from Indic languages like Marathi and Gujarati into English.

### Getting the list of voters

Once we obtain a text document of the translated Electrocal Roll, we generate a list of voters that are present in that locality. We get the voter's-
* Name
* Father's Name or Husband's Name or Other's Name
* House Number
* Age
* Gender
and create a csv file containing their information. This csv file is now passed to the Family Tree generation algorithm.


