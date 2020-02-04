import * as React from "react";

export interface setSelectionFunc {
	(index: number): void
}


export interface PackageItemProps { data: any , 
	index : number,
setSelection : setSelectionFunc}

export interface PackageItemState {expanded: boolean}

export class PackageItem extends React.Component<PackageItemProps, PackageItemState> {
  constructor(props: PackageItemProps) {
    super(props); // Must call base-class
    this.state = { expanded: false }; // assign initial state
    this.toggleExpandState = this.toggleExpandState.bind(this);
    this.packageItemClicked = this.packageItemClicked.bind(this);
  }
  toggleExpandState() {
    let currentState = this.state.expanded;
    this.setState( { expanded: !currentState } ); // toggle boolean value
  }

  packageItemClicked() {
  	this.props.setSelection(this.props.index);
  }
  render() {
    let pkg = this.props.data; // A single package.
    let description: string = pkg.description;
    if (!this.state.expanded)
    { description = description.substr(0, 140) + "..."; }
    return (<div className="ItemContainer">
      <div className="ItemLeftPanel">
        <img className="PackageIcon" src="/resources/icons/package.png" />
      </div>
      <div className="ItemRightPanel">
        <div className="PackageCaption"> {pkg.name}
          <span className="PackageVersion">{pkg.versions.version}</span>
        </div>
        <div className="PackageAuthor" onClick= {this.packageItemClicked}>{pkg.maintainers.username}</div>
        <div className="PackageDescription" onClick={ this.toggleExpandState } >{ description }</div>
      </div>
    </div>);
  }
}