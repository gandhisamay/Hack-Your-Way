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
    this.chrome = new driver.Builder().withCapabilities(driver.Capabilities.chrome()).build()
    this.search_url = "https://electoralsearch.in/"

  }

  async run(name, daddyName, age, gender, state, district, assemblyConstituency) {
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

    let refreshes = -1
    let found = true
    while ((await this.chrome.findElements({ 'css': "input[name='epic_no_plain']" })).length == 0) {
      refreshes++;

      if (refreshes >= 15) {
        found = false
        break;
      }

      let image = await this.chrome.findElement({ id: 'captchaDetailImg' }).takeScreenshot()
      fs.writeFileSync('scraper_parser_translator/views/voter_portal/captcha.png', image, 'base64', function(err) {
        if (err) throw err
      })


      exec('python3 -m  scraper_parser_translator.views.mainCaptcha ; cat scraper_parser_translator/views/voter_portal/captcha_text', function(err, stdout, _) {
        console.log(stdout)
        if (err) throw err
      })


      fs.readFile('scraper_parser_translator/views/voter_portal/captcha_text', { encoding: 'utf8' }, async (_, data) => {
        await this.chrome.findElement({ 'id': 'txtCaptcha' }).sendKeys(data)
        this.chrome.sleep(2500)
        let buttons = await this.chrome.findElements({ 'id': 'btnDetailsSubmit' })
        await buttons[1].click()
      });

      await this.chrome.sleep(1000)
    }

    var user;

    if (found) {
      let epicNo = await this.chrome.findElement({ "css": "input[name='epic_no_plain']" }).getAttribute('value')
      let district = await this.chrome.findElement({ "css": "input[name='district']" }).getAttribute('value')
      let ac_name = await this.chrome.findElement({ "css": "input[name='ac_name']" }).getAttribute('value')
      let ac_no = await this.chrome.findElement({ "css": "input[name='ac_no']" }).getAttribute('value')
      let pc_name = await this.chrome.findElement({ "css": "input[name='pc_name']" }).getAttribute('value')
      let part_no = await this.chrome.findElement({ "css": "input[name='part_no']" }).getAttribute('value')
      let ps_name = await this.chrome.findElement({ "css": "input[name='ps_name']" }).getAttribute('value')

      user = {
        found, epicNo, district, ac_no, ac_name, pc_name, part_no, ps_name
      }
    }
    else {
      user = {
        found
      }
    }

    fs.writeFile('scraper_parser_translator/views/voter_portal/data.json', JSON.stringify(user), function(err) {
      if (err) throw err
    })

    this.chrome.close()
  }
}


console.log(process.argv)
let [_, __, name, fatherOrHusbandName, age, gender, state, district, assemblyConstituency] = process.argv
let scraper = new VoterPortalScrapper()
scraper.run(name, fatherOrHusbandName, age, gender, state, district, assemblyConstituency);
