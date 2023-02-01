import { createRoot } from 'react-dom/client';
import React from 'react'
import Facility from '../components/facility';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    fetch("api/facilities")
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then(data => {
        this.setState({
          data: data,
          loaded: true
        });
      });
  }

  render() {
    if(this.state.loaded) {
      return (
        <div className='row row-cols-1 row-cols-md-2 row-cols-lg-3 g-3'>
          {this.state.data.facilities.map((facility) =>
            <div className='col'>
              <Facility key={facility.id} data={facility} />
            </div>
          )}
        </div>
      );
    } else {
      return (
        <p>
          {this.state.placeholder}
        </p>
      );
    }
    
  }
}

export default App;

const container = document.getElementById("app");
const root = createRoot(container)
root.render(<App />);