import * as React from "react";
import * as ReactDOM from "react-dom";

import { PackageList } from "./components/PackageList";

// Download the locally hosted data type json file.
fetch("/packages")
  .then(function (response: Response) {
    return response.text();
  }).then(function (jsonString) {
    let completeJson = JSON.parse(jsonString);
    let firstPackage = completeJson.content; // Get the first package for render.
   
    ReactDOM.render(
      <PackageList packages={firstPackage}/>,
      document.getElementById("myPlaceholder")
    );

});