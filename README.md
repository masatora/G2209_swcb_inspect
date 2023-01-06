# G2209_swcb_inspect (g2209-swcb-inspect)

A Quasar Project

## Install the dependencies
```bash
yarn
# or
npm install
```

### Start the app in development mode (hot-code reloading, error reporting, etc.)
```bash
quasar dev
```


### Lint the files
```bash
yarn lint
# or
npm run lint
```



### Build the app for production
```bash
quasar build
```

### Customize the configuration
See [Configuring quasar.config.js](https://v2.quasar.dev/quasar-cli-vite/quasar-config-js).

### docker command
```bash
docker build -f Dockerfile_backend --tag g2209_swcb_inspect_backend .
docker run -d --name g2209_inspect_backend -p 10091:10091 -p 5432:5432 --env-file ./.env_backend g2209_swcb_inspect_backend
docker build -f Dockerfile_frontend --tag g2209_swcb_inspect_frontend .
docker run -d --name g2209_inspect_frontend -p 10090:10090 g2209_swcb_inspect_frontend
```
