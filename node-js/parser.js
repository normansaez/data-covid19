const StreamArray = require("stream-json/streamers/StreamArray");
const path = require("path");
const { Writable } = require("stream");
const fs = require("fs-extra");

const fileStream = fs.createReadStream(path.join(__dirname, "comunas.json")); // Cambiar el nombre y encerrar el GeoJSON completo en corchetes ([])
const jsonStream = StreamArray.withParser();

const processingStream = new Writable({
  write({ key, value }, encoding, callback) {

    setTimeout(() => {
      console.log(value.features[0]);
      value.features.forEach((el) => {
        // Cada elemento es una comuna
        let file =
          "comunas/" +
          el.properties.REGION +
          "_" +
          el.properties.NOM_REGION +
          "/" +
          el.properties.PROVINCIA +
          "_" +
          el.properties.NOM_PROVIN +
          "/" +
          el.properties.COMUNA +
          "_" +
          el.properties.NOM_COMUNA +
          '.json'
          ;
        fs.outputFile(file, JSON.stringify(el));

        return;
      });

      callback();
    }, 1000);
  },
  objectMode: true,
});

fileStream.pipe(jsonStream.input);
jsonStream.pipe(processingStream);

processingStream.on("finish", () => console.log("All done"));