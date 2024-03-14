## Credits
The React app has been build ontop of [ofnullable](https://github.com/ofnullable)'s template: [https://github.com/ofnullable/react-spa-template](https://github.com/ofnullable/react-spa-template)

## Installation

```shell
# clone this repository
$ git clone https://github.com/AlphaeusNg/FYP

# go into template directory
$ cd react-spa-template

# install dependencies
$ npm install
```

## Commands

### Run dev server

```shell
$ npm start
```

Run dev server on [http://localhost:5000](http://localhost:5000)

### Build

```shell
$ npm run build
```

Creating a Production Build. The build artifacts will be stored in the `dist/` directory.

### Deploy github pages

```json
# edit package.json
{
  ...
  "hompage": "https://{github username}.github.io/{repository name}",
}
```

```shell
$ npm run deploy
```

Deploy to github pages
