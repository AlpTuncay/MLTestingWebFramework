import React from "react";

class ModelObject extends React.Component {

  constructor(props){
    super(props);
  }

  render() {
    return (
      <div className="col-md-4">
        <br />
        <div className="card">
          <div className="card-header">
            {this.props.model_title}
          </div>
          <div className="card-body">
            {this.props.model_framework}
          </div>
        </div>
      </div>
    )
  }
}

export default ModelObject;
