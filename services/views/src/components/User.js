import React from "react";

class User extends React.Component {
    constructor(props) {
        super(props);

    }

    render() {
        return (
            <div className="row d-flex justify-content-center">
                <div className="col-md-12">
                    <div className="card">
                        <div className="card-body">
                            <h3>Welcome {this.props.username}</h3>
                        </div>
                    </div>
                    <div className="card">
                        {(Array.isArray(this.props.models) && this.props.models.length > 0) && <div className="card-body col-md-3">A</div>}
                        {(Array.isArray(this.props.models) && this.props.models.length === 0) &&
                        <div className="card-body d-flex justify-content-center">
                            You have not deployed any models yet.
                        </div>}
                        <div className="card-footer d-flex justify-content-center">
                            {this.props.models}
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default User;