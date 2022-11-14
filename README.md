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

  **Detailed Search**
      
    Inputs Required
      1) Name
      2) Father's or Husband's name
      3) Age
      4) State
      5) District (Optional)
      6) Assembly Constituency (Optional)
        
  **EPIC Search**
    
    Inputs Required
      1) Voter Id / Epic No 
      2) State
      
### OCR of the Captcha
After giving the user input the next thing is we use Google Vision API to get the captcha extracted from image of the portal. This captcha is then sent to the website so that we can further get the details.

### Getting the User Data
Then the next step is we click the submit button using the scraper and once that is done the results appear in the HTML and then using the appropriate tags the data is scraped from the screen and sent back to the server.

### Output
The following fields are obtained as an output from the voter information portal
```
1) EPIC No
2) Husband Name
3) Assembly Constituency Number
4) Assembly Constituency Name
5) Parliamentary Constituency
6) Part Name
7) Part Number
8) Polling station
```

### Issues
1) Voter Information Portal is too slow at times and thus takes long to return the data and may lead to failure.
2) State Electoral Portal is in a different language for many states.

## Scrapping the Statewise Electoral Portal
In this step, we first input the details received from the voter information portal and then get the captcha by perfoming PhotoOCR, and then using all of the fields to get the pdf of the state electoral rolls data. 
```
States Scraped
1) Sikkim 
2) Goa
3) Mizoram
4) Gujarat
5) Maharashtra
```

These 5 states cover majority of the cases for all the 29 states.

## Pdf Parsing

### Challenges 

After we receive the polling booth pdf from web scrapping, we observe that the pdf was formed of images. To overcome this issue, we use Document-AI API as OCR file
reader to convert the images to characters. But Document-AI was restraining us from parsing more than 10 pages at once. So we divide our input file into batches of pdf
each of size 10 and concatanate them to get the parsed file.

### Translation of Indic Languages

In most states, we observed that the Electoral Roll pdf is obtained in that state's regional language for most of the polling booths. Thus we needed to transliterate
the information into English so we could process the information in a uniform way. We used the Googletrans library in python to translate the contents of the electoral
roll from Indic languages like Marathi and Gujarati into English.

### Getting the list of voters

Once we obtain a text document of the translated Electrocal Roll, we generate a list of voters that are present in that locality. We get the voter's-
```
1) Name
2) Father's Name or Husband's Name or Other's Name
3) House Number
4) Age
5) Gender
```

and create a csv file containing their information. This csv file is now passed to the Family Tree generation algorithm.

### Issues
1) The state electoral rolls pdf obtained are present in different language for each and every state and hence has to be translated first everytime.
2) Translation process is way too slow at times and hence might cause issues.
3) Translation results received from the Google Translate are incorrect often.

## Family Tree Algorithm
In this part, we use C++ language for writing the algorithms which will help us getting the required family tree. The required family tree returns the following relations if the data returned after translation is not broken.
```
1) Father
2) Mother
3) Spouse
4) Father-in-law
5) Mother-in-law
6) Children
7) Neighbors (Individuals living in the same household, identified by the same house number)
```
We created a Node class representing an individual or a node of the Family tree. The class contains the Name, gender, Age, and House Number, along with the relationships mentioned.


We started with a ``getData()`` function that fetched all the data contained within a CSV file. We then found the corresponding Father/ Husband denoted by a boolean stored by searching the entire roll for possible candidates. This was done in the ``setData()`` function with the help of Balanced Binary Search Trees in the form of sets. This step also added the Children and Spouses to the corresponding lists.

 Then, we used the ``pruneData()`` function to extend the information available into setting the Mothers, Father-in-laws and Mother-in-laws of the individuals, and also clubbed all the individuals living in the same household together using a similar hash-like **balanced binary search tree method** in the form of an unordered map.  

After finishing all of this, we returned the necessary candidates in the CSV file format that matched the search query that was supplied as parameter arguments to the main function.

## Input format for Postman API

### For Search via Voter Information
```
{
    "name": "NAME_YOU_WANT_TO_SEARCH",
    "state": "STATE",
    "gender": "GENDER( CAN ONLY BE M/F/O)",
    "age": AGE,
    "father_or_husband_name": "FATHER'S OR HUSBAND'S NAME",
    "father_or_husband": 1 FOR FATHER, 0 FOR HUSBAND
}
```

### For EPIC Search
```
{
    "epic_no": "EPIC NUMBER",
    "state": "STATE"
}
```
