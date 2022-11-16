// var fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));
var driver = require('selenium-webdriver')
var fs = require('fs')
var chrome = new driver.Builder().withCapabilities(driver.Capabilities.chrome()).build()

let func = async function() {



  url = "https://electoralsearch.in/"

  chrome.get(url);

  await chrome.findElement({ id: 'continue' }).click()
  chrome.findElement({ id: 'captchaDetailImg' }).takeScreenshot().then(
    function(image, err) {
      fs.writeFile('captcha.png', image, 'base64', function(err) {
        if (err) throw err
      })
    }
  )

  // var promise = chrome.getTitle();

  //
  // promise.then(function(title) {
  //
  //   console.log(title);
  //
  // });


  // data = {
  //   "txtCaptcha": "qIyuDe",
  //   "search_type": "details",
  //   "reureureired": "ca3ac2c8-4676-48eb-9129-4cdce3adf6ea",
  //   "name": "Nirali Gandhi",
  //   "rln_name": "Amit Gandhi",
  //   "page_no": 1,
  //   "location": "S13,,",
  //   "results_per_page": 10,
  //   "location_range": "20",
  //   "age": 45,
  //   "dob": null,
  //   "gender": "F"
  // }
  //
  // let res = await fetch(url, {
  //   method: 'POST',
  //   headers: {
  //     'Content-Type': 'application/json',
  //   },
  //   body: JSON.stringify(data)
  // })
  //
  // let result = await res.text()
  // console.log(result)
}

func()
