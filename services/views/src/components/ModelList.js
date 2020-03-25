import React from "react";
import ModelObject from "./ModelObject";
import ModelTest from "./ModelTest";

import {BrowserRouter as Router, Switch, Route} from "react-router-dom";

class ModelList extends React.Component {
    constructor(props) {
        super(props);

    }

    render() {
        return (
          <div className="row">
            <br />
              {this.props.models.map((item) => (
                  <ModelObject key={item.id} model_id={item.id} model_title={item.model_title}
                                model_framework={item.model_framework} name={item.filename}>
                  </ModelObject>
              ))}
          </div>
        )
    }
}

export default ModelList;
