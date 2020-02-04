/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// identity function for calling harmony imports with the correct context
/******/ 	__webpack_require__.i = function(value) { return value; };
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 4);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports) {

module.exports = React;

/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var React = __webpack_require__(0);
var PackageItem_1 = __webpack_require__(3);
var PackageList = /** @class */ (function (_super) {
    __extends(PackageList, _super);
    function PackageList() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PackageList.prototype.somefunc = function (index) {
        this.setState({ selectedItem: index });
    };
    PackageList.prototype.render = function () {
        var _this = this;
        var packageElements = [];
        this.props.packages.map(function (pkg) { return packageElements.push(React.createElement(PackageItem_1.PackageItem, { data: pkg, index: 2, setSelection: _this.somefunc })); });
        return (React.createElement("div", null,
            " ",
            this.state.selectedItem,
            " ")
            ,
                React.createElement("div", null,
                    " ",
                    packageElements,
                    " "));
    };
    return PackageList;
}(React.Component));
exports.PackageList = PackageList;


/***/ }),
/* 2 */
/***/ (function(module, exports) {

module.exports = ReactDOM;

/***/ }),
/* 3 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var React = __webpack_require__(0);
var PackageItem = /** @class */ (function (_super) {
    __extends(PackageItem, _super);
    function PackageItem(props) {
        var _this = _super.call(this, props) || this;
        _this.state = { expanded: false }; // assign initial state
        _this.toggleExpandState = _this.toggleExpandState.bind(_this);
        _this.packageItemClicked = _this.packageItemClicked.bind(_this);
        return _this;
    }
    PackageItem.prototype.toggleExpandState = function () {
        var currentState = this.state.expanded;
        this.setState({ expanded: !currentState }); // toggle boolean value
    };
    PackageItem.prototype.packageItemClicked = function () {
        this.props.setSelection(this.props.index);
    };
    PackageItem.prototype.render = function () {
        var pkg = this.props.data; // A single package.
        var description = pkg.description;
        if (!this.state.expanded) {
            description = description.substr(0, 140) + "...";
        }
        return (React.createElement("div", { className: "ItemContainer" },
            React.createElement("div", { className: "ItemLeftPanel" },
                React.createElement("img", { className: "PackageIcon", src: "/resources/icons/package.png" })),
            React.createElement("div", { className: "ItemRightPanel" },
                React.createElement("div", { className: "PackageCaption" },
                    " ",
                    pkg.name,
                    React.createElement("span", { className: "PackageVersion" }, pkg.versions.version)),
                React.createElement("div", { className: "PackageAuthor", onClick: this.packageItemClicked }, pkg.maintainers.username),
                React.createElement("div", { className: "PackageDescription", onClick: this.toggleExpandState }, description))));
    };
    return PackageItem;
}(React.Component));
exports.PackageItem = PackageItem;


/***/ }),
/* 4 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
var React = __webpack_require__(0);
var ReactDOM = __webpack_require__(2);
var PackageList_1 = __webpack_require__(1);
// Download the locally hosted data type json file.
fetch("/packages")
    .then(function (response) {
    return response.text();
}).then(function (jsonString) {
    var completeJson = JSON.parse(jsonString);
    var firstPackage = completeJson.content; // Get the first package for render.
    ReactDOM.render(React.createElement(PackageList_1.PackageList, { packages: firstPackage }), document.getElementById("myPlaceholder"));
});


/***/ })
/******/ ]);
//# sourceMappingURL=bundle.js.map