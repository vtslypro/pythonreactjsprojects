import * as React from "react";
import {PackageItem} from "./PackageItem";

export interface PackageListProps { packages: any }
export interface PackageListStates { selectedItem: number }

export class PackageList extends React.Component<PackageListProps, PackageListStates> {

	somefunc(index: number) {
		this.setState({selectedItem: index});
	}
	
	render() {
	 let packageElements : JSX.Element[] = [];

	 this.props.packages.map((pkg: any) => packageElements.push(
	 <PackageItem data={ pkg } index = {2}  setSelection = { this.somefunc } />
	 ));

	 return ( 
	 <div> { this.state.selectedItem} </div>
	 <div> { packageElements} </div>);

	}
	
}

