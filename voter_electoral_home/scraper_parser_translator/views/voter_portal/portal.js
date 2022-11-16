let func = async function() {
  url = "https://electoralsearch.in"
  data = {
    "txtCaptcha": "qIyuDe",
    "search_type": "details",
    "reureureired": "ca3ac2c8-4676-48eb-9129-4cdce3adf6ea",
    "name": "Nirali Gandhi",
    "rln_name": "Amit Gandhi",
    "page_no": 1,
    "location": "S13,,",
    "results_per_page": 10,
    "location_range": "20",
    "age": 45,
    "dob": null,
    "gender": "F"
  }

  let res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
  })

  let result = await res.text()
  console.log(result)
}

func()
