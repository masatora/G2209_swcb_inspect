module.exports = {
  dev: {
    BASE_URL: 'http://192.168.50.3:10090',
    API_URL: 'http://192.168.50.3:10091/api'
  },
  beta: {
    BASE_URL: 'http://192.168.2.110:10090',
    API_URL: 'http://192.168.2.110:10091/api'
  },
  stage: {
    BASE_URL: 'https://iot.thinktron.co/ntpcswc',
    API_URL: 'https://iot.thinktron.co/ntpcswc/api'
  },
  // prod: {
  //   BASE_URL: 'https://iot.thinktron.co/ntpcswc',
  //   API_URL: 'https://iot.thinktron.co/ntpcswc/api'
  // }
  prod: {
    BASE_URL: 'http://192.168.2.110:10090',
    API_URL: 'http://192.168.2.110:10091/api'
  }
}
