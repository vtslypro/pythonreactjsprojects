import * as React from "react"

export interface HelloProps {
	name : string
}
export class Hello extends React.Component<HelloProps, undefined> {
	render() {
		return <div className="MainCaption"> Hellow from { this.props.name } </div>;

	}
}


