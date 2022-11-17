let chrome = require('selenium-webdriver/chrome')
let driver = require('selenium-webdriver')
let fs = require('fs')
let exec = require('child_process').execSync

class VoterPortalScrapper {
  map_of_states = new Map([
    ["Maharashtra", "S13"],
    ["Goa", "S05"],
    ["Sikkim", "S21"],
    ["Mizoram", "S17"],
    ["Gujarat", "S06"],
  ]);

  constructor() {
    this.chrome = new driver.Builder().withCapabilities(driver.Capabilities.chrome())
            .setChromeOptions(new chrome.Options()
            .addArguments("--headless=chrome", "--no-sandbox", "--disable-dev-shm-usage")).build()

    this.search_url = "https://electoralsearch.in/"

  }

  async epicSearch(epicNo, state) {
    this.chrome.get(this.search_url);
    await this.chrome.sleep(1000)
    while ((await this.chrome.findElements({ 'id': 'continue' })).length == 1) {
      try {
        await this.chrome.findElement({ 'id': 'continue' }).click()
      }
      catch (err) {
        break;
      }
    }

    let mapped_state = this.map_of_states.get(state);

    let tab1 = await this.chrome.findElement({ 'css': "li[role='tab']" })
    await this.chrome.executeScript("arguments[0].setAttribute('class','')", tab1)
    await this.chrome.executeScript("arguments[0].setAttribute('role','')", tab1)

    let tab2 = await this.chrome.findElement({ 'css': "li[role='tab']" })
    await this.chrome.executeScript("arguments[0].setAttribute('class','active')", tab2)
    await tab2.click()


    console.log(`Filling Epic with state ${mapped_state}...`)
    await this.chrome.findElement({ 'id': 'name' }).sendKeys(epicNo)
    await this.chrome.findElement({ 'css': `#epicStateList>option[value="${mapped_state}"]` }).click()

    await this.chrome.findElement({ 'id': 'txtEpicCaptcha' }).sendKeys("axx")
    await this.chrome.sleep(2000)


    let buttons = await this.chrome.findElement({ 'id': 'btnEpicSubmit' })
    await buttons.click()
    console.log("Submitted with fake Captcha...")

    let refreshes = -1
    let found = true
    while ((await this.chrome.findElements({ 'css': "input[name='epic_no_plain']" })).length == 0) {
      refreshes++;

      if (refreshes >= 15) {
        found = false
        break;
      }

      console.log("Storing captcha png...")
      let image = await this.chrome.findElement({ id: 'captchaEpicImg' }).takeScreenshot()
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
        await this.chrome.findElement({ 'id': 'txtEpicCaptcha' }).sendKeys(data)
        this.chrome.sleep(2500)
        console.log(`Submitting with captcha: ${data}`)
        let buttons = await this.chrome.findElement({ 'id': 'btnEpicSubmit' })
        await buttons.click()
        console.log(`Submitted with captcha: ${data}`)
      });

      await this.chrome.sleep(500)
    }

    console.log("Extracting obtained details...")
    await this.extractDetails(found);

    console.log(await this.chrome.getCurrentUrl())

    console.log("Closing chrome...")
    this.chrome.close()

  }

  async detailedSearch(name, daddyName, age, gender, state, district, assemblyConstituency) {
    this.chrome.get(this.search_url);
    await this.chrome.sleep(1000)
    while ((await this.chrome.findElements({ 'id': 'continue' })).length == 1) {
      try {
        await this.chrome.findElement({ 'id': 'continue' }).click()
      }
      catch (err) {
        break;
      }
    }

    let mapped_state = this.map_of_states.get(state);

    console.log("Filling details...")
    await this.chrome.findElement({ 'id': 'name1' }).sendKeys(name)
    await this.chrome.findElement({ 'id': 'txtFName' }).sendKeys(daddyName)
    await this.chrome.findElement({ 'css': `#ageList>option[value="number:${age}"]` }).click()
    await this.chrome.findElement({ 'css': `#listGender>option[value="${gender}"]` }).click()
    await this.chrome.findElement({ 'css': `#nameStateList>option[value="${mapped_state}"]` }).click()

    let dropDowns = await this.chrome.findElements({ 'css': '#namelocationList' })
    if (district) await dropDowns[0].sendKeys(district)
    if (assemblyConstituency) await dropDowns[1].sendKeys(assemblyConstituency)

    await this.chrome.findElement({ 'id': 'txtCaptcha' }).sendKeys("axx")
    await this.chrome.sleep(2500)


    let buttons = await this.chrome.findElements({ 'id': 'btnDetailsSubmit' })
    await buttons[1].click()
    console.log("Submitted with fake Captcha...")

    let refreshes = -1
    let found = true
    while ((await this.chrome.findElements({ 'css': "input[name='epic_no_plain']" })).length == 0) {
      refreshes++;

      if (refreshes >= 15) {
        found = false
        break;
      }

      console.log("Storing captcha png...")
      let image = await this.chrome.findElement({ id: 'captchaDetailImg' }).takeScreenshot()
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
        await this.chrome.findElement({ 'id': 'txtCaptcha' }).sendKeys(data)
        this.chrome.sleep(2500)
        console.log(`Submitting with captcha: ${data}`)
        let buttons = await this.chrome.findElements({ 'id': 'btnDetailsSubmit' })
        await buttons[1].click()
        console.log(`Submitted with captcha: ${data}`)
      });

      await this.chrome.sleep(1000)
    }

    console.log("Extracting obtained details...")
    await this.extractDetails(found);

    console.log("Closing chrome...")
    this.chrome.close()
  }

  async extractDetails(found) {
    var user;

    console.log(`   Found user details: ${found}`)
    if (found) {
    console.log(`   Parsing user details...`)
      this.chrome.sleep(500)
      let name = await this.chrome.findElement({ 'css': 'input[name="name"]' }).getAttribute('value')
            let name2 = await this.chrome.findElements({'id': '#resultsTable'})
            console.log(name2)
      let epicNo = await this.chrome.findElement({ "css": "input[name='epic_no_plain']" }).getAttribute('value')
      let gender = await this.chrome.findElement({ 'css': "input[name='gender']" }).getAttribute('value')
      let age = await this.chrome.findElement({ 'css': "input[name='age']" }).getAttribute('value')
      let fatherOrHusbandName = await this.chrome.findElement({ 'css': "input[name='rln_name']" }).getAttribute('value')
      let state = await this.chrome.findElement({ 'css': "input[name='state']" }).getAttribute('value')
      let district = await this.chrome.findElement({ "css": "input[name='district']" }).getAttribute('value')
      let ac_name = await this.chrome.findElement({ "css": "input[name='ac_name']" }).getAttribute('value')
      let ac_no = await this.chrome.findElement({ "css": "input[name='ac_no']" }).getAttribute('value')
      let pc_name = await this.chrome.findElement({ "css": "input[name='pc_name']" }).getAttribute('value')
      let part_no = await this.chrome.findElement({ "css": "input[name='part_no']" }).getAttribute('value')
      let ps_name = await this.chrome.findElement({ "css": "input[name='ps_name']" }).getAttribute('value')
      console.log(`   Parsed user details with name: ${name}...`)

      user = {
        found, epicNo, name, age, gender, fatherOrHusbandName, state, district, ac_no, ac_name, pc_name, part_no, ps_name
      }
      console.log(`   User created: ${user}`)
    }
    else {
      user = {
        found
      }
    }

    console.log(`   Writing user details to json...`)
    fs.writeFile('scraper_parser_translator/views/voter_portal/data.json', JSON.stringify(user), function(err) {
      if (err) throw err
    })
    console.log(`   Written user details to json...`)

  }
}


console.log(process.argv)
let scraper = new VoterPortalScrapper()
let [__, ___, searchMethod] = process.argv

if (searchMethod == "epic_search"){
    let [_, __, searchMethod, epicNo, state] = process.argv
    scraper.epicSearch(epicNo, state)
}
else{
    let [_, __, searchMethod, name, fatherOrHusbandName, age, gender, state, district, assemblyConstituency] = process.argv
    scraper.detailedSearch(name, fatherOrHusbandName, age, gender, state, district, assemblyConstituency)
}

