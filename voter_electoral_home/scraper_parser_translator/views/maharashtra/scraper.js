let chrome = require('selenium-webdriver/chrome')
let driver = require('selenium-webdriver')
let fs = require('fs')
let exec = require('child_process').execSync
let http = require('http')

class MaharashtraScraper {
  constructor() {
    this.userPreferences = {
      'download.default_directory': '/home/samaygandhi/Documents/Hack-Your-Way/voter_electoral_home/scraper_parser_translator/views/maharashtra',
      "download.prompt_for_download": false,
      "download.directory_upgrade": true,
      "plugins.always_open_pdf_externally": true
    }

    this.chrome = new driver.Builder().withCapabilities(driver.Capabilities.chrome())
      .setChromeOptions(new chrome.Options()
        .addArguments("--no-sandbox", "--disable-dev-shm-usage").setUserPreferences(this.userPreferences)).build()
    this.searchUrl = "https://ceoelection.maharashtra.gov.in/searchlist/"
  }

  async run(district, assemblyConstituency, pollingPart) {

    await this.chrome.get(this.searchUrl)
    await this.chrome.findElement({ 'id': 'ctl00_Content_DistrictList' }).sendKeys(district)


    let left = assemblyConstituency.split('-')[0]
    let right = assemblyConstituency.split('-')[1]
    assemblyConstituency = right + '-' + left

    await this.chrome.findElement({ 'id': 'ctl00_Content_AssemblyList' }).sendKeys(assemblyConstituency)
    await this.chrome.findElement({ 'css': `#ctl00_Content_PartList>option[value='94'}]` }).click()
    // let image = await this.chrome.findElements({ 'css': 'img' })[1].takeScreenshot()
    let images = await this.chrome.findElements({ 'css': 'img' })
    let image = await images[1].takeScreenshot()

    fs.writeFileSync('scraper_parser_translator/views/voter_portal/captcha.png', image, 'base64', function(err) {
      if (err) throw err
    })


    console.log("Parsing captcha png to text...")
    exec('python3 -m  scraper_parser_translator.views.mainCaptcha', function(err, stdout, _) {
      console.log(stdout)
      if (err) throw err
    })


    console.log("Reading captcha text...")
    fs.readFile('scraper_parser_translator/views/voter_portal/captcha_text', { encoding: 'utf8' }, async (_, data) => {
      console.log(`Got captcha text: ${data}`)
      await this.chrome.findElement({ 'id': "ctl00_Content_txtcaptcha" }).sendKeys(data)
      let openPDFButton = await this.chrome.findElement({ 'id': "ctl00_Content_OpenButton" })
      await openPDFButton.click()

      console.log(await this.chrome.getCurrentUrl())


      let file = fs.createWriteStream('electoral_rolls.pdf')
      http.get("http://ceoelection.maharashtra.gov.in/searchlist/ViewPDF.aspx"
        , function(response) {
          response.pipe(file)

          file.on("finish", () => {
            file.close();
            console.log("Download Completed");
          });
        })




      console.log(`Submitted with captcha: ${data}`)
    });
  }

}


let scraper = new MaharashtraScraper()
scraper.run('Mumbai Suburban', 'Dhaisar - 153', 1)
