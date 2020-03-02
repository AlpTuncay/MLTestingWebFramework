import React from "react";
import ModelObject from "./ModelObject";

class ModelList extends React.Component {
    constructor(props) {
        super(props);

    }

    render() {
        return (
          <div className="row d-flex justify-content-center">
            <br />
              {this.props.models.map((item) => (
                <ModelObject key={item.id} model_title={item.model_title} model_framework={item.model_framework} />
              ))}
          </div>
        )
    }
}

export default ModelList;
