import React from 'react'

function Facility(props) {
  return (
    <div className="card col-lg-3 col-md-4 col-sm-6">
      <img className="card-img-top" src={props.data.imageLink} alt={props.data.altText} />
      <div className="card-body">
        <h5 className="card-title">{props.data.name}</h5>
        <a href={props.data.link}>Details</a>
      </div>
      
    </div>
  );
}

export default Facility;