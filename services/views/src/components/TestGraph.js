import React from "react";
import { Redirect } from "react-router-dom";
import FusionCharts from "fusioncharts";
import charts from "fusioncharts/fusioncharts.charts";
import ReactFusioncharts from "react-fusioncharts";

charts(FusionCharts);

const axios = require("axios").default;


class TestGraph extends React.Component {

  constructor(props){
    super(props);
    this.state = {}
  }

  getGraphDataForModel = () => {
    axios.get(`http://127.0.0.1:5002/graph/${this.props.model_id}`,
              {headers: {"x-access-token": window.localStorage.getItem("x-access-token")}}
    ).then(response => {
      console.log(response)

      const dataSource = {
          chart: {
            caption: "Historical Test Results of the Model",
            showhovereffect: "1",
            drawcrossline: "1",
            showLegend: "1"
          },
          categories: [{
            category: response.data.graph_data.category
          }],
          dataset: response.data.graph_data.dataset_results
      };

      const runTimeStats = {
          chart: {
            caption: "Runtime Statistics of the Model",
            showhovereffect: "1",
            drawcrossline: "1",
            showLegend: "1"
          },
          categories: [{
            category: response.data.graph_data.category
          }],
          dataset: response.data.graph_data.dataset_runtime
      };

      this.setState({
        test_result: dataSource,
        runtime_stats: runTimeStats
      })

    }).catch(error => {
      console.error(error)
    })
  }

  componentDidMount() {
    this.getGraphDataForModel()
  }

  render(){

    return (
      <div className="col-md-12">
          <br />
          <div className="card">
              <ReactFusioncharts
                type="msline"
                width="100%"
                dataFormat="JSON"
                dataSource={this.state.test_result}
              />
          </div>
          <div className="card">
              <ReactFusioncharts
                type="msline"
                width="100%"
                dataFormat="JSON"
                dataSource={this.state.runtime_stats}
              />
          </div>
      </div>

    )

  }

}

export default TestGraph;
