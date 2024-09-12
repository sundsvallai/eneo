/**
 * Updater script to download latest openapi.json form staging and update types and client version
 */
import fs from "fs";
import { exec } from "node:child_process";

async function updateClient() {
  const url = "https://staging.backend.instorage.inoolabs.com/openapi.json";
  const version = await fetch(url)
    .then((res) => res.json())
    .then((json) => json.info.version);
  if (version) {
    // Update actual client.js file
    const clientFile = "./src/client/client.js";
    const client = String(fs.readFileSync(clientFile));

    // looks like this:
    // const version = "...";
    const regex = /(?<=const version = ")(.*)(?=";)/;
    const updatedClient = client.replace(regex, version);

    fs.writeFileSync(clientFile, updatedClient);

    console.log(`Updated client/client.js with current schema version ${version}`);
  } else {
    console.log("Could not update client/client.js version");
  }
}

async function updateSchema() {
  exec(
    "pnpm exec openapi-typescript https://staging.backend.instorage.inoolabs.com/openapi.json -o src/types/schema.d.ts",
    (err, stdout, stderr) => {
      if (err) {
        console.log(err);
        return;
      }
      console.log(stdout);
      console.error(stderr);
    }
  );
}

updateClient();
updateSchema();
